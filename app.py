from flask import Flask, render_template, request, redirect
import os
import requests
from datetime import date,timedelta
from requests.auth import HTTPBasicAuth
import simplejson as json
import pandas as pd

from bokeh.plotting import figure,show
from bokeh.embed import components
from bokeh.util.string import encode_utf8

app = Flask(__name__)

@app.route('/index',methods=['GET','POST'])
def index2():
    if request.method=='GET':
        return render_template('request.html')
    else:
        ticker=request.form['ticker_symbol']

    start_date='2017-01-01'
    end_date='2017-12-31'
    url='https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?'
    my_api_key='Qj1qW5k3GsuLbUpvpsfZ'
    params = {'ticker':ticker,'api_key':my_api_key, 'qopts.columns':'date,close'}#, date.gte='20170101',date.lt='20171231'}
    quandl_data = requests.get(url,params=params)
    data_load = json.loads(quandl_data.content)
    df = pd.DataFrame(data_load['datatable']['data'])
    columns = []
    temp = data_load['datatable']['columns']
    for item in temp:
        columns.append(item['name'])
    df.columns=columns
    df.date = pd.to_datetime(df.date)
    df=df[(df.date > start_date) & (df.date <= end_date)]

#Create the Bokeh Plot
    p = figure(x_axis_type="datetime", title="2017 Daily Closing Prices")
    p.grid.grid_line_alpha=0.3
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.line(df.date, df.close, legend=ticker) #color='#A6CEE3')
    p.legend.location = "top_left"
    #p.show()
    script, div = components(p)
    return render_template("chart.html", div=div, script=script)

if __name__ == '__main__':
  app.run(port=33507,debug=True)
