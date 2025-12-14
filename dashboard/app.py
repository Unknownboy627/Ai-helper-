from flask import Flask, render_template, redirect, session
from flask_session import Session
import os

app = Flask(__name__)

# REQUIRED FOR RAILWAY
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "super-secret-key")
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

Session(app)

@app.route("/")
def home():
    if session.get("user"):
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/login")
def login():
    DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
    REDIRECT_URI = "https://ai-helper-production-1db8.up.railway.app/callback"

    discord_url = (
        "https://discord.com/api/oauth2/authorize"
        f"?client_id={DISCORD_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&response_type=code"
        "&scope=identify"
    )
    return redirect(discord_url)

@app.route("/callback")
def callback():
    # TEMP LOGIN (PROOF IT WORKS)
    session["user"] = {
        "username": "Andrew",
        "id": "123456"
    }
    return redirect("/loading")

@app.route("/loading")
def loading():
    return render_template("loading.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect("/")
    return render_template("dashboard.html", user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run() 
