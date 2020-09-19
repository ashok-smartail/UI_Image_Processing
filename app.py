from flask import Flask, render_template, url_for, request, redirect
import os

app = Flask(__name__)


global imageState, imageIndex, imageList, numberOfImages, directory


class Directory():
	def __init__(self, dir_name, dir_files):
		self.dir_name = dir_name
		self.dir_files = dir_files

	def __str__(self):
		return self.dir_name + ' --> ' + str(self.dir_files)

def pass_directory(path, directory, all_files):
	list_ = []
	for x in os.listdir(path):
		file = path+'/'+str(x)
		if os.path.isfile(file):
			all_files.append(x)
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
	global imageList, directories
	directory = []
	all_files = []
	pass_directory("./static/s3_downloads", directory, all_files)
	directories = directory[:]
	imageList = all_files[:]
	return render_template('image-process.html', directory = directories, image = imageList[imageIndex], all_files = imageList)

@app.route('/next')
def next():
	global imageIndex
	imageIndex += 1
	try:
		image = imageList[imageIndex]
	except IndexError:
		imageIndex = 0
		image = imageList[imageIndex]
	return render_template('image-process.html', directory = directories, image = image, all_files = imageList)
	
@app.route('/previous')
def previous():
	global imageIndex
	imageIndex -= 1
	try:
		image = imageList[imageIndex]
	except IndexError:
		imageIndex = len(imageList) - 1
		image = imageList[imageIndex]
	return render_template('image-process.html', directory = directories, image = image, all_files = imageList)


@app.route('/left_rotate')
def left_rotate():
	print('left_rotate')
	return "left_rotate"

@app.route('/right_rotate')
def right_rotate():
	print('right_rotate')
	return "right_rotate"

if __name__ == '__main__':
	
	imageState , imageIndex , imageList, directory = 0 , 0 , list(), list()
	print(imageState , imageIndex , imageList, directory)
	numberOfImages = len(imageList)
	app.run(debug=True)