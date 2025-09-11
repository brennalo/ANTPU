import os
import json
import hashlib
import hmac
from flask import Flask, request, abort
import google.genai as genai
import requests

app = Flask(__name__)

# --- Configuration ---
# You should set these as environment variables for security
# For testing, you can hardcode them.
# VERIFY_TOKEN = os.environ.get('WEBHOOK_VERIFY_TOKEN', 'your-secret-verify-token')
# APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET', 'your-facebook-app-secret')

VERIFY_TOKEN = '16antpu64'
APP_SECRET = '239b30c574977410db4f4e6e04e8ed0d'
ACCESS_TOKEN = "EAA0JBMtW6XMBPbvm4aNqvHfkrb6b7fLVY8oJ37z4Y4B4eCYEeZAVSijDis91gOZBMSZBvcpp9MsqlItHZArrt2kzV6PdcLk0LZAldmZB6MLwZBOBv9nogAHRP73UOk8e7Rpm4k13FmPl7nCPAhXB0L4IPaSIPROHdWp3MQEpWtdDSyrmzJjNVehqSTP7Bb7sE4ZBpAHTACcaMoJOb8OowDID6cRhw5HmlsPZCUQZDZD"

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # --- Webhook Verification ---
        # This is the initial setup challenge from the Facebook App Dashboard.
        if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == VERIFY_TOKEN:
            print("Webhook verified!")
            return request.args.get('hub.challenge'), 200
        else:
            # Respond with 403 Forbidden if tokens do not match.
            return 'Verification token mismatch', 403

    elif request.method == 'POST':
        # --- Handle Incoming Notifications ---
        # 1. Verify the request signature for security
        signature = request.headers.get('X-Hub-Signature-256', '')[7:]  # Remove 'sha256='
        expected_signature = hmac.new(
            bytes(APP_SECRET, 'latin-1'),
            msg=request.data,
            digestmod=hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            print("Signature verification failed!")
            abort(403)  # Use abort(403) for security reasons

        # 2. Parse the incoming data
        payload = request.get_json()
        print("Received payload:")
        print(json.dumps(payload, indent=2))

        # 3. Process the comment notification
        # The payload structure matches the examples you provided.
        for entry in payload.get('entry', []):
            for change in entry.get('changes', []):
                if change.get('field') == 'comments':
                    comment_data = change.get('value', {})
                    comment_id = comment_data.get('id')
                    from_data = comment_data.get('from', {})
                    # Extract the username from the 'from' object
                    username = from_data.get('username')
                    if not comment_id:  # Fallback for the other payload structure
                        comment_id = comment_data.get('comment_id')

                    media_id = comment_data.get('media', {}).get('id')
                    comment_text = comment_data.get('text', '')

                    print(f"New comment! ID: {comment_id}, on Media ID: {media_id}")
                    print(f"Text: '{comment_text}'")
                    print(f"username: '{username}'")
                    # Here you would trigger your reply logic
                    if username != 'ant_pu':
                        comment_by_ai = generate_comment_reply(comment_text, "")
                        reply_to_comment(ACCESS_TOKEN,comment_id, comment_by_ai)

        return 'EVENT_RECEIVED', 200

    else:
        # Method not allowed
        abort(405)

# --- Gemini API Configuration ---
def configure_gemini():
    """
    Configures the Gemini API with your API key.
    It's recommended to set your API key as an environment variable.
    """
    api_key = 'AIzaSyBey0QThM5OK_XqeeZvE_FFsH867Rk6WBY'
    #api_key = os.getenv("GOOGLE_API_KEY")  # safer than hardcoding
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it to your Google API key.")

    # Create a client instance instead of configure()
    client = genai.Client(api_key=api_key)
    return client


def generate_comment_reply(comment_text, post_caption):
    """
    Generates a contextual and friendly reply to an Instagram comment
    using the Gemini API.
    """
    try:
        client = configure_gemini()

        prompt = f"""
        You are a friendly and helpful social media manager for a restaurant brand.
        Your task is to reply to a user's comment on an Instagram post.

        **Instructions:**
        1. Be positive, friendly, and engaging.
        2. Keep the reply concise and natural, like a real person wrote it. Use emojis where appropriate.
        3. If the comment is a question, answer it helpfully based on the post's caption.
        4. If the comment is a compliment, thank the user warmly.
        5. If the comment is negative or spam, generate the specific text "IGNORE".
        6. Do not include hashtags in your reply.

        **Context:**
        - The Instagram Post Caption is: "{post_caption}"
        - The User's Comment is: "{comment_text}"

        **Your Reply:**
        """

        print(f"Generating AI reply for comment: '{comment_text}'...")
        response = client.models.generate_content(
            model="gemini-1.5-flash",  # or gemini-1.5-pro
            contents=prompt
        )

        reply_text = response.text.strip()

        if reply_text == "IGNORE":
            print("AI decided to ignore this comment.")
            return None

        return reply_text

    except Exception as e:
        print(f"An error occurred while generating response with Gemini: {e}")
        return None

def reply_to_comment2(comment_id, message):
    # This is a placeholder for the function that would use the Graph API
    # to post a reply to the comment.
    print(f"Replying to comment {comment_id} with message: '{message}'")
    # See Step 4 for the actual implementation.

def reply_to_comment(access_token, comment_id, message):
    # print(f"\n--- Replying to Comment ID: {comment_id} ---")
    print(f"Replying to comment {comment_id} with message: '{message}'")
    url = f"https://graph.facebook.com/v23.0/{comment_id}/replies"
    params = {
        'access_token': access_token,
        'message': message
    }

    response = requests.post(url, params=params)

    if response.status_code == 200:
        print("✅ Success! Reply posted.")
        return response.json()
    else:
        print("❌ Error posting reply:")
        print(response.json())
        return None

if __name__ == '__main__':
    # Use 0.0.0.0 to make it accessible on your network
    app.run(host='0.0.0.0', port=5000, debug=True)