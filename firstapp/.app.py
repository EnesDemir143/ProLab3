from flask import Flask,render_template
from Main import author_name


app = Flask(__name__,template_folder='templates')

@app.route('/')
def index():
    return render_template("index.html",author_name=author_name)

if __name__ == '__main__':
    app.run(host= '0.0.0.0',port=5555, debug=True)
