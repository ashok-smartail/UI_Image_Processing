from flask import Flask, render_template, url_for, request, redirect
import os

app = Flask(__name__)

class Directory():
	def __init__(self, dir_name, dir_files):
		self.dir_name = dir_name
		self.dir_files = dir_files

	def __str__(self):
		return self.dir_name + ' --> ' + str(self.dir_files)

def pass_directory(path, directory):
	list_ = []
	for x in os.listdir(path):
		file = path+'/'+str(x)
		if os.path.isfile(file):
			list_.append(x)
		elif os.path.isdir(file):
			pass_directory(file, list_)

	directory.append(Directory(path, list_))


@app.route('/', methods = ['GET', 'POST'])
def index():
	if request.method == "POST":
		return redirect('image-process')
	return render_template("index.html")

@app.route('/image-process')
def image():
	directory = []
	pass_directory("./static/s3_downloads", directory)
	
	return render_template('image-process.html', directory = directory)


if __name__ == '__main__':
	app.run(debug=True)