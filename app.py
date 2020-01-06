from flask import Flask, render_template, request, redirect

import os
import requests
from datetime import date,timedelta
from requests.auth import HTTPBasicAuth
import simplejson as json
import pandas as pd

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.util.string import encode_utf8

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(port=33507)

#start_date='2017-01-01'
#end_date='2017-12-31'
url='https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?'
ticker = 'GOOGL'
my_api_key='Qj1qW5k3GsuLbUpvpsfZ'
payload = {'ticker':ticker,'api_key':my_api_key}#, date.gte='20170101',date.lt='20171231'}


quandl_data = requests.get(url,params=payload)
stock_load = json.loads(quandl_data.content)
df = pd.DataFrame(stock_load['datatable']['data'])
columns = []
temp = stock_load['datatable']['columns']
for item in temp:
    columns.append(item['name'])
df.columns=columns
df.date = pd.to_datetime(df.date)
#df=df[(df.date > start_date) & (df.date <= end_date)]
print(df)
