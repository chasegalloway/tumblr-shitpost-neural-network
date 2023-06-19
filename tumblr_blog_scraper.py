import pytumblr
import csv
from unidecode import unidecode
import calendar
import time

# Enter your Tumblr API key here:
tumblr = pytumblr.TumblrRestClient('')

# Set search parameters here:
#
# Tumblr's API only supports searching for a single blog at a time
# Filter options are text, html, or raw
# Before - only search for posts before this time - in seconds past the epoch
# use calendar.timegm(time.gmtime()) to use the current epoch
blog_url = ''  # Tumblr blog URL (e.g., example.tumblr.com)
filter = 'text'
before = calendar.timegm(time.gmtime())

# Set output file here:
outputPath = ''

filePath = outputPath + 'TumblrPosts-' + str(before) + '-' + blog_url + '.csv'
with open(filePath, mode='a', newline='', encoding='utf-8') as results_file:
    results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    results_writer.writerow(["timeStamp", "URL", "blogName", "title", "tags", "body"])

print("Searching Tumblr for 100 posts from blog '" + blog_url + "'")

j = 1

# If you really wanted to, you could increase this number here to increase the number of batches
# Tumblr's API limits you to 20 results at a time, but we can loop through the search multiple times
# BUT I'd be cautious about making this number too big - to avoid running into API call limits

while j < 5:
    # Run the search and snag the results
    searchResults = tumblr.posts(blog_url, filter=filter, before=before, limit=20)
    print("Batch " + str(j) + " of 5")
    print(str(len(searchResults["posts"])) + " results retrieved")
    for post in searchResults["posts"]:
        blog_name = searchResults["blog"]["name"]
        date = post["date"]
        url = post["post_url"]

        try:
            title = post["title"]
        except KeyError:
            title = "Couldn't Get Title"
        try:
            tags = post["tags"]
        except KeyError:
            tags = "Couldn't Get tags"
        try:
            body = post["body"]
        except KeyError:
            body = "Couldn't Get Post Body"

        if body != "Couldn't Get Post Body":
            with open(filePath, mode='a', newline='', encoding='utf-8') as results_file:
                results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                try:
                    results_writer.writerow([date, url, blog_name, title, tags, body])
                    print("Successfully wrote row for post from " + date)
                except:
                    print("Error writing row")

    # Next, we make note of the oldest timestamp
    oldestTime = post["timestamp"]
    before = oldestTime
    j = j + 1

print("Finished!")
print("Saved CSV to " + filePath)
