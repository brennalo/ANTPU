import requests

ACCESS_TOKEN = "EAA0JBMtW6XMBPd1B1RwFAOpZCVP0gyKOrNbndZByiAN58AjZAyTaXqzkjYriVhX3NWXgRr39NNx9rmmwZCXi1Bec7kK4OOmWZAlJaV6HjsR9WySzorIw9veFlmjFvrtKBYIwIZAf82ym2ZB2WmVDwZCbtPMeCSjdgudCXAUSjpT92WxNYxZB40LUzL8ikrbaNEP1HUzk9bzZCZCPsjoZCypGQOnzyrKuqgWLeIAxF7ZCvlNZCkMlkZD"
PAGE_ID = "816523878201926"

url = f"https://graph.facebook.com/v23.0/{PAGE_ID}/feed?fields=id,comments"
params = {
    "access_token": ACCESS_TOKEN
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()

    for post in data.get("data", []):
        post_id = post.get("id")
        print(f"\nPost ID: {post_id}")

        comments = post.get("comments", {}).get("data", [])
        if comments:
            print("Comments:")
            for c in comments:
                comment_id = c.get("id")
                author = c.get("from", {}).get("name", "Unknown")
                message = c.get("message", "")
                created_time = c.get("created_time")

                print(f"  - Comment ID: {comment_id}")
                print(f"    From: {author}")
                print(f"    Time: {created_time}")
                print(f"    Message: {message}\n")
        else:
            print("No comments found.")
else:
    print("Error:", response.json())