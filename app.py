from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def get_logs():
    db = mysql.connector.connect(
        host="localhost",
        user="superiron",
        password="]zIiZHz-Hq8eHR2h",
        database="ironshield"
    )
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM logs ORDER BY fecha DESC LIMIT 50")
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

@app.route('/')
def dashboard():
    logs = get_logs()
    return render_template("index.html", logs=logs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
