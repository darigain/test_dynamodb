import streamlit as st
import boto3
import pandas as pd
import io

# AWS Credentials (Ensure they are correct)
AWS_ACCESS_KEY_ID = st.secrets["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = st.secrets["AWS_SECRET_ACCESS_KEY"]
AWS_REGION = st.secrets["AWS_REGION"]
DYNAMODB_TABLE = st.secrets["DYNAMODB_TABLE"]

# Connect to DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

table = dynamodb.Table(DYNAMODB_TABLE)

# Function to insert data into DynamoDB
def insert_data(username, datetime, squat_count, pushup_count):
    item = {
        "username": username,
        "datetime": datetime,
        "squat_count": int(squat_count),
        "pushup_count": int(pushup_count),
    }
    table.put_item(Item=item)

# Function to fetch all data from DynamoDB
def fetch_data():
    response = table.scan()
    items = response.get("Items", [])
    return pd.DataFrame(items) if items else pd.DataFrame(columns=["username", "datetime", "squat_count", "pushup_count"])

# Streamlit UI
st.title("📊 Upload CSV & Save to DynamoDB")

# **Upload CSV Section**
st.subheader("📂 Upload CSV to DynamoDB")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Check if required columns exist
    required_columns = ["id", "username", "datetime", "squat_count", "pushup_count"]
    if not all(col in df.columns for col in required_columns):
        st.error("❌ CSV format is incorrect. Expected columns: " + ", ".join(required_columns))
    else:
        # Drop 'id' column since DynamoDB does not use it
        df = df.drop(columns=["id"])

        # Insert each row into DynamoDB
        for _, row in df.iterrows():
            insert_data(row["username"], row["datetime"], row["squat_count"], row["pushup_count"])
        
        st.success("✅ Data successfully inserted into DynamoDB!")

# **Show Data Section**
st.subheader("📋 View Data in DynamoDB")
if st.button("Show Data"):
    df = fetch_data()
    if df.empty:
        st.warning("⚠️ No data found in DynamoDB table.")
    else:
        st.write(df)
