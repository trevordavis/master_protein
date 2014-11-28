#!/usr/bin/env python
# flask app for master
#
# takes a post like so:
# curl -F query="hiii this is a test" -F query_file=@"bc-30-sc-correct-20141022/ad/1adu_A.pds" http://localhost:5000/api/search

from flask import Flask, jsonify, request, render_template
from flask import redirect, url_for, send_from_directory
from MasterSearch import *

app = Flask(__name__)
masterSearch = MasterSearch()

# some config vars
ALLOWED_EXTENSIONS = frozenset(['pdb', 'pds'])
ALLOWED_ARGS = frozenset(['bbRMSD', 'dEps', 'ddZScore',
    'matchInFile', 'matchOutFile', 'phiEps', 'psiEps',
    'query', 'rmsdCut', 'rmsdMode', 'seqOutFile', 'structOut',
    'structOutType', 'target', 'targetList', 'topN', 'tune'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def allowed_args(list_of_args):
    # checks if list is allowed
    # returns: (bool isAllowed, listOfNotAllowed)
    argset = set(list_of_args)
    issubset = argset <= ALLOWED_ARGS
    intersection = argset - ALLOWED_ARGS
    return issubset, intersection

# routes
@app.after_request
def after(response):
    return response

# default web route just returns an intro page
@app.route("/", methods=['GET', 'OPTIONS'])
def hello():
    return render_template('index.html')

# api route for submitting a search
@app.route("/api/search", methods=['POST', 'OPTIONS'])
def search():

    # check args
    (is_allowed, not_allowed_list) = allowed_args(request.form)
    if not is_allowed:
        return jsonify({'error': 'bad parameters: ' + ', '.join(not_allowed_list)})

    # check query file
    if len(request.files) == 1 and 'query_file' in request.files:
        query_file = request.files['query_file']
        if allowed_file(query_file.filename):
            print("found query_file: " + str(query_file))
        else:
            return jsonify({'error': 'bad query file!'}), 201
    else:
        return jsonify({'error': 'no query file!'}), 201

    results = masterSearch.process(query_file, request.form)
    return jsonify({'results': results}), 201
    # return redirect(url_for('uploaded_file',
    #                         filename=filename))

# an image, that image is going to be show after the upload
@app.route('/api/search/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



if __name__ == "__main__":
  app.run(debug=True)
  #app.run()
