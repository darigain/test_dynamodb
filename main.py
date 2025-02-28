import streamlit as st
import boto3
import pandas as pd
from datetime import datetime

# Load credentials from Streamlit secrets
aws_access_key = st.secrets["AWS_ACCESS_KEY_ID"]
aws_secret_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
aws_region = st.secrets["AWS_REGION"]
dynamodb_table = st.secrets["DYNAMODB_TABLE"]

# Initialize DynamoDB client
dynamodb = boto3.resource(
    "dynamodb",
    region_name=aws_region,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)
table = dynamodb.Table(dynamodb_table)

# Streamlit UI
st.title("🏋️ FitSmart Test App")

### 1️⃣ Input Fields for Data Entry
username = st.text_input("👤 Enter Username:")
squat_count = st.number_input("🦵 Squat Count", min_value=0, step=1)
pushup_count = st.number_input("💪 Push-up Count", min_value=0, step=1)

# Save to DB Function
def save_to_dynamodb(username, squat_count, pushup_count):
    if not username:
        st.warning("⚠️ Please enter a username.")
        return

    timestamp = datetime.utcnow().isoformat()
    
    table.put_item(
        Item={
            "username": username,
            "datetime": timestamp,
            "squat_count": int(squat_count),
            "pushup_count": int(pushup_count)
        }
    )
    
    st.success(f"✅ Data saved for {username} at {timestamp}!")

# Button to Save Data
if st.button("💾 Save to DB"):
    save_to_dynamodb(username, squat_count, pushup_count)

### 2️⃣ Fetch and Display Full Table
def fetch_all_data():
    response = table.scan()
    return response.get("Items", [])

if st.button("📊 Show Data"):
    records = fetch_all_data()
    
    if records:
        df = pd.DataFrame(records)
        st.write("### 📋 Exercise Records Table")
        st.dataframe(df)
    else:
        st.warning("⚠️ No records found in the database.")
