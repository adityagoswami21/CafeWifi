from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)

@app.route('/')
def home():
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True, port=5002)
