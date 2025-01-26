from flask import Flask, request, jsonify, render_template
from main import get_info
#tell flask where application is located
app = Flask(__name__)


# @app.route('/info', methods=['GET'])

# def info_endpoint():
#     # Get the domain from the query string
#     domain = request.args.get('domain')
#     if not domain:
#         return jsonify({"error": "Domain parameter is required"}), 400
#
#     # Call get_info to handle everything
#     result = get_info(domain)
#
#     # Return the result as JSON
#     return jsonify(result)


# basic for stlying sake
@app.route('/')
def home():
    # Render the basic index.html page
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5050)
