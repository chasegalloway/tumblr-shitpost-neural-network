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

print("Searching Tumblr for blog posts from '" + blog_url + "'")

# Accept user input for the desired post count
post_count = int(input("Enter the number of blog posts to scrape: "))
remaining_posts = post_count

j = 1
post_bodies = []
total_posts = 0

while j < 16 and remaining_posts > 0:
    # Determine the number of posts to fetch in this batch
    limit = min(remaining_posts, 20)

    # Run the search and snag the results
    searchResults = tumblr.posts(blog_url, filter=filter, before=before, limit=limit)
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
            # Remove user's name from the beginning of the post body
            if body.startswith(blog_name + ":"):
                body = body[len(blog_name) + 1:].lstrip()

            with open(csvFilePath, mode='a', newline='', encoding='utf-8') as results_file:
                results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                try:
                    results_writer.writerow([date, url, blog_name, title, tags, body])
                    print("Successfully wrote row for post from " + date)
                    total_posts += 1
                    remaining_posts -= 1
                    post_bodies.append(body)
                except:
                    print("Error writing row")

        # Update the 'before' timestamp to fetch the next batch
        oldestTime = post['timestamp']
        before = oldestTime

    j += 1

print("Finished scraping " + str(total_posts) + " posts!")
print("Saved CSV to " + csvFilePath)

# Save the post bodies to a text file
with open(textFilePath, mode='w', encoding='utf-8') as text_file:
    for body in post_bodies:
        text_file.write(body + '\n')

print("Saved post bodies to " + textFilePath)
