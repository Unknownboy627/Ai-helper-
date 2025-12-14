from flask import Flask, render_template

app = Flask(__name__)

# ===== HOME / DASHBOARD =====
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

# ===== START SERVER =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
