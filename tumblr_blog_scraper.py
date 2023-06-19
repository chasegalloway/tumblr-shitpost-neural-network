import pytumblr
import csv
from unidecode import unidecode
import calendar
import time

# Enter your Tumblr API key here:
tumblr = pytumblr.TumblrRestClient('')

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
