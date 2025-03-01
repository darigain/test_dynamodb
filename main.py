import streamlit as st
import boto3
import pandas as pd
import os

# AWS Credentials (Make sure to set them correctly)
AWS_ACCESS_KEY_ID = "your_access_key"
AWS_SECRET_ACCESS_KEY = "your_secret_key"
AWS_REGION = "eu-north-1"  # Change this if needed
DYNAMODB_TABLE = "exercise_records"

# Connect to DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

table = dynamodb.Table(DYNAMODB_TABLE)

# Function to Fetch Data
def fetch_data():
    response = table.scan()
    items = response.get("Items", [])
    return pd.DataFrame(items) if items else pd.DataFrame(columns=["username", "datetime", "squat_count", "pushup_count"])

# Streamlit UI
st.title("📊 DynamoDB Data Viewer")

if st.button("Show Data"):
    df = fetch_data()
    if df.empty:
        st.warning("No data found in DynamoDB table.")
    else:
        st.write(df)
