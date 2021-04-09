from altair.vegalite.v4.schema.core import Step
import yfinance as yf
import streamlit as st
import wealthsimple
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ta

def format_number(number):
    return f"{number:,}"


st.sidebar.write("Navigation")
screen = st.sidebar.selectbox("View",("Overview","Fundamentals","Wealthsimple","Stock Compare","Technical Analysis"))
st.title(screen)
symbol = st.sidebar.text_input("Symbol",value="AAPL")
ticker = yf.Ticker(symbol)

if screen == "Overview":
    col1,col2 = st.beta_columns([1,4])
    with col1:
        st.image(ticker.info.get('logo_url'))
    with col2:
        st.subheader(ticker.info.get('longName'))  
        st.subheader("Industry")
        st.write(ticker.info.get('industry'))
        st.subheader("Traded Exchange")
        st.write(ticker.info.get('exchange'))
        st.write(ticker.info.get('market'))
        st.subheader("Summary")
        with st.beta_expander(label="Expand", expanded=False):
            st.write(ticker.info.get('longBusinessSummary'))

if screen == "Fundamentals":
    st.subheader(ticker.info.get('longName'))  
    col1,col2,col3 = st.beta_columns(3)
    with col1:
        st.header("Basic Values")
        st.subheader("Market Cap")
        if ticker.info.get('marketCap') is not None:
            st.write(format_number(ticker.info.get('marketCap')))
        else:
            st.write("No Value")

        st.subheader("EPS")
        if ticker.info.get('trailingEps') is not None:
            st.write(format_number(ticker.info.get('trailingEps')))
        else:
            st.write("No Value")

        st.subheader("Dividend")
        if ticker.info.get('dividendRate') is not None:
            st.write(format_number(ticker.info.get('dividendRate')))
        else:
            st.write('No Value')

        st.subheader("Volume")
        if ticker.info.get('volume') is not None:
            st.write(format_number(ticker.info.get('volume')))
        else:
            st.write('No Value')
    
        st.subheader("P/E Ratio")
        if ticker.info.get('trailingPE') is not None:
            st.write(format_number(ticker.info.get('trailingPE')))
        else:
            st.write('No Value')

    with col2:
        st.header("Prices")
        st.subheader("Yesterday's Price")    
        yest = ticker.info.get('previousClose')
        st.write(format_number(yest))

        st.subheader("Opening Price")    
        open = ticker.info.get('regularMarketOpen')
        st.write(format_number(open))

        st.subheader("Closing Price")
        close = ticker.info.get('regularMarketPrice')
        st.write(format_number(open))

        st.subheader("% Change")
        change = (close - yest)/(yest)*100
        st.write(format_number(change))

        st.subheader("Day High/Low")
        st.write(ticker.info.get('dayLow'),"/",ticker.info.get('dayHigh'))

    with col3:
        st.header("Fun Stats")

        st.subheader("Shorted Shares")
        if ticker.info.get('sharesShort') is not None:
            st.write(format_number(ticker.info.get('sharesShort')))
        else:
            st.write('No Value')

        st.subheader("Shorted Ratio")
        if ticker.info.get('shortRatio') is not None:
            st.write(format_number(ticker.info.get('shortRatio')))
        else:
            st.write('No Value')
        
        st.subheader("200 Day Average")
        if ticker.info.get('twoHundredDayAverage') is not None:
            st.write(format_number(ticker.info.get('twoHundredDayAverage')))
        else:
            st.write('No Value')

        st.subheader("50 Day Average")
        if ticker.info.get('fiftyDayAverage') is not None:
            st.write(format_number(ticker.info.get('fiftyDayAverage')))
        else:
            st.write('No Value')

        st.subheader("Beta")
        if ticker.info.get('beta') is not None:
            st.write(format_number(ticker.info.get('beta')))
        else:
            st.write('No Value')

        st.subheader("PEG Ratio")
        if ticker.info.get('pegRatio') is not None:
            st.write(format_number(ticker.info.get('pegRatio')))
        else:
            st.write('No Value')
            
    time_period = st.selectbox("Select Timeframe",("1d","5d","1mo","3mo","6mo","1y","2y","5y", "10y", "ytd","max"))
    if time_period == "1d" or "5d" or "1mo":
        interval =  st.selectbox("Select Interval",("1m","2m","5m","15m","30m","60m","90m","1h","1d","5d","1wk"))
    else: 
        interval =  st.selectbox("Select Interval",("1d","5d","1wk","1mo","3mo"))

    df = pd.DataFrame(ticker.history(period=time_period,interval=interval))
    st.line_chart(data=df['Close'], width=0, height=0, use_container_width=True)


# if screen == "Wealthsimple":
#     email = st.text_input("Enter Email")
#     password = st.text_input("Enter Password",type="password")
#     tfa = st.text_input("Enter 2FA code:")

