from flask import Blueprint
from flask import render_template, request
from flask import url_for, current_app
from flask import send_file, Response
from flask import after_this_request
import os
import zipfile
main = Blueprint('main', __name__)
import shutil



@main.route('/')
@main.route('/home')
def home():
	return render_template('home.html')


# @main.route('/downloads')
# def downloads():
#
# 	ziptidefile =os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'out', 'tide.zip'))
# 	zipbcfile = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'out', 'bc.zip'))
# 	zipextfile = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'out', 'ext.zip'))
# 	allzips = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'out', 'all.zip'))
# 	with zipfile.ZipFile(allzips, 'w') as zf:
# 		fullpath = ziptidefile
# 		zf.write(fullpath, os.path.basename(fullpath))
# 		fullpath = zipbcfile
# 		zf.write(fullpath, os.path.basename(fullpath))
# 		fullpath = zipextfile
# 		zf.write(fullpath, os.path.basename(fullpath))
#
# 	@after_this_request
# 	def remove_file(response):
# 		outdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'out'))
# 		shutil.rmtree(outdir)
# 		print('removed output directory', outdir)
# 		return response
#
#
# 	return send_file(allzips, attachment_filename='downloads.zip', as_attachment=True)


