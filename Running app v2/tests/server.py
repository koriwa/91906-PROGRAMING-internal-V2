# server.py

from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace this with your own client ID and redirect URI
GOOGLE_CLIENT_ID = "1097287749447-6e9mfvfbdc3bknvh2guode8qlk4a63jh.apps.googleusercontent.com"
REDIRECT_URI = "http://localhost:8000/callback"

# This variable will store the access token
access_token = None

@app.route("/callback")
def callback():
    global access_token
    code = request.args.get("code")
    if code:
        # You need to exchange the authorization code for an access token
        import requests
        data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        response = requests.post("https://oauth2.googleapis.com/token", data=data)
        if response.ok:
            access_token = response.json().get("access_token")

        # Close the sign_in_page after successful sign-in
        # This part is modified since we'll get the access token from the main code
        return "Successfully signed in! You can close this window now."
    else:
        return "Error: No authorization code received."

# New route to send the access token back to the main code
@app.route("/get_token")
def get_token():
    global access_token
    return access_token

if __name__ == "__main__":
    app.run(host="localhost", port=8000)
