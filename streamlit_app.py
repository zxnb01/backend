import streamlit as st
import requests
import json

# Base URL of your FastAPI backend (Update it to match the actual server URL)
BASE_URL = "http://localhost:8000"

# Function to create or update a subscription
def create_or_update_subscription(subscription_id=None):
    st.subheader(f"Create / Update Subscription")
    target_url = st.text_input("Target URL", value="" if not subscription_id else "http://example.com")
    secret = st.text_input("Secret Key (optional)", value="")
    event_type = st.text_input("Event Type (optional)", value="")
    
    if st.button("Submit"):
        data = {
            "target_url": target_url,
            "secret": secret,
            "event_type": event_type
        }
        
        if subscription_id:
            response = requests.put(f"{BASE_URL}/api/subscriptions/{subscription_id}", json=data)
        else:
            response = requests.post(f"{BASE_URL}/api/subscriptions", json=data)
        
        if response.status_code == 200 or response.status_code == 201:
            st.success(f"Subscription {'updated' if subscription_id else 'created'} successfully!")
        else:
            st.error(f"Error: {response.text}")

# Function to list subscriptions
def list_subscriptions():
    st.subheader("All Subscriptions")
    response = requests.get(f"{BASE_URL}/api/subscriptions")
    
    if response.status_code == 200:
        subscriptions = response.json()
        for sub in subscriptions:
            subscription_id = sub['id']
            st.write(f"ID: {subscription_id}, Target URL: {sub['target_url']}, Event Type: {sub.get('event_type', 'N/A')}")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"View Logs {subscription_id}", key=f"logs_{subscription_id}"):
                    show_delivery_logs(subscription_id)
            with col2:
                if st.button(f"Update {subscription_id}", key=f"update_{subscription_id}"):
                    create_or_update_subscription(subscription_id)

# Function to handle webhook ingestion
def ingest_webhook():
    st.subheader("Ingest Webhook")
    subscription_id = st.text_input("Subscription ID (for testing)", value="")
    event_type = st.text_input("Event Type", value="")
    payload = st.text_area("Payload (JSON)", value=json.dumps({"key": "value"}), height=200)
    
    if st.button("Submit Webhook"):
        data = {
            "subscription_id": subscription_id,
            "event_type": event_type,
            "payload": json.loads(payload)
        }
        
        response = requests.post(f"{BASE_URL}/api/ingest/{subscription_id}", json=data)
        
        if response.status_code == 202:
            st.success("Webhook successfully ingested!")
        else:
            st.error(f"Error: {response.text}")

# Function to show delivery logs for a specific subscription
def show_delivery_logs(subscription_id):
    st.subheader(f"Delivery Logs for Subscription {subscription_id}")
    response = requests.get(f"{BASE_URL}/api/status/{subscription_id}")
    
    if response.status_code == 200:
        logs = response.json()
        if not logs:
            st.write("No logs available.")
        else:
            for log in logs:
                st.write(f"Task ID: {log['task_id']}, Timestamp: {log['timestamp']}, Status: {log['status']}, HTTP Code: {log['http_code']}, Error: {log.get('error', 'N/A')}")
    else:
        st.error(f"Error: {response.text}")

# Main function to render the UI
def main():
    st.title("Webhook Delivery Service UI")

    # Sidebar navigation
    st.sidebar.header("Navigation")
    app_mode = st.sidebar.radio("Choose a page", ["Manage Subscriptions", "Ingest Webhook", "View Delivery Logs"])

    if app_mode == "Manage Subscriptions":
        list_subscriptions()

    elif app_mode == "Ingest Webhook":
        ingest_webhook()

    elif app_mode == "View Delivery Logs":
        subscription_id = st.text_input("Enter Subscription ID to view logs")
        if subscription_id:
            show_delivery_logs(subscription_id)

if __name__ == "__main__":
    main()
