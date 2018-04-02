from flask import Flask, redirect, url_for, request, render_template
import Popularity
app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/')
def home():
	return render_template('Home.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route('/predict', methods= ['POST'])
def predict():
	return "<H1> Your News Article will be popular</H1>"



if __name__ == '__main__':
   app.run(debug = True)