import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Personal Immersion Tracker")

st.header("Add a New Log")
with st.form("create_log"):
    log_type = st.text_input("Type")
    duration = st.number_input("Duration (mins)", min_value=1)
    description = st.text_input("Description")
    submitted = st.form_submit_button("Submit")

    if submitted:
        response = requests.post(f"{API_URL}/log", json={
            "type": log_type,
            "duration": duration,
            "description": description
        })
        if response.status_code == 200:
            st.success("Log created!")
        else:
            st.error(f"Failed: {response.text}")


st.header("All Logs")
response = requests.get(f"{API_URL}/logs")
if response.status_code == 200:
    logs = response.json()
    for log in logs:
        st.write(log)
else:
    st.error("Could not fetch logs.")

st.markdown("---")
st.subheader("Total Time by Type")

try:
    response = requests.get(f"{API_URL}/logs")
    logs = response.json()
    all_types = list(set(log["type"] for log in logs))  # unique types
except Exception as e:
    st.error(f"Failed to fetch logs: {e}")
    logs = []
    all_types = []

selected_type = st.selectbox("Select type to calculate total time", all_types)

if st.button("Calculate Total Time (mins)"):
    try:
        filtered = [log for log in logs if log["type"] == selected_type]
        total_duration = sum(log["duration"] for log in filtered)
        st.success(f"Total time logged for '{selected_type}': **{total_duration} minutes**")
    except Exception as e:
        st.error(f"Error: {e}")


st.markdown("---")
st.subheader("Delete a Log")

try:
    response = requests.get(f"{API_URL}/logs")
    logs = response.json()
except Exception as e:
    st.error(f"Failed to fetch logs: {e}")
    logs = []

if logs:
    log_options = [
        f"{log['type']} | {log['duration']} mins | {log['description']} | {log['date']} | {log['id']}"
        for log in logs
    ]
    selected_log = st.selectbox("Select a log to delete", log_options)

    if st.button("Delete Selected Log"):
        try:
            log_id = selected_log.split(" | ")[-1]
            delete_response = requests.delete(f"{API_URL}/log/{log_id}")
            if delete_response.status_code == 200:
                st.success("Log deleted successfully! Refresh to see updates.")
            else:
                st.error(f"Failed to delete. Status: {delete_response.status_code}")
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("No logs found.")

st.markdown("---")
st.subheader("Update a Log")

try:
    response = requests.get(f"{API_URL}/logs")
    logs = response.json()
except Exception as e:
    st.error(f"Failed to fetch logs: {e}")
    logs = []

if logs:
    log_options = [
        f"{log['type']} | {log['duration']} mins | {log['description']} | {log['date']} | {log['id']}"
        for log in logs
    ]
    selected_log = st.selectbox("Select a log to update", log_options)
    log_id = selected_log.split(" | ")[-1]
    selected_data = next(log for log in logs if log["id"] == log_id)

    new_type = st.text_input("Type", value=selected_data["type"])
    new_duration = st.number_input("Duration (minutes)", min_value=0, value=selected_data["duration"])
    new_description = st.text_input("Description", value=selected_data["description"])

    if st.button("Update Log"):
        payload = {
            "type": new_type,
            "duration": new_duration,
            "description": new_description
        }
        try:
            update_response = requests.put(f"{API_URL}/log/{log_id}", json=payload)
            if update_response.status_code == 200:
                st.success("Log updated successfully!")
            else:
                st.error(f"Failed to update. Status code: {update_response.status_code}")
        except Exception as e:
            st.error(f"Error during update: {e}")
else:
    st.info("No logs found.")