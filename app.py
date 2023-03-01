from flask import Flask, render_template, request
app = Flask(__name__)
 
 
@app.route('/')
def index():
    return "Welcome to Procurement Tracking System"
 
 
if __name__ == '__main__':
    app.run()
