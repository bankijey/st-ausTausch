import streamlit as st
# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.utils import executor
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from binance.client import Client
from binance.enums import *
import config


# Initialize the bot and dispatcher
def send_message_to_bot(message):
    # Replace 'YOUR_BOT_TOKEN' with the token of the first bot
    bot_token = '5016947449:AAHTi1p_XeLpA0K3WZ2ASvxjdE8izPEmG70'
    bot_chat_id = 1233695002

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {'chat_id': bot_chat_id, 'text': message}
    response = requests.post(url, params=params)
    st.write(response.json())




st.sidebar.title("Input parameters")

amount = st.sidebar.number_input(
    "Euro exchange amount",
    value = 100.0,
    min_value=1.0,
    step = 50.0,
    format="%.2f")

requested = st.sidebar.number_input(
    "Enter requested rate (₦)",
    value = 915.0,
    min_value=1.0,
    step=5.0,
    format="%.2f")

amount_ngn = st.sidebar.number_input(
    "Naira exchange amount",
    value = amount*requested,
    min_value=1.0,
    step = 1.0,
    format="%.2f")


p2p_usd = st.sidebar.number_input(
    "Enter binance USDT P2P rate (₦)",
    value = 900.0,
    min_value=1.0,
    step=1.0,
    format="%.2f")

submit = st.sidebar.button(
    label = 'Submit'
)


if submit:
    send_message_to_bot(f"ST Submited {amount}, {requested}")
    
request_ngn = amount*requested

def get_bin_spot():# API calls
    eurusdt = st.sidebar.number_input(
    "EURUSDT exchange spot rate",
    value = 1.096,
    min_value=1.0,
    step = 1.0,
    format="%.2f")

    usdtngn = st.sidebar.number_input(
    "USDTNGN exchange spot rate",
    value = 865.4,
    min_value=1.0,
    step = 1.0,
    format="%.2f")

    gbpusdt = st.sidebar.number_input(
    "GBPUSDT exchange spot rate",
    value = 1.082,
    min_value=1.0,
    step = 1.0,
    format="%.2f")

    # client = Client()
    # eurusdt = round(float(client.get_klines(symbol= 'EURUSDT', interval = KLINE_INTERVAL_1MINUTE)[-1][4]),2)
    # usdtngn = round(float(client.get_klines(symbol= 'USDTNGN', interval = KLINE_INTERVAL_1MINUTE)[-1][4]),2)
    # gbpusdt = round(float(client.get_klines(symbol= 'GBPUSDT', interval = KLINE_INTERVAL_1MINUTE)[-1][4]),2)
    return dict(eur = eurusdt ,usd = usdtngn, gbp = gbpusdt)


def get_flutter():
    f = requests.get('https://sendgateway.myflutterwave.com/api/v1/config/countrypairs/DE')
    f_data = json.loads(f.text)['data']

    eur = f_data[21]['exchangeRate']
    usd = eur/f_data[15]['exchangeRate']
    gbp =eur/f_data[1]['exchangeRate']
    
    return dict(eur = eur, usd = usd, gbp = gbp)

spot = get_bin_spot()

rates = dict()
rates['flutter'] = get_flutter()



rates['binance_spot']  = dict(
    eur = spot['eur']*spot['usd'],
    usd = spot['usd'],
    gpb = spot['gbp']*spot['usd']
)

rates['binance_p2p'] = dict(
    eur = spot['eur']*p2p_usd,
    usd = p2p_usd,
    gpb = spot['gbp']*p2p_usd
)

def calculate_profit(amount, requested, rates):
    
    request_ngn = amount*requested
    spot_profit = amount*(rates['binance_spot']['eur']*0.98 - requested)
    p2p_profit = amount*(rates['binance_p2p']['eur'] - requested)
    flutter_profit = amount*(rates['flutter']['eur'] - requested)
    
    profit = dict(
        flutter = flutter_profit,
        spot = spot_profit,
        p2p = p2p_profit
        )
    
    return profit

def create_array(N):
    # Calculate the step size for the elements to the left and right of N
    step = 5
    length = 7
    # Initialize an empty array with 7 elements
    result = [0] * length

    # Fill the array with the elements in the specified pattern
    for i in range(length):
        result[i] = N - (3 - i) * step

    return result

def profit_chart(amount, requested, rates, profit):
    
    xlist = create_array(requested)
    ylist = []
    for x in xlist:
        y = calculate_profit(amount, x, rates)
        ylist.append(y['p2p'])
    
    xlist.append(rates['flutter']['eur'])
    ylist.append(profit['flutter'])
    
    colors = ['lightslategray',] * len(xlist)
    colors[xlist.index(requested)] = 'crimson'
    colors[xlist.index(rates['flutter']['eur'])] = 'blue'
    # fig = px.bar(x=xlist, y=ylist)
    fig = go.Figure(data=[go.Bar(
    x=xlist,
    y=ylist,
    marker_color=colors # marker color can be a single color value or an iterable
    )
                          ]
                    )
    # fig.add_hline(y= profit['flutter'], line_dash="dot", 
    #           annotation_text="Flutterwave", 
    #           annotation_position="top right")

    return fig


profit = calculate_profit(amount, requested, rates)
profit_plot = profit_chart(amount, requested, rates, profit) 
    
# if submit:


st.write("Rates \n")
st.write(rates)
st.write("Profit \n")
st.write(profit)

st.plotly_chart(profit_plot, use_container_width=True)



    
