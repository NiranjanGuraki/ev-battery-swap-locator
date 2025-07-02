# Final Flask app code for EV Battery Swap Station Locator
from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("query")
    conn = get_db_connection()
    stations = conn.execute("SELECT * FROM stations WHERE city LIKE ? OR pincode LIKE ?", 
                            (f"%{query}%", f"%{query}%")).fetchall()
    conn.close()
    return jsonify([dict(s) for s in stations])

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                            (username, password)).fetchone()
        conn.close()
        if user:
            session["user_id"] = user["id"]
            return redirect("/")
        return "Invalid credentials", 401
    return render_template("login.html")

@app.route("/favorite", methods=["POST"])
def favorite():
    if "user_id" not in session:
        return redirect("/login")
    station_id = request.form["station_id"]
    user_id = session["user_id"]
    conn = get_db_connection()
    conn.execute("INSERT INTO favorites (user_id, station_id) VALUES (?, ?)", (user_id, station_id))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/favorites")
def favorites():
    if "user_id" not in session:
        return redirect("/login")
    conn = get_db_connection()
    stations = conn.execute("""
        SELECT s.id, s.name, s.address, s.battery_types FROM stations s
        JOIN favorites f ON s.id = f.station_id
        WHERE f.user_id = ?
    """, (session["user_id"],)).fetchall()
    conn.close()
    return render_template("favorites.html", stations=stations)

if __name__ == "__main__":
    app.run(debug=True)
