from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser

# Your Google Client ID and Redirect URI
GOOGLE_CLIENT_ID = "1097287749447-6e9mfvfbdc3bknvh2guode8qlk4a63jh.apps.googleusercontent.com"
REDIRECT_URI = "http://localhost:8000/callback"
ACCESS_TOKEN = None

class OAuthRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global ACCESS_TOKEN

        # The user has signed in successfully with Google, and the callback is received.
        if self.path.startswith("/callback"):
            query_params = self.path.split("?")[1]
            params_dict = dict(param.split("=") for param in query_params.split("&"))
            ACCESS_TOKEN = params_dict.get("code", None)

            # Send a simple response back to the browser.
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>You can close this window now.</h1></body></html>")
            return

def start_server():
    server_address = ("localhost", 8000)
    httpd = HTTPServer(server_address, OAuthRequestHandler)

    # Open the browser to initiate the sign-in process
    webbrowser.open(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=email")

    # Wait for a request to be handled by the server
    httpd.handle_request()

if __name__ == "__main__":
    start_server()
