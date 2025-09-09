from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = 'ABC123'

@app.route('/webhook', methods=['GET'])
def webhook_connect():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print("✅ Webhook verified successfully.")
        return challenge, 200
    else:
        return '❌ Verification failed.', 403

@app.route('/webhook', methods=['POST'])       
def webhook_fetch():
    data = request.get_json()
    print("🔔 New Webhook Event Received:")
    print(data)
    return 'EVENT_RECEIVED', 200

if __name__ == '__main__':
    app.run(port=5000)
