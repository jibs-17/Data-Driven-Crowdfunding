import streamlit as st
import csv
import os
import matplotlib.pyplot as plt
import qrcode



# CSV File
FILENAME = "fire_relief_log.csv"

# Ensure CSV file with headers exists
if not os.path.exists(FILENAME):
    with open(FILENAME, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Area', 'Resource Type'])

# Preset options
locations = ["Srinagar", "Anantnag", "Baramulla", "Pulwama", "Budgam", "Kupwara" ]
resources = ["Fire Affected Area", "Relief Camp", "Water Supply Point", "Medical Help", "Donation Center"]

# Streamlit page settings
st.set_page_config(page_title="Crowd Funding - Kashmir", page_icon="a")
st.title("Crowd Funding - Kashmir")
st.caption("Help Kashmir by reporting disaster prone areas and tracking relief resources.")

menu = st.sidebar.radio("Menu", ["📝 Add Entry", "📄 View Records", "📊 Visualize Data"])

# 📝 Add entry
if menu == "📝 Add Entry":
    st.subheader("Report Area or Relief Resource")
    area = st.selectbox("Choose Location", locations)
    resource = st.selectbox("Select Resource Type", resources)
    
    if st.button("Submit"):
        with open(FILENAME, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([area, resource])
        st.success(f"✔️ Saved: {area} - {resource}")

# 📄 View records
elif menu == "📄 View Records":
    st.subheader("Current Entries")
    try:
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            data = list(reader)
            if data:
                for row in data:
                    st.write(f"📍 **Area:** {row[0]} | **Resource:** {row[1]}")
            else:
                st.warning("No data available.")
    except FileNotFoundError:
        st.error("Data file not found.")

# 📊 Visualization
elif menu == "📊 Visualize Data":
    st.subheader("Resource Distribution Chart")
    data = {res: 0 for res in resources}
    try:
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row[1] in data:
                    data[row[1]] += 1
    except FileNotFoundError:
        st.error("No data found.")

    if sum(data.values()) > 0:
        fig, ax = plt.subplots()
        ax.bar(data.keys(), data.values(), color='orange', edgecolor='black')
        plt.xticks(rotation=15)
        plt.title("Fire Relief Resource Usage")
        st.pyplot(fig)
    else:
        st.info("No entries yet.")


