import streamlit as st
import boto3
import pandas as pd
import csv
import io

# AWS Credentials & Table Info
AWS_ACCESS_KEY = "your_access_key"
AWS_SECRET_KEY = "your_secret_key"
AWS_REGION = "eu-north-1"
DYNAMODB_TABLE = "exercise_records"

# Initialize DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)
table = dynamodb.Table(DYNAMODB_TABLE)

# Function to insert a record into DynamoDB
def insert_record(username, datetime, squat_count, pushup_count):
    table.put_item(
        Item={
            'username': username,
            'datetime': datetime,
            'squat_count': int(squat_count),
            'pushup_count': int(pushup_count)
        }
    )

# Function to read CSV and insert data
def process_csv(file):
    df = pd.read_csv(file)
    for _, row in df.iterrows():
        insert_record(row["username"], row["datetime"], row["squat_count"], row["pushup_count"])
    st.success("✅ Data successfully uploaded to DynamoDB!")

# Function to fetch all data from DynamoDB
def fetch_data():
    response = table.scan()
    items = response.get("Items", [])
    return pd.DataFrame(items)

# Streamlit UI
st.title("📂 CSV to DynamoDB Migration")

# File Upload
uploaded_file = st.file_uploader("📥 Upload CSV File", type=["csv"])
if uploaded_file:
    process_csv(uploaded_file)

# Show Data Button
if st.button("📊 Show Data from DynamoDB"):
    df = fetch_data()
    st.write(df)
