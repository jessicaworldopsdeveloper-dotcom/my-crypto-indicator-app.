import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta

# 1. Setup the Page Layout
st.set_page_config(page_title="Logic Trade App", layout="wide")

st.title("📊 Crypto Logic Dashboard")
st.write("Real-time technical indicators translated into human advice.")

# 2. Sidebar for User Selection
symbol = st.sidebar.selectbox("Select Coin", ["BTC-USD", "ETH-USD", "SOL-USD", "NVDA"])
interval = st.sidebar.radio("Timeframe", ["1h", "4h", "1d"])

# 3. Fetch Real-Time Data
df = yf.download(symbol, period="60d", interval=interval)

if not df.empty:
    # 4. Calculate Indicators (The Math)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    macd = ta.macd(df['Close'])
    df = pd.concat([df, macd], axis=1)
    
    current_rsi = df['RSI'].iloc[-1]
    
    # 5. THE MAIN SCOREBOARD (Consensus)
    st.header(f"Live Analysis: {symbol}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Current RSI", f"{current_rsi:.2f}")
        # Apply your IF-THEN Map
        if current_rsi > 70:
            st.error("🚨 OVERBOUGHT")
            st.write("**Advice:** The market is overheated. High risk of a 'Bull Trap'. Consider waiting for a dip.")
        elif current_rsi < 30:
            st.success("✅ OVERSOLD")
            st.write("**Advice:** Sellers are exhausted. This is often a 'Value Zone' for a bounce.")
        else:
            st.info("🟡 NEUTRAL")
            st.write("**Advice:** No extreme pressure. The trend is likely to continue its current path.")

    with col2:
        st.write("### 📈 Price & RSI History")
        st.line_chart(df['Close'].tail(50))
        st.line_chart(df['RSI'].tail(50))

    # 6. THE DEEP DIVE SECTION (The Library)
    st.divider()
    st.header("📚 Indicator Library")
    
    with st.expander("🔍 View Separate Indicators"):
        tab1, tab2 = st.tabs(["Momentum", "Trend"])
        
        with tab1:
            st.write("**Relative Strength Index (RSI)**")
            st.write("Status: " + ("Extreme" if current_rsi > 70 or current_rsi < 30 else "Normal"))
            st.progress(int(current_rsi)) # Visual progress bar
            
        with tab2:
            st.write("**MACD (Moving Average Convergence Divergence)**")
            last_macd = df.iloc[-1]['MACD_12_26_9']
            st.write(f"MACD Value: {last_macd:.4f}")
            if last_macd > 0:
                st.write("Interpretation: Short-term momentum is stronger than long-term. Bullish.")
            else:
                st.write("Interpretation: Momentum is fading. Bearish.")

else:
    st.warning("Data not found. Please try a different symbol.")
