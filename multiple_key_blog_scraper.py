import pytumblr
import csv
import calendar
import time

# Enter your Tumblr API keys here:
api_keys = ['']  # Add more keys as needed

blog_url = ''  # Tumblr blog URL (e.g., example.tumblr.com)
filter = 'text'

# Set output file paths
csvFilePath = 'TumblrPosts-' + blog_url + '.csv'
textFilePath = 'TumblrPosts-' + blog_url + '.txt'

with open(csvFilePath, mode='a', newline='', encoding='utf-8') as results_file:
    results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    results_writer.writerow(["timeStamp", "URL", "blogName", "title", "tags", "body"])

print("Searching Tumblr for blog posts from '" + blog_url + "'")

# Fetch posts until there are no more left
before = calendar.timegm(time.gmtime())
total_posts = 0
post_bodies = []
key_index = 0  # Current API key index
remaining_api_calls = 500  # Number of API calls allowed per key

while True:
    # Get the current API key
    api_key = api_keys[key_index]

    # Create a TumblrRestClient instance with the current API key
    tumblr = pytumblr.TumblrRestClient(api_key)

    # Run the search and snag the results
    searchResults = tumblr.posts(blog_url, filter=filter, before=before)
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
                    post_bodies.append(body)
                except:
                    print("Error writing row")

        # Update the 'before' timestamp to fetch the next batch
        oldestTime = post['timestamp']
        before = oldestTime

        remaining_api_calls -= 1

        # Switch to the next API key if the current one reaches the limit
        if remaining_api_calls <= 0:
            key_index = (key_index + 1) % len(api_keys)
            remaining_api_calls = 500

print("Finished scraping " + str(total_posts) + " posts!")
print("Saved CSV to " + csvFilePath)

# Save the post bodies to a text file
with open(textFilePath, mode='w', encoding='utf-8') as text_file:
    for body in post_bodies:
        text_file.write(body + '\n')

print("Saved post bodies to " + textFilePath)
