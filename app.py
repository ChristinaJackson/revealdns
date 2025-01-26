from flask import Flask, render_template, request
from main import get_info

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/info', methods=['GET'])
def info():
    # Get the domain from the query parameter
    domain = request.args.get('domain')

    # Call your get_info function to fetch data
    data = get_info(domain)

    # Render the result page with the data
    return render_template('index.html', data=data)

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True, port=5050)
