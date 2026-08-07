from flask import Flask, jsonify
import socket, os
app=Flask(__name__)
APP_VERSION=os.environ.get("APP_VERSION","1.0.0")
@app.get("/")
def home():
    return jsonify(message="Hello from the Flask CI/CD Kubernetes pipeline!",
                   version=APP_VERSION,
                   hostname=socket.gethostname())
@app.get("/health")
def health():
    return jsonify(status="healthy"),200
if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)
