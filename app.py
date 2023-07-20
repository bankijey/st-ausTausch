import streamlit as st
import plotly.express as px

st.sidebar.title("Input parameters")

amount = st.sidebar.number_input(
    "Enter exchange amount (€)",
    value = 100.0,
    min_value=1.0,
    step = 1.0,
    format="%.2f")

rate = st.sidebar.number_input(
    "Enter requested rate (₦)",
    value = 915.0,
    min_value=1.0,
    step=5.0,
    format="%.2f")

submit = st.sidebar.button(
    label = 'Submit'
)

request_ngn = amount*rate

eurusdt = 1.1179
usdtngn = 868.9 
bin_spot_amt = amount*eurusdt*usdtngn*0.98

def calculate_profit(amount, rate):
    request_ngn = amount*rate
    bin_spot_amt = amount*eurusdt*usdtngn*0.98
    profit = bin_spot_amt-request_ngn
    return profit
    
    # return{
    #     'requested': request_ngn,
    #     'binance_spot': bin_spot_amt}
    
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

def profit_chart(amount, rate):
    xlist = create_array(rate)
    ylist = []
    for x in xlist:
        y = calculate_profit(amount, x)
        ylist.append(y)
    
    fig = px.bar(x=xlist, y=ylist)
    return fig

profit_plot = profit_chart(amount, rate) 
    
if submit:
    st.write(f"Naira amount to send ₦ {request_ngn}")
    st.write(f"Naira amount to recieved from binance spot ₦ {bin_spot_amt}")
    st.write(f"Naira profit ₦ {bin_spot_amt-request_ngn}")
    st.plotly_chart(profit_plot, use_container_width=True)
    
    