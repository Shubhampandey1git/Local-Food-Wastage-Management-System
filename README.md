# 🍲 Food Waste Management System

## 📌 Project Overview

This project is a **SQL-powered Food Waste Management System** with an interactive **Streamlit web app**.
It helps connect **food providers** (restaurants, supermarkets, catering services, etc.) with **receivers** (NGOs, individuals, and organizations) to minimize **food wastage** and ensure efficient distribution.

The system supports **data storage, analysis, and visualization** of food donations, claims, and availability trends.

---

## 🚀 Features

* **Food Listings**: Filter food donations by city, provider type, and food type.
* **Providers & Receivers Directory**: View and contact food providers/receivers by city.
* **CRUD Operations**: Add, update, delete, and view food listings.
* **SQL Trends & Insights**: 15+ SQL queries for data analysis with auto-generated charts.
* **Data Cleaning & Integration**: CSV data standardized and loaded into an SQLite database.

---

## 🛠️ Tech Stack

* **Python** (Data processing, analysis)
* **SQLite** (Database storage and querying)
* **Pandas** (CSV data handling)
* **Streamlit** (Web application & dashboard)

---

## 📂 Project Structure

```
project/
│── app.py                     # Streamlit main app
│── data.db                # SQLite database
│── results/                   # Pre-saved SQL query results (CSV files)
│   ├── providers_per_city.csv
│   ├── receivers_per_city.csv
│   ├── provider_type_contributions.csv
│   ├── ...
│── test.ipynb    # Jupyter Notebook for cleaning & loading CSVs
│── README.md                  # Project documentation
```

---

## ⚡ How to Run

1. Clone this repo or copy project files.
2. Install dependencies:

   ```
   pip install streamlit pandas sqlite3
   ```

   *(sqlite3 is built into Python, no extra install needed)*
3. Run the app:

   ```
   streamlit run app.py
   ```
4. Open the Streamlit app in your browser at `http://localhost:8501`.

---

## 📊 SQL Analysis Queries (15+)

The project includes SQL-based analysis stored as CSV outputs, such as:

* Providers per City
* Receivers per City
* Provider Type Contributions
* Top Receivers by Claims
* Total Food Available
* Most Common Food Types
* Claims per Food Item
* Claim Status Distribution
* Cities with Highest Demand
  ... and more.

---

## ✅ Results

* Interactive app for exploring food donation data.
* SQL-powered insights for identifying demand, contributions, and wastage patterns.
* Simple CRUD system for real-time data management.
* Visualization of donation and claim trends using Streamlit.

---

## 🔮 Future Scope

* Add **prediction models** for demand forecasting.
* Implement **alerts/notifications** for expiring food.
* Extend to a **multi-user system** with authentication.
* Deploy online for real-world NGO usage.

---

## 🗂️ Data sets
* This project was created during and Internship.
* If you want to use the data that I have used, you can contact me.

---

## 🙋‍♂️ Author

**Shubham Pandey**
📧 [Email Me](mailto:shubhamppandey1084@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/shubham-pandey-6a65a524a/) • [GitHub](https://github.com/Shubhampandey1git)