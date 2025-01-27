from flask import Flask, render_template, request
from main import get_info

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    # Initial load without any data or error
    return render_template("index.html", data={}, error_message=None)

@app.route("/info", methods=["GET"])
def info():
    data = {}
    error_message = None

    # Get the domain from the query parameter
    domain_name = request.args.get("domain")
    if domain_name:
        try:
            data = get_info(domain_name) or {}
        except Exception as e:
            error_message = str(e)
    else:
        error_message = "Please provide a valid domain."

    return render_template("index.html", data=data, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True, port=5050)
