from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
	return 'Push it real good... OR ELSE!'

@app.route('/data')
def names():
	data = {"names": ["John", "Jacob", "Jingle-heimer", "Schmidt"]}
	return jsonify(data)

@app.route('/template')
def templated():
	return render_template('test.html')

if __name__ == '__main__':
	app.run()
