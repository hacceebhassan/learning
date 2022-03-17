#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
   Experiment with Docker
'''

# Ownership
__author__ = ["M. Haseeb Hassan"]
__copyright__ = ["Copyrights @ hacceebhassan"]
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "M. Haseeb Hassan"
__email__ = "hacceebhassan@gmail.com"
__status__ = "Development"

from flask import Flask, send_file
from plotdata import regression_plot

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def regr_plot():
    image = regression_plot()

    return send_file(image,
    attachment_filename = 'regplot.png',
    mimetype = 'image/png' )

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = False)

