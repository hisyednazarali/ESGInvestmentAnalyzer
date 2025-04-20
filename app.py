import streamlit as st
import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="ESG Investment Analyzer", layout="wide")

st.title("🌿 ESG Investment Analyzer")

# ESG scores defined directly in code
esg_scores = {
    "AAPL": {"ESG_Score": 75, "Environmental": 70, "Social": 80, "Governance": 75},
    "MSFT": {"ESG_Score": 85, "Environmental": 90, "Social": 80, "Governance": 85},
    "TSLA": {"ESG_Score": 65, "Environmental": 60, "Social": 70, "Governance": 65},
    "AMZN": {"ESG_Score": 60, "Environmental": 55, "Social": 65, "Governance": 60},
    "GOOGL": {"ESG_Score": 80, "Environmental": 75, "Social": 85, "Governance": 80},
    "META": {"ESG_Score": 70, "Environmental": 65, "Social": 72, "Governance": 73},
    "NVDA": {"ESG_Score": 78, "Environmental": 72, "Social": 80, "Governance": 76},
    "JPM": {"ESG_Score": 74, "Environmental": 68, "Social": 75, "Governance": 79},
    "JNJ": {"ESG_Score": 82, "Environmental": 78, "Social": 83, "Governance": 85},
    "XOM": {"ESG_Score": 55, "Environmental": 50, "Social": 60, "Governance": 55},
}

tickers = list(esg_scores.keys())

@st.cache_data(show_spinner=True)
def get_financial_data(tickers):
    data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        data.append({
            "Ticker": ticker,
            "Company": info.get("longName"),
            "Market Cap": info.get("marketCap"),
            "PE Ratio": info.get("trailingPE"),
            "ROE": info.get("returnOnEquity"),
            "Dividend Yield": info.get("dividendYield"),
            "Beta": info.get("beta"),
            "Debt to Equity": info.get("debtToEquity"),
        })
    return pd.DataFrame(data)

# Convert ESG dict to DataFrame
esg_df = pd.DataFrame.from_dict(esg_scores, orient='index').reset_index().rename(columns={"index": "Ticker"})

# Fetch financial data
with st.spinner("Fetching financial data..."):
    financial_df = get_financial_data(tickers)

# Merge ESG + financial data
final_df = pd.merge(financial_df, esg_df, on="Ticker")

# Sidebar filters
st.sidebar.header("Filters")
min_esg = st.sidebar.slider("Minimum ESG Score", 0, 100, 60)
max_pe = st.sidebar.slider("Maximum P/E Ratio", 0, 100, 40)

filtered_df = final_df[
    (final_df["ESG_Score"] >= min_esg) &
    (final_df["PE Ratio"] <= max_pe)
]

# Show table
st.subheader("📊 Filtered Companies")
st.dataframe(filtered_df, use_container_width=True)

# ESG vs PE plot
st.subheader("📈 ESG Score vs P/E Ratio")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=filtered_df, x="PE Ratio", y="ESG_Score", hue="Ticker", s=100)
plt.grid(True)
plt.xlabel("P/E Ratio")
plt.ylabel("ESG Score")
st.pyplot(plt)

# Top picks
st.subheader("🏆 Top ESG Picks")
top_df = filtered_df.sort_values(by="ESG_Score", ascending=False).head(5)
st.table(top_df[["Company", "ESG_Score", "PE Ratio", "ROE", "Dividend Yield", "Beta"]])
