from flask import Flask

#tell flask where application is located
app = Flask(__name__)

@app.route('/')
def home():
    return 'IT IS WORKING'


if __name__ == '__main__':
    app.run(debug=True, port=5050)  # Use port 5050 or another free port

