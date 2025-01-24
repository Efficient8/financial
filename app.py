import streamlit as st
import pandas as pd
import os

# Page Config
st.set_page_config(page_title="Financial", page_icon=":moneybag:", layout="centered")

# Title
st.title("Financial Information")

st.divider()

# Sample DataFrame
data = {
    "Purpose": [],
    "Amount": [],
}

df = pd.DataFrame(data)
df["Purpose"] = df["Purpose"].astype(str)  # Ensure Purpose is string
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

# Owner credentials (can be replaced with a more secure authentication system)
OWNER_USERNAME = os.getenv("OWNER_USERNAME")
OWNER_PASSWORD = os.getenv("OWNER_PASSWORD")

# Session state to manage authentication and button clicks
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "show_login_form" not in st.session_state:
    st.session_state.show_login_form = False

# Button to toggle the login form
if not st.session_state.authenticated:
    if st.button("Login to Edit DataFrame"):
        st.session_state.show_login_form = True

st.divider()

# Show the login form only if the button is clicked
if st.session_state.show_login_form and not st.session_state.authenticated:
    with st.form("login_form"):
        st.write("Enter your credentials to edit the DataFrame:")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

        if login_button:
            if username == OWNER_USERNAME and password == OWNER_PASSWORD:
                st.session_state.authenticated = True
                st.success("Login successful! You can now edit the DataFrame.")
                st.session_state.show_login_form = False
            else:
                st.error("Invalid credentials. Please try again.")

# If authenticated, allow edits
if st.session_state.authenticated:
    st.title("Editable DataFrame (Owner Access)")
    st.write("You can edit the DataFrame below:")

    # Allow the owner to edit the DataFrame
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")

    # Calculate the sum of rows below the header
    sum_row = pd.DataFrame(
        [["Total"] + edited_df.iloc[:, 1:].sum().tolist()],
        columns=edited_df.columns
    )

    # Append the sum row to the DataFrame
    df_with_sum = pd.concat([sum_row, edited_df], ignore_index=True)

    # Display the updated DataFrame
    st.write("Updated DataFrame with Sum Row:")
    st.dataframe(df_with_sum, use_container_width=True)

else:

    # Calculate the sum of rows below the header
    sum_row = pd.DataFrame(
        [["Total"] + df.iloc[:, 1:].sum().tolist()],
        columns=df.columns
    )

    # Append the sum row to the DataFrame
    df_with_sum = pd.concat([sum_row, df], ignore_index=True)

    # Display the static DataFrame
    st.dataframe(df_with_sum, use_container_width=True)
