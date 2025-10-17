# Etsy Digital Planner 2026 — Power BI Dashboard

📊 **Interactive Data Analysis & Visualization Project**  
This project explores the market for **Digital Planners (2026)** on [Etsy.com](https://www.etsy.com), using **Python Web Scraping** for data extraction and **Power BI** for visualization.

---

## 🚀 Project Overview

The goal of this project is to analyze the **Etsy digital planner market** by collecting real product data, cleaning it, and building an interactive Power BI dashboard that reveals key business insights such as:

- Top-performing sellers and pricing trends  
- The ratio of digital vs physical products  
- Category-level breakdowns  
- Distribution of reviews and ratings  

---

## 🧠 Skills Demonstrated

- **Web Scraping** with Python (`Selenium`, `BeautifulSoup`, `pandas`)  
- **Data Cleaning & Transformation**  
- **Business Data Analysis**  
- **DAX & Power BI Dashboard Design**  
- **Data Visualization & Storytelling**

---

## 🧩 Data Collection

Data was collected using a custom Python script:

etsy_digital_planner_2026_scraper.py


## It extracts:

Product title, price, and link

Seller name and total sales

Product type (digital / physical)

Tags and primary category

Review count and rating

Output file:

etsy_digital_planner_2026_raw.csv

Then the data was cleaned and prepared for Power BI in:

etsy_digital_planner_2026_cleaned.csv


📈 Power BI Dashboard Structure
1️⃣ Overview Page

KPIs: Total Listings, Distinct Sellers, Average Price, % Digital

Visuals: Category breakdown, Price distribution, Rating trend

2️⃣ Seller Insights

Top 10 sellers by total sales

Average product price vs. review count

Digital vs Physical share per seller

3️⃣ Product Analysis

Scatter plot: Price vs. Rating

Word cloud / bar chart of most common tags

Filter panel: Seller name, is_digital, category



📂 Repository Contents

| File                                       | Description            |
| ------------------------------------------ | ---------------------- |
| `etsy_digital_planner_2026_scraper.py`     | Python scraper script  |
| `etsy_digital_planner_2026_raw.csv`        | Raw data file          |
| `etsy_digital_planner_2026_cleaned.csv`    | Cleaned dataset        |
| `Etsy_Digital_Planner_2026_Dashboard.pbix` | Power BI dashboard     |
| `dashboard_preview.pdf`                    | Exported dashboard PDF |
| `README.md`                                | Project documentation  |




🧭 Insights Example

💡 Digital products represent more than 80% of listings.

💰 Top 5 sellers generate over 60% of total sales.

⭐ Products priced between $8–$15 tend to receive the best ratings.

🕓 Sales peak during October–December, when customers plan for the next year.


🧩 Tools & Technologies

| Category           | Tools                                   |
| ------------------ | --------------------------------------- |
| Data Collection    | Python, Selenium, BeautifulSoup, pandas |
| Data Visualization | Power BI, DAX                           |
| Data Cleaning      | Power Query                             |
| Other              | GitHub, Excel, JSON Theme               |


💼 Author

Feriel Chorfi
Data Analyst | Web Scraping | Power BI
📍 Tunisia
🌐 LinkedIn
 | GitHub

📜 License

This project is for educational and portfolio purposes only.
Etsy data was collected responsibly for analytical demonstration.
















```bash
etsy_digital_planner_2026_scraper.py
