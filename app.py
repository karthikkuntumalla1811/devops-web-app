
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Welcome to DevOps Web Application!</h1>
    <h2>Version: 1.0</h2>
    <h2>Environment: Development</h2>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
