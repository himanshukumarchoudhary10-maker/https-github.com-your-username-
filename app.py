from flask import Flask, render_template, request
from phone_details import get_phone_details

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/lookup", methods=["POST"])
def lookup():
    number = request.form.get("number", "")
    details = get_phone_details(number)
    return render_template("result.html", number=number, details=details)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
