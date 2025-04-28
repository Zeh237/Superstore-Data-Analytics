# Superstore Data Analytics Dashboard

A Flask-based web application providing interactive dashboards for analyzing superstore sales data across various dimensions like time, geography, categories, and customer segments.

## Table of Contents
- [About](#about)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Screenshots](#screenshots)
- [Contact](#contact)

## About

This project is a web dashboard built with Flask that connects to superstore sales database to visualize key metrics and trends. It allows users to filter data dynamically based on various criteria such as date ranges, ship modes, locations (country, state, city, region), categories, and customer segments, providing insights into sales performance, profitability, and regional/segment-specific trends.

## Features

The dashboard is organized into several sections, each offering specific analytical views:

* **Sales Analytics (`/`)**:
    * Overall Sales and Profit Summations
    * Sales, Profit, and Profit Margin performance per year
    * Year-over-Year (YoY) Growth analysis for Sales, Profit, and Profit Margin
    * Filtering by Date Range, Ship Mode, Country, City, State, Region, Category, Sub-Category, and Segment.

* **Category Analytics (`/categories`)**:
    * Identification of Top Selling Categories
    * Sales Performance of Categories per year
    * Sales, Profit, and Order Count breakdown by Category
    * Profit Performance of Categories per year
    * Filtering by Date Range, Ship Mode, Country, City, State, Region, and Segment.

* **Regional Analytics (`/regions`)**:
    * Analysis of Top Cities per Region
    * Average Order Value (AOV) per Region
    * Unique Customer Count per Region
    * Regional Sales Performance per year
    * Average Profit per Order per Region
    * Filtering by Date Range, Ship Mode, Country, City, State, and Segment.

* **Segment Analytics (`/segments`)**:
    * Sales Performance per Segment over time
    * Identification of Top Selling Categories, Cities, and States per Segment
    * Breakdown of Performance by Ship Mode per Segment
    * Year-over-Year Growth analysis per Segment
    * Filtering by Date Range, Ship Mode, Country, City, State, Region, Category, Sub-Category, and City.

All dashboards include interactive filtering capabilities based on available dimensions.

## Technologies Used

* **Backend:**
    * Flask (Web Framework)
    * Python
    * SQLAlchemy (ORM for database interaction)
    * Pandas (Data analysis and manipulation)
    * `utils.py` (for data fetching utility functions)
    * Specific analytics modules (`salesAnalytics.py`, `categoryAnalytics.py`, `regionalAnalytics.py`, `segmentAnalytics.py`)

* **Frontend:**
    * HTML5
    * CSS
    * JavaScript
    * Jinja2 (Templating Engine)
    * ChartJS

* **Database:**
    * mysql

## Prerequisites

Before you begin, ensure you have the following installed:

* Python 3.12
* pip (Python package installer)
* A database system eg  mysql

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Zeh237/Superstore-Data-Analytics.git
    cd Superstore-Data-Analytics
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    # On Windows:
    # venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Setup:**

    * In the root directory of the project you will see a db.sql file, it contains all the superstore data needed for this project. Import it into your database using mysqlworkbench or any tool of your choice
    * Head on to the .env file and specify your database credentials. the .env.example will help you. The env file should look like this
      
    ![image](https://github.com/user-attachments/assets/44bb9bc8-9978-4bdb-9f8d-37fd2e245329)


## Running the Application

With your virtual environment activated and database configured:

```bash
flask run
```

The application should now be running at http://127.0.0.1:5000/.

## Screenshots
* The visiting the link above will take you to the sales analytics page that look like this

![image](https://github.com/user-attachments/assets/3f648eed-fa91-4348-9131-57ddfb955fe3)
![image](https://github.com/user-attachments/assets/ed519b23-4eae-451e-aeb8-6d08a3f2af2d)


* The category analytics page looks like this

![image](https://github.com/user-attachments/assets/be1b3dcf-53b0-4446-9a6f-7496fdf1c96d)
![image](https://github.com/user-attachments/assets/72ab00f0-efc5-41c9-abd3-b27cc5a953ba)


* The regional analytics page looks like this
![image](https://github.com/user-attachments/assets/4503e09f-3424-4c0b-8dcc-e2a3cda33998)
![image](https://github.com/user-attachments/assets/6cf423e5-9400-4fe4-b02c-49bcc01a9c30)

* The Segment analytics page looks like this
![image](https://github.com/user-attachments/assets/1205ed2d-0700-4c20-9e3d-3a3452d3b5b0)
![image](https://github.com/user-attachments/assets/96b71a14-6f16-40bf-8a9a-cb65498cdd53)
![image](https://github.com/user-attachments/assets/a77f38c3-d6cc-4632-b213-8e7f580a554e)

## Contact
You are free to contact me at zehbrien@gmail.com for inquiries. Stay blessed✌.
