import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import requests
import json

st.sidebar.title("Input parameters")

amount = st.sidebar.number_input(
    "Euro exchange amount",
    value = 100.0,
    min_value=1.0,
    step = 1.0,
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

request_ngn = amount*requested

def get_bin_spot():# API calls
    eurusdt = 1.1179 
    usdtngn = 868.9
    gbpusdt = 1.123
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
    length = 9
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
    
    colors = ['lightslategray',] * len(xlist)
    colors[xlist.index(requested)] = 'crimson'
    # fig = px.bar(x=xlist, y=ylist)
    fig = go.Figure(data=[go.Bar(
    x=xlist,
    y=ylist,
    marker_color=colors # marker color can be a single color value or an iterable
    )
                          ]
                    )
    fig.add_hline(y= profit['flutter'], line_dash="dot", 
              annotation_text="Flutterwave", 
              annotation_position="top right")

    return fig


profit = calculate_profit(amount, requested, rates)
profit_plot = profit_chart(amount, requested, rates, profit) 
    
# if submit:


st.write("Rates \n")
st.write(rates)
st.write("Profit \n")
st.write(profit)

st.plotly_chart(profit_plot, use_container_width=True)



    