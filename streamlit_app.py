import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import yfinance as yf
from datetime import date, timedelta

# Set page layout
st.set_page_config(page_title="Stock Graph", page_icon="📈", layout="wide")

with open("css/style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden; height:0;}
    .block-container {
      margin-top: 0;
      padding-top: 0;
    }
    </style>
""", unsafe_allow_html=True)


# Define stock options and allow user to select one
stock_options = ['AAPL', 'MSFT', 'GOOG', 'TSLA', 'NVDA']  # Added NVDA as another option
selected_stock = st.sidebar.selectbox("Select a stock:", stock_options)

# Date range picker for selecting start and end dates
today = date.today()
default_start_date = today - timedelta(days=365)  # Default to 1 year ago

start_date = st.sidebar.date_input("Start Date", default_start_date)
end_date = st.sidebar.date_input("End Date", today)

# Validate the date input
if start_date > end_date:
    st.sidebar.error("Error: End date must fall after start date.")
else:
    # Fetch stock data from yfinance
    stock_data = yf.download(selected_stock, start=start_date, end=end_date)

    # Display a message if no data is returned
    if stock_data.empty:
        st.write(f"No data available for {selected_stock} from {start_date} to {end_date}.")
    else:
        # Prepare the data for candlestick and volume bar chart
        candlestick_data = [
            {"time": row.Index.strftime('%Y-%m-%d'), "open": row.Open, "high": row.High, "low": row.Low, "close": row.Close}
            for row in stock_data.itertuples()
        ]

        volume_data = [
            {"time": row.Index.strftime('%Y-%m-%d'), "value": row.Volume}
            for row in stock_data.itertuples()
        ]

        # Chart options
        priceVolumeChartOptions = {
            "height": 700,
            "rightPriceScale": {
                "scaleMargins": {
                    "top": 0.2,
                    "bottom": 0.25,
                },
                "borderVisible": False,
            },
            "overlayPriceScales": {
                "scaleMargins": {
                    "top": 0.7,
                    "bottom": 0,
                }
            },
            "layout": {
                "background": {
                    "type": 'solid',
                    "color": '#131722'
                },
                "textColor": '#d1d4dc',
            },
            "grid": {
                "vertLines": {
                    "color": 'rgba(42, 46, 57, 0)',
                },
                "horzLines": {
                    "color": 'rgba(42, 46, 57, 0.6)',
                }
            }
        }

        # Candlestick and volume series
        priceVolumeSeries = [
            {
                "type": 'Candlestick',
                "data": candlestick_data,
                "options": {
                    "upColor": '#4CAF50',
                    "borderUpColor": '#4CAF50',
                    "downColor": '#F44336',
                    "borderDownColor": '#F44336',
                }
            },
            {
                "type": 'Histogram',
                "data": volume_data,
                "options": {
                    "color": '#26a69a',
                    "priceFormat": {
                        "type": 'volume',
                    },
                    "priceScaleId": ""  # set as an overlay setting,
                },
                "priceScale": {
                    "scaleMargins": {
                        "top": 0.7,
                        "bottom": 0,
                    }
                }
            }
        ]

        # Display the subheader and render the charts
        st.subheader(f"{selected_stock} Price and Volume Chart")

        renderLightweightCharts([
            {
                "chart": priceVolumeChartOptions,
                "series": priceVolumeSeries
            }
        ], 'priceAndVolume')
