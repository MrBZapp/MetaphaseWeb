from flask import Flask, jsonify, render_template

app = Flask(__name__)
@app.route('/')
def index():
	page_vars = {"active_page": "index"}
	base = app.jinja_env.get_template('index.html', globals=page_vars )
	#header = app.jinja_env.get_template('layout_header.html')
	#base = app.jinja_env.join_path(header, base)
	#base = app.jinja_env.join_path('layout_body.html', base)
	#base = app.jinja_env.join_path('layout_footer.html', base)
	#base = render_template('layout_header.html', title="home", bootstrap="TRUE")
	return render_template(base, title="home", bootstrap=True)

@app.route('/data')
def names():
	data = {"names": ["John", "Jacob", "Jingle-heimer", "Schmidt"]}
	return jsonify(data)

if __name__ == '__main__':
	app.run(debug=True)
