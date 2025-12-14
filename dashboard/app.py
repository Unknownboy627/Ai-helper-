from flask import Flask, redirect, request, session, url_for, render_template
import requests
import os

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET", "dev")

DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")

DISCORD_API = "https://discord.com/api"

@app.route("/")
def home():
    user = session.get("user")
    return render_template("dashboard.html", user=user)

@app.route("/login")
def login():
    return redirect(
        f"{DISCORD_API}/oauth2/authorize"
        f"?client_id={DISCORD_CLIENT_ID}"
        f"&redirect_uri={DISCORD_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify email"
    )

@app.route("/login/callback")
def callback():
    code = request.args.get("code")

    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token = requests.post(
        f"{DISCORD_API}/oauth2/token",
        data=data,
        headers=headers
    ).json()

    user = requests.get(
        f"{DISCORD_API}/users/@me",
        headers={"Authorization": f"Bearer {token['access_token']}"}
    ).json()

    session["user"] = user
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
