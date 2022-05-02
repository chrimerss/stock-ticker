import time
from flask import Flask, request, render_template
from datetime import datetime
from pandas import DataFrame
import pandas as pd
from tickerstats_yf import build_headline,\
                           get_all_stocks,\
                           build_df,\
                           indices_dict,\
                            currency_dict,\
                            minutes_between_updates,\
                           get_ticker_symbols
symbols=open('watchlist.txt').read().splitlines()
app  = Flask(__name__)

def _sleep(minutes):
    time.sleep(minutes*60)

def _highlight_greaterthan(s):
    if s.name in ['CHANGE%','LOW52%',
                    'HIGH52%','MA50%',
                    'MA200%']:
        

        return ['background-color: green' if v>=0 else 'background-color: red' for v in s]
    else:
        return ['background-color: white' for v in s]

def _highlight_greaterthan(cell):
    return 'color: ' + ('red' if cell <0 else 'green')

@app.route("/")
def main():

#   symbol = request.args.get('symbol', default="AAPL")
    # symbols = get_ticker_symbols()
    first=True
    while True:
        index_headline = build_headline(indices_dict)
        currency_headline = build_headline(currency_dict)
        stocks = get_all_stocks(symbols)
        dataframe = build_df(stocks)
        # df_styles= dataframe.apply(_highlight_greaterthan, axis=0)
        df_html = dataframe.style.applymap(_highlight_greaterthan,
         subset=['CHANGE%','LOW52%','HIGH52%','MA50%','MA200%']).format(precision=2).render()
        # df_html = styles.render()
        # print(dataframe)
        # os.system('cls||clear')
        # print('\n' + index_headline)
        # print(currency_headline + '\n')
        # print(dataframe)
        # print('\n updated: ' + datetime.now().strftime('%H:%M:%S'))
        if not first:
            _sleep(1*60)
            first=False

        return render_template('index.html',
                             tables=[df_html],
                             titles=dataframe.columns.values,
                             time=datetime.now().strftime('%Y-%m-%d %H:%M'))

if __name__ == "__main__":
  app.run(debug=True)