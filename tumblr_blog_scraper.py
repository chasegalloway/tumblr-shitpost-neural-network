import pytumblr
import csv
import calendar
import time

# Enter your Tumblr API key here:
tumblr = pytumblr.TumblrRestClient('')

blog_url = ''  # Tumblr blog URL (e.g., example.tumblr.com)
filter = 'text'
before = calendar.timegm(time.gmtime())

# Set output file paths
csvFilePath = 'TumblrPosts-' + str(before) + '-' + blog_url + '.csv'
textFilePath = 'TumblrPosts-' + str(before) + '-' + blog_url + '.txt'

with open(csvFilePath, mode='a', newline='', encoding='utf-8') as results_file:
    results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    results_writer.writerow(["timeStamp", "URL", "blogName", "title", "tags", "body"])

print("Searching Tumblr for 300 posts from blog '" + blog_url + "'")

j = 1
post_bodies = []
total_posts = 0

while j < 16 and total_posts < 300:
    # Run the search and snag the results
    searchResults = tumblr.posts(blog_url, filter=filter, before=before, limit=20)
    print("Batch " + str(j) + " of 15")
    num_results = len(searchResults["posts"])
    print(str(num_results) + " results retrieved")

    if num_results == 0:
        break

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
            with open(csvFilePath, mode='a', newline='', encoding='utf-8') as results_file:
                results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                try:
                    results_writer.writerow([date, url, blog_name, title, tags, body])
                    print("Successfully wrote row for post from " + date)
                    total_posts += 1
                except:
                    print("Error writing row")

            post_bodies.append(body)

    # Next, we make note of the oldest timestamp
    oldestTime = post["timestamp"]
    before = oldestTime
    j = j + 1

print("Finished!")
print("Saved CSV to " + csvFilePath)

# Write post bodies to a text file
with open(textFilePath, mode='w', encoding='utf-8') as text_file:
    for body in post_bodies:
        text_file.write(body + '\n')

print("Saved post bodies to " + textFilePath)
