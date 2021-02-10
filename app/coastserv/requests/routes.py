from flask import render_template, url_for, flash, redirect, abort, current_app, request
from coastserv import db
from coastserv.requests.forms import RequestForm
from coastserv.models.model import Model
from coastserv.models.query import Query
from coastserv.models.tide import Tide
from coastserv.models.boundary import Boundary
from coastserv.models.units.units import usefor
from flask import after_this_request
from flask import send_file, Response
from flask import session
import shutil

import os
import json
import numpy as np
import pandas as pd
import coastserv.models.utils as utils
from flask import Blueprint
from azure.storage.file import FileService
import zipfile

# file_service = FileService(account_name='coastservstorage', account_key='HOBOcLV1nEDevDKfHMVq9N0TsgNrh4AXI2Qyxt4QAmvDi+oSUD9R6xnI8UEz7AVduzMill3+ymlNlj11jC58vw==')
# generator = file_service.list_directories_and_files('static')
# for file_or_dir in generator:
#     print(file_or_dir.name)


requests = Blueprint('requests', __name__)

@requests.route('/request', methods = ['GET', 'POST'])
def new_request():
	
	form = RequestForm()

	if form.validate_on_submit():
		flash('Form was deemed valid', 'success')

		name = form.name.data

		tstart = form.tstart.data
		tend = form.tend.data
		tref = form.tref.data
		xmin = form.xmin.data
		xmax = form.xmax.data
		ymin = form.ymin.data
		ymax = form.ymax.data

		username = form.username.data
		password = form.password.data
		dataset  = form.dataset.data

		pli_file = utils.save_pli_file(os.path.join(current_app.root_path, 'static','pli_files'), form.pli_file.data)

		model = Model(name = name, tstart = tstart, tend = tend , tref = tref, xmin= xmin, xmax = xmax, ymin = ymin, ymax = ymax, pli_file = pli_file, dataset = dataset, user = username)

		db.session.add(model)
		db.session.commit()

		# prepare for sending via url
		coords      = str([xmin, xmax, ymin, ymax])
		time_vect   = {"t_start" : tstart, "t_end" : tend}
		time_vect   = json.dumps(time_vect)
		credentials = {"user" : username, "pwd" : password}
		credentials = json.dumps(credentials)

		return redirect(url_for('requests.processing_query', name = name, time_vect = time_vect, tref = tref, dataset = dataset, coords = coords, pli_file = pli_file, credentials = credentials))

		
	return render_template('new_request.html', title = 'New Request', form = form, legend = 'New Request')


@requests.route('/processing_query', methods = ['GET', 'POST'])
def processing_query():
	'''
	for display/feedback purposes only
	'''
	name     = request.args.get('name')
	tref     = request.args.get('tref')
	dataset  = request.args.get('dataset')
	pli_file = request.args.get('pli_file')

	credentials = request.args.get('credentials') 
	time_vect   = request.args.get('time_vect')
	coords      = request.args.get('coords')

	return render_template('processing_query.html', name = name, time_vect = time_vect, tref = tref, dataset = dataset, coords = coords, pli_file = pli_file, credentials = credentials, legend = 'Processing Query')


@requests.route('/process', methods = ['GET', 'POST'])
def process():
	name     = request.args.get('name')
	# print(name)
	out = os.path.join(current_app.root_path, 'static', 'out')
	if not os.path.exists(out):
		os.mkdir(out)
	out = os.path.join(current_app.root_path, 'static','out', name)
	if not os.path.exists(out):
		os.mkdir(out)

	tref     = request.args.get('tref')
	dataset  = request.args.get('dataset')
	pli_file = request.args.get('pli_file')

	credentials = json.loads(request.args.get('credentials')) 
	time_vect = json.loads(request.args.get('time_vect'))
	coords = request.args.get('coords').replace('[','').replace(']','').split(',')
	coords = np.array(coords, dtype = np.float64)

	mod_query = Query(time_vect, dataset, coords, credentials, out)
	mod_query.build_query()

	fes_path = os.path.abspath(os.path.join(current_app.root_path, 'static', 'FES'))
	# file_service = FileService(account_name='coastservstorage',
	# 						   account_key='HOBOcLV1nEDevDKfHMVq9N0TsgNrh4AXI2Qyxt4QAmvDi+oSUD9R6xnI8UEz7AVduzMill3+ymlNlj11jC58vw==')
	# generator = file_service.list_directories_and_files('static/FES')
	# print('****************8testprinting848484848********************')
	# for file_or_dir in generator:
	# 	if file_or_dir.name == 'FES':
	# 		# fes_path3=file_or_dir.name
	# 		print(file_or_dir, file_or_dir.name)
	# 		# file_service.get_file_to_path('static/FES', None, file_or_dir.name, 'out.nc')
	mod_tide = Tide(fes_path, coords, pli_file, out)
	
	ext = mod_tide.ext
	data_list = os.path.join(out, 'data', '*.nc')
	
	# convert from CMEMS parameter names to DFM names

	CMEMS_subs = mod_query.all_subs[dataset]
	sub_list = []
	for sub in usefor.keys():
		if usefor[sub]['substance'][0] in CMEMS_subs:
			sub_list.append(sub)

	tref       = pd.Timestamp(tref).to_pydatetime()
	model_dir  = mod_tide.out
	mod_bound  = Boundary(ext, data_list, sub_list, tref, model_dir)

	return render_template('process.html', query = mod_query, tide = mod_tide, model = mod_bound, legend = 'Processing Query')

@requests.route('/downloads', methods = ['GET', 'POST'])
def downloads():

	ziptidefile =os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'out', 'tide.zip'))
	zipbcfile = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'out', 'bc.zip'))
	zipextfile = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'out', 'ext.zip'))
	allzips = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'out', 'all.zip'))
	with zipfile.ZipFile(allzips, 'w') as zf:
		fullpath = ziptidefile
		zf.write(fullpath, os.path.basename(fullpath))
		fullpath = zipbcfile
		zf.write(fullpath, os.path.basename(fullpath))
		fullpath = zipextfile
		zf.write(fullpath, os.path.basename(fullpath))

	@after_this_request
	def remove_file(response):
		outdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'out'))
		os.remove(ziptidefile)
		os.remove(zipbcfile)
		os.remove(zipextfile)
		os.remove(allzips)
		shutil.rmtree(outdir)
		session.clear()


		return response


	return send_file(allzips, attachment_filename='downloads.zip', as_attachment=True)
