import requests

ACCESS_TOKEN = "EAA0JBMtW6XMBPdkmyk9Ywn6DlTa33KfFyOZAfgQJ7Lca2cZCw5cAnTA4uvzBe54WTn2rxExLhsVse8mAJbehTZAPTUP8NkymjRdo7EZACiTo7Ap5kvtWAIFUzZA7o9UZBx5PcLqwWsvnkdqRCVYe5N2Ayim6N9BzjkvORBbaKaw3mxLtRTsF7zoy9bomDp7biPD1gffnCEZBJjF86OV1KRQAW8ZAzvuql7i1ugZDZD"
MEDIA_ID = "18043035302363677"
COMMENT_ID = "17906302152234147"

url = f"https://graph.facebook.com/v23.0/{MEDIA_ID}/comments"
params = {
    "access_token": ACCESS_TOKEN
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print("Comments:", data["data"])

    print(f"\nPost ID: {MEDIA_ID}")
    for post in data.get("data", []):
        comment_id = post.get("id")
        if comment_id:
            created_time = post.get("timestamp")
            message = post.get("text")

            print(f"  - Comment ID: {comment_id}")
            print(f"    Time: {created_time}")
            print(f"    Message: {message}\n")

        else:
            print("No comments found.")
else:
    print("Error:", response.json())


# def reply_to_comment(access_token, comment_id, message):
#     """
#     Posts a reply to a specific Instagram comment.
#
#     Args:
#         access_token (str): Your Meta Graph API access token.
#         comment_id (str): The ID of the comment you want to reply to.
#         message (str): The text of your reply.
#
#     Returns:
#         dict: The API response confirming the reply, or None on error.
#     """
#     print(f"\n--- Replying to Comment ID: {comment_id} ---")
#     url = f"https://graph.facebook.com/v23.0/{comment_id}/replies"
#     params = {
#         'access_token': access_token,
#         'message': message
#     }
#
#     response = requests.post(url, params=params)
#
#     if response.status_code == 200:
#         print("✅ Success! Reply posted.")
#         return response.json()
#     else:
#         print("❌ Error posting reply:")
#         print(response.json())
#         return None
#
#
# reply_message = "Thank you for your comment! We appreciate it."
# reply_response = reply_to_comment(ACCESS_TOKEN, COMMENT_ID, reply_message)
# if reply_response:
#     print("Reply Response:", reply_response)