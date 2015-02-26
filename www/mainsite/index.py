from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
	return 'New Site is active!'

@app.route('/data')
def names():
	data = {"names": ["John", "Jacob", "Jingle-heimer", "Schmidt"]}
	return jsonify(data)

@app.route('/template')
def templated():
	return render_template('test.html')

if __name__ == '__main__':
	app.run()
