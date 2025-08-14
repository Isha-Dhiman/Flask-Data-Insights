from flask import Flask, render_template, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

data_df = pd.DataFrame()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/pandas')
def pandas():
    global data_df
    data_df = pd.read_csv('airlines_flights_data.csv').head()
    return render_template("pandas.html",title="PANDAS",table=data_df.to_html(index=False, classes="table"))

@app.route('/bar')
def bar():
    if data_df.empty:
        return redirect('/pandas')
    plt.figure(figsize=(10,6))
    plt.bar(data_df['airline'],data_df['departure_time'])
    plt.grid(False)
    chart_path = os.path.join('static','chart.png')
    plt.savefig(chart_path)
    plt.close()

    return render_template('bar.html', chart_url = url_for('static', filename='chart.png'))

@app.route('/pie')
def pie():
    if data_df.empty:
        return redirect('/pandas')

    count = data_df['airline'].value_counts()

    plt.figure(figsize=(10,6))
    plt.pie(count.values, labels=count.index, autopct='%1.1f%%')
    plt.grid(False)

    chart_path = os.path.join('static', 'chart.png')
    plt.savefig(chart_path)
    plt.close()

    return render_template('pie.html', chart_url=url_for('static', filename='chart.png'))

if(__name__) == '__main__':
    app.run(port=3000,debug=True)

