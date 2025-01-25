import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import os
import requests


# Lottie Files

def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_cal = load_lottie(r"https://lottie.host/11deb4b4-3d8f-47b3-a53c-970a32cecb41/XCdH2OnU4f.json")

# Page Config
st.set_page_config(page_title="Efficient8 Financial Data", page_icon=":moneybag:", layout="centered")

# Title
st_lottie(lottie_cal, height=150, reverse=True)
st.title("Financial Information")

st.divider()

book = 'workbook.xlsx'

df = pd.read_excel(book)

# Ensure correct data types
# df["Purpose"] = df["Purpose"].astype(str)  # Ensure Purpose is string
# df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")  # Ensure Amount is numeric


# Ensure Purpose is string and Amount is numeric
df["Purpose"] = df["Purpose"].astype(str)
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

# Calculate the total row
sum_row = pd.DataFrame(
    [["Total", df["Amount"].sum()]],
    columns=df.columns
)

# Append the total row to the DataFrame
df_with_sum = pd.concat([sum_row, df], ignore_index=True)

# Display the static DataFrame
st.dataframe(df_with_sum, use_container_width=True)
