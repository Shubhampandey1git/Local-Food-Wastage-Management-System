import streamlit as st
import sqlite3
import pandas as pd
import os

# ---------- DB Connection ----------
def get_connection():
    return sqlite3.connect("data.db")

def run_query(query, params=()):
    conn = get_connection()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

# ---------- Food Listings Page ----------
def food_listings_page():
    st.header("🍲 Available Food Listings")

    # Fetch unique filter values
    conn = get_connection()
    cities = pd.read_sql("SELECT DISTINCT Location FROM Food_Listings;", conn)["Location"].dropna().tolist()
    providers = pd.read_sql("SELECT DISTINCT Provider_Type FROM Food_Listings;", conn)["Provider_Type"].dropna().tolist()
    food_types = pd.read_sql("SELECT DISTINCT Food_Type FROM Food_Listings;", conn)["Food_Type"].dropna().tolist()
    conn.close()

    # Sidebar filters
    city = st.sidebar.selectbox("Filter by City", ["All"] + cities)
    provider = st.sidebar.selectbox("Filter by Provider Type", ["All"] + providers)
    food_type = st.sidebar.selectbox("Filter by Food Type", ["All"] + food_types)

    # Build query dynamically
    query = "SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Provider_Type, Location, Food_Type, Meal_Type FROM Food_Listings WHERE 1=1"
    params = []

    if city != "All":
        query += " AND Location = ?"
        params.append(city)
    if provider != "All":
        query += " AND Provider_Type = ?"
        params.append(provider)
    if food_type != "All":
        query += " AND Food_Type = ?"
        params.append(food_type)

    df = run_query(query, params)

    st.write("### Filtered Results")
    st.dataframe(df, use_container_width=True)

    st.success(f"Found {len(df)} matching food items ✅")

# ---------- Providers & Receivers Page ----------
def providers_receivers_page():
    st.header("📇 Providers & Receivers Directory")

    conn = get_connection()
    cities_prov = pd.read_sql("SELECT DISTINCT City FROM Providers;", conn)["City"].dropna().tolist()
    cities_recv = pd.read_sql("SELECT DISTINCT City FROM Receivers;", conn)["City"].dropna().tolist()
    conn.close()

    # Allow user to select city
    city = st.selectbox("Select a City", sorted(set(cities_prov + cities_recv)))

    # Show providers in that city
    st.subheader("🏢 Food Providers")
    prov_query = """
        SELECT Name, Type, Contact, Address
        FROM Providers
        WHERE City = ?
    """
    prov_df = run_query(prov_query, (city,))
    if not prov_df.empty:
        st.dataframe(prov_df, use_container_width=True)
    else:
        st.info("No providers found in this city.")

    # Show receivers in that city
    st.subheader("🤝 Receivers")
    recv_query = """
        SELECT Name, Type, Contact
        FROM Receivers
        WHERE City = ?
    """
    recv_df = run_query(recv_query, (city,))
    if not recv_df.empty:
        st.dataframe(recv_df, use_container_width=True)
    else:
        st.info("No receivers found in this city.")

