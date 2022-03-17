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


# Importing Modules
import pandas as pd
import matplotlib
import seaborn as sns
import io


if __name__ =='__main__':
    from PIL import Image

matplotlib.use('agg')

def regression_plot():
    df = pd.read_csv('app/data/tempYearly.csv')

    sns_plot = sns.regplot(x='Rainfall', y='Temperature', data=df)

    image = io.BytesIO()

    sns_plot.figure.savefig(image, format = 'png')

    image.seek(0)
    return image

if  __name__ == '__main__':
    image = regression_plot()
    im = Image.open(image)
    im.save('regress.png','PNG')