#     try:
#         def my_two_factor_function():
#             MFACode = tfa
#             return MFACode

#         ws = wealthsimple.WSTrade(
#             email,
#             password,
#             two_factor_callback=my_two_factor_function,
#         )
#     except:
#         pass
#     else:
#         st.header("Wealthsimple info")
#         st.subheader("Positions")
#         #st.write(ws.get_account_ids())
#         #st.write(ws.get_account("tfsa-gjcsjvzu"))

#         positions = ws.get_positions("tfsa-gjcsjvzu")
#         # st.write(positions[0])

#         stock_vals = {}
#         stock_name = []
#         symbols = []
#         avg_daily_vol = []
#         stock_country = []
#         exchange = []
#         old_value = []
#         currency = []
#         quantity = []
#         closing_price = []
#         daily_high = []
#         daily_low = []
#         daily_vol = []

#         for i in range(len(positions)):
#             stock_name.append(positions[i]['stock']['name'])
#             symbols.append(positions[i]['stock']['symbol'])
#             stock_country.append(positions[i]['stock']['country_of_issue'])
#             exchange.append(positions[i]['stock']['primary_exchange'])
#             currency.append(positions[i]['market_book_value']['currency'])
#             old_value.append(positions[i]['market_book_value']['amount'])
#             quantity.append(float(positions[i]['quantity']))
#             closing_price.append(float(positions[i]['quote']['amount']))
#             daily_high.append(positions[i]['quote']['high'])
#             daily_low.append(positions[i]['quote']['low'])
#             avg_daily_vol.append(positions[i]['stock']['avg_daily_volume_last_month'])
#             daily_vol.append(positions[i]['quote']['volume'])

#         today_value = []
#         for num1, num2 in zip(quantity, closing_price):
#     	    today_value.append(num1 * num2)


#         stock_vals["Name"] = stock_name
#         stock_vals["Symbol"] = symbols
#         stock_vals["Country"] = stock_country
#         stock_vals["Exchange"] = exchange
#         stock_vals["Currency"] = currency
#         stock_vals["Value At Buy"] = old_value
#         stock_vals["Value Today"] = today_value
#         stock_vals["Quantity"] = quantity
#         stock_vals["Closing Price"] = closing_price
#         stock_vals["Daily High"] = daily_high
#         stock_vals["Daily Low"] = daily_low
#         stock_vals["Average Daily Volume"] = avg_daily_vol
#         stock_vals["Daily Volume"] = daily_vol

#         portfolio = pd.DataFrame(stock_vals)
#         st.write(portfolio)

#         st.subheader("Portfolio Breakdown")
#         # show_chart = st.selectbox("select stock", symbols)
#         fig, ax = plt.subplots()
#         ax = plt.pie(today_value, labels = symbols, autopct='%1.1f%%')
#         st.pyplot(fig)

#         # st.write("Deposits")
#         # st.write(ws.get_deposits())
#         st.header("History")
#         portfolio_amount = {}
#         history = []
#         dates = []
#         historical_vals = ws.get_account_history("tfsa-gjcsjvzu")["results"]
#         for i in range(len(historical_vals)):
#             history.append(historical_vals[i]["value"]['amount'])
#             dates.append(historical_vals[i]["date"])

#         portfolio_amount["Date"] = dates
#         portfolio_amount["Value"] = history
        
#         performance = pd.DataFrame(portfolio_amount)
#         # st.write(performance)
#         st.line_chart(data=performance, width=0, height=0, use_container_width=True)
#         # st.write("Get activities")
#         # st.write(ws.get_activities())

if screen == "Stock Compare":
    col1,col2,col3,col4,col5 = st.beta_columns(5)
    with col1:
        symbol1 = st.text_input("Symbol 1",value = "AAPL",max_chars=10)
    with col2:
        symbol2 = st.text_input("Symbol 2", value = "MSFT",max_chars=10)
    with col3:
        symbol3 = st.text_input("Symbol 3", value = "TSLA",max_chars=10)
    with col4:
        symbol4 = st.text_input("Symbol 4", value = "AMZN",max_chars=10)
    with col5:
        symbol5 = st.text_input("Symbol 5",value = "GOOG",max_chars=10)

    start = st.date_input("Select Start Date")
    end = st.date_input("Select End Date")

    data = (yf.download(f"{symbol1} {symbol2} {symbol3} {symbol4} {symbol5}", start=start, end=end))
    # st.write(data)
    st.line_chart(data=data['Close'], width=0, height=0, use_container_width=True)

    # df = pd.DataFrame(ticker.history(period=time_period,interval=interval))
    # st.line_chart(data=df['Close'], width=0, height=0, use_container_width=True)

# if screen == "Technical Analysis":

    
