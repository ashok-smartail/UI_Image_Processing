from flask import Flask, render_template, url_for, request, redirect, session
import os
import cv2

app = Flask(__name__)
app.secret_key = "image tool"

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
		session['username'] = 'smartail-ashok'
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
	n = len(imageList)
	progress = ((imageIndex + 1)*100) // n
	print(progress, imageIndex+1, len(imageList))
	return render_template('image-process.html', directory = directories, image = imageList[imageIndex], 
		all_files = imageList, progress = progress, i = imageIndex, n = n, username = session['username'])

@app.route('/next')
def next():
	global imageIndex
	imageIndex += 1
	try:
		image = imageList[imageIndex]
	except IndexError:
		imageIndex = 0
		image = imageList[imageIndex]
	return redirect('image-process')
	
@app.route('/previous')
def previous():
	global imageIndex
	imageIndex -= 1
	try:
		image = imageList[imageIndex]
	except IndexError:
		imageIndex = len(imageList) - 1
		image = imageList[imageIndex]
	return redirect('image-process')

@app.route('/left_rotate')
def left_rotate():
	base_dir = '/home/ashokubuntu/Desktop/smartailtool/UI_Image_Processing/static/s3_downloads/'
	image = imageList[imageIndex]
	complete_path = base_dir + str(image)
	# print(complete_path)
	img = cv2.imread(complete_path)
	# print(img)
	img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
	cv2.imwrite(complete_path, img)
	return redirect('image-process')

@app.route('/right_rotate')
def right_rotate():
	base_dir = '/home/ashokubuntu/Desktop/smartailtool/UI_Image_Processing/static/s3_downloads/'
	image = imageList[imageIndex]
	complete_path = base_dir + str(image)
	# print(complete_path)
	img = cv2.imread(complete_path)
	# print(img)
	img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
	cv2.imwrite(complete_path, img)
	return redirect('image-process')

@app.route('/crop/<data>')
def crop(data):
	base_dir = '/home/ashokubuntu/Desktop/smartailtool/UI_Image_Processing/static/s3_downloads/'
	x, y, w, h = map(int, data.split(','))
	image = imageList[imageIndex]
	complete_path = base_dir + str(image)
	img = cv2.imread(complete_path)
	img = img[y:y+h, x:x+w]
	cv2.imwrite(complete_path, img)

	return redirect(url_for('next'))


if __name__ == '__main__':	
	imageState , imageIndex , imageList , directory = 0, 0, list(), list()
	# print(imageState , imageIndex , imageList, directory)
	numberOfImages = len(imageList)
	app.run(debug=True)