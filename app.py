from flask import Flask, render_template, request
app = Flask(__name__)
 
 
@app.route('/')
def index():
    return "Welcome to Procurement Tracking System. You can track your shipments here."
 
 
if __name__ == '__main__':
    app.run()