# ---------- CRUD Operations Page ----------
def crud_operations_page():
    st.header("🛠 Manage Food Listings (CRUD)")

    conn = get_connection()
    cursor = conn.cursor()

    # --- CREATE ---
    st.subheader("➕ Add a New Food Listing")
    with st.form("add_form", clear_on_submit=True):
        food_name = st.text_input("Food Name")
        quantity = st.number_input("Quantity", min_value=1, step=1)
        expiry_date = st.date_input("Expiry Date")
        provider_id = st.number_input("Provider ID", min_value=1, step=1)
        provider_type = st.text_input("Provider Type")
        location = st.text_input("City / Location")
        food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
        submitted = st.form_submit_button("Add Listing")
        if submitted:
            cursor.execute("""
                INSERT INTO Food_Listings 
                (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type))
            conn.commit()
            st.success("✅ New food listing added!")

    # --- READ ---
    st.subheader("📖 Current Food Listings")
    listings = pd.read_sql("SELECT * FROM Food_Listings LIMIT 50;", conn)
    st.dataframe(listings, use_container_width=True)

    # --- UPDATE ---
    st.subheader("✏️ Update an Existing Listing")
    ids = pd.read_sql("SELECT Food_ID FROM Food_Listings;", conn)["Food_ID"].tolist()
    if ids:
        food_id = st.selectbox("Select Food ID to Update", ids)
        new_quantity = st.number_input("New Quantity", min_value=0, step=1)
        new_status = st.date_input("New Expiry Date")
        if st.button("Update Listing"):
            cursor.execute("UPDATE Food_Listings SET Quantity=?, Expiry_Date=? WHERE Food_ID=?", (new_quantity, new_status, food_id))
            conn.commit()
            st.success(f"✅ Listing {food_id} updated!")
    else:
        st.info("No listings available to update.")

    # --- DELETE ---
    st.subheader("🗑 Delete a Listing")
    del_id = st.selectbox("Select Food ID to Delete", ids if ids else [])
    if st.button("Delete Listing"):
        cursor.execute("DELETE FROM Food_Listings WHERE Food_ID=?", (del_id,))
        conn.commit()
        st.warning(f"⚠️ Listing {del_id} deleted!")

    conn.close()

# ---------- SQL Trends Page ----------
def sql_trends_page():
    st.header("📊 SQL Trends & Insights")

    # Map user-friendly names to CSV file paths
    QUERY_OUTPUTS = {
        "Providers per City": "results/Providers_per_City.csv",
        "Receivers per City": "results/Receivers_per_City.csv",
        "Provider Type Contributions": "results/Provider_Type_Contributions.csv",
        "Provider Contacts by City": "results/Provider_Contacts_by_City.csv",
        "Top Receivers by Claims": "results/Top_Receivers_by_Claims.csv",
        "Total Food Available": "results/Total_Food_Available.csv",
        "Top City by Listings": "results/Top_City_by_Listings.csv",
        "Most Common Food Types": "results/Most_Common_Food_Types.csv",
        "Claims per Food Item": "results/Claims_per_Food_Item.csv",
        "Top Provider by Successful Claims": "results/Top_Provider_by_Successful_Claims.csv",
        "Claim Status Distribution": "results/Claim_Status_Distribution.csv",
        "Avg Quantity Claimed per Receiver": "results/Avg_Quantity_Claimed_per_Receiver.csv",
        "Most Claimed Meal Type": "results/Most_Claimed_Meal_Type.csv",
        "Total Donated per Provider": "results/Total_Donated_per_Provider.csv",
        "Cities with Highest Demand": "results/Cities_with_Highest_Demand.csv"
    }

    # Dropdown to select analysis
    query_name = st.selectbox("Choose a Trend to View", list(QUERY_OUTPUTS.keys()))

    # Load CSV
    file_path = QUERY_OUTPUTS[query_name]
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)

        st.subheader(f"Results: {query_name}")
        st.dataframe(df, use_container_width=True)

        # Visualization: auto-generate if possible
        if df.shape[1] == 2:  # if two columns → bar chart
            x, y = df.columns[0], df.columns[1]
            st.bar_chart(df.set_index(x))
        elif "Date" in df.columns[0] or "Day" in df.columns[0]:
            st.line_chart(df.set_index(df.columns[0]))
        else:
            st.info("📋 No chart available for this query.")
    else:
        st.error("❌ CSV file not found. Please check the outputs folder.")

# ---------- Main App ----------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Food Listings", "Providers & Receivers", "CRUD Operations", "SQL Trends"])

if page == "Food Listings":
    food_listings_page()
elif page == "Providers & Receivers":
    providers_receivers_page()
elif page == "CRUD Operations":
    crud_operations_page()
elif page == "SQL Trends":
    sql_trends_page()