from flask import Flask,render_template, request
app = Flask(__name__, template_folder='../vista',static_folder='../static')

@app.route('/')
def login():
    return render_template('comunes/login.html')

if __name__ == '__main__':
    app.run(debug=True)