import requests

ACCESS_TOKEN = "EAA0JBMtW6XMBPSUQpjk4P7gZBFlQfLMu9PeugTB2ZCUqkviLOQi99ZBy658goYXZBZCeWkGNxGXSDC8LjQrGnnJ0ooah3gO0KRpoMqgzXDeSQBvdTobUgobMjOMDCqij8IzBBsUnHeVvhTS5GozHZC0q0dRM97FIohmmkZCk8PcJqhLrqmX95joeji5fiU08JE7mJogoJGiXZC2inuaLWojM6ouUpw6JITysAoT2FfA4ZCzEZD"
PAGE_ID = "816523878201926"
COMMENT_ID = "122101141335006309_555703980942364"


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


def reply_to_comment(access_token, comment_id, message):
    print(f"\n--- Replying to Comment ID: {comment_id} ---")

    url = f"https://graph.facebook.com/v23.0/{comment_id}/comments"  # Use stable Graph API version

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    data = {
        'message': message
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print("✅ Success! Reply posted.")
        return response.json()
    else:
        print("❌ Error posting reply:")
        try:
            print(response.json())
        except Exception as e:
            print(f"Unexpected error: {e}")
            print(response.text)
        return None

reply_message = "Thank you for your comment! We appreciate it."
reply_response = reply_to_comment(ACCESS_TOKEN, COMMENT_ID, reply_message)

if reply_response:
    print("Reply Response:", reply_response)

