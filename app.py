from flask import Flask, render_template, request
from main import get_info

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/info', methods=['GET'])
def info():
    domain = request.args.get('domain')
    data = None
    error_message = None

    if domain:
        data = get_info(domain)  # Get results only if domain is not empty
    else:
        error_message = "Please enter a valid domain."

    return render_template('index.html', data=data, error_message=error_message)

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True, port=5050)
