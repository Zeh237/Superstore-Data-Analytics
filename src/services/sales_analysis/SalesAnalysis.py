import pandas as pd
from sqlalchemy import text
from src.db_connection.connection import DBConnection


class SalesAnalysis:
    def __init__(self):
        self.db_connection = DBConnection()
        self.engine = self.db_connection.create_db_connection()

    def sales_and_profit_sum(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None, state=None,
                             region=None, category=None, sub_category=None, segment=None):
        query = """
            SELECT
                SUM(Sales) AS Total_Sales,
                SUM(Profit) AS Total_Profit
            FROM
                superstore
        """

        conditions = []
        params = {}

        if start_date:
            conditions.append("`Order Date` >= :start_date")
            params['start_date'] = start_date
        if end_date:
            conditions.append("`Order Date` <= :end_date")
            params['end_date'] = end_date
        if ship_mode:
            conditions.append("`Ship Mode` = :ship_mode")
            params['ship_mode'] = ship_mode
        if country:
            conditions.append("Country = :country")
            params['country'] = country
        if city:
            conditions.append("City = :city")
            params['city'] = city
        if state:
            conditions.append("State = :state")
            params['state'] = state
        if region:
            conditions.append("Region = :region")
            params['region'] = region
        if category:
            conditions.append("Category = :category")
            params['category'] = category
        if sub_category:
            conditions.append("`Sub-Category` = :sub_category")
            params['sub_category'] = sub_category
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        with self.engine.connect() as connection:
            result = connection.execute(text(query), params)
            row = result.fetchone()

            if row:
                return {"Sales": row[0], "Profit": row[1]}
            else:
                return {"Sales": 0, "Profit": 0}


    def sales_over_time(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None,
                                state=None, region=None, category=None, sub_category=None, segment=None):

        query = """
            SELECT `Order Date`, SUM(Sales) as Total_Sales
            FROM superstore
        """

        conditions = []
        params = {}
        if start_date:
            conditions.append("`Order Date` >= :start_date")
            params['start_date'] = start_date
        if end_date:
            conditions.append("`Order Date` <= :end_date")
            params['end_date'] = end_date
        if ship_mode:
            conditions.append("`Ship Mode` = :ship_mode")
            params['ship_mode'] = ship_mode
        if country:
            conditions.append("Country = :country")
            params['country'] = country
        if city:
            conditions.append("City = :city")
            params['city'] = city
        if state:
            conditions.append("State = :state")
            params['state'] = state
        if region:
            conditions.append("Region = :region")
            params['region'] = region
        if category:
            conditions.append("Category = :category")
            params['category'] = category
        if sub_category:
            conditions.append("`Sub-Category` = :sub_category")
            params['sub_category'] = sub_category
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Order Date` ORDER BY `Order Date` DESC"

        with self.engine.connect() as connection:
            result = connection.execute(text(query), params)
            sales_data = [{"date": row[0], "sales": row[1]} for row in result.fetchall()]
            return sales_data


    def profits_over_time(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None,
                                state=None, region=None, category=None, sub_category=None, segment=None):

        query = """
                    SELECT `Order Date`, SUM(Profit) as Total_Profit
                    FROM superstore
                """

        conditions = []
        params = {}
        if start_date:
            conditions.append("`Order Date` >= :start_date")
            params['start_date'] = start_date
        if end_date:
            conditions.append("`Order Date` <= :end_date")
            params['end_date'] = end_date
        if ship_mode:
            conditions.append("`Ship Mode` = :ship_mode")
            params['ship_mode'] = ship_mode
        if country:
            conditions.append("Country = :country")
            params['country'] = country
        if city:
            conditions.append("City = :city")
            params['city'] = city
        if state:
            conditions.append("State = :state")
            params['state'] = state
        if region:
            conditions.append("Region = :region")
            params['region'] = region
        if category:
            conditions.append("Category = :category")
            params['category'] = category
        if sub_category:
            conditions.append("`Sub-Category` = :sub_category")
            params['sub_category'] = sub_category
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Order Date` ORDER BY `Order Date` DESC"

        with self.engine.connect() as connection:
            result = connection.execute(text(query), params)
            profit_data = [{"date": row[0], "profit": row[1]} for row in result.fetchall()]
            return profit_data


    def profit_margins_over_time(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None,
                                state=None, region=None, category=None, sub_category=None, segment=None):

        query = """
            SELECT `Order Date`, SUM(Profit) as profit, SUM(Sales) as sales
            FROM superstore
        """

        conditions = []
        params = {}
        if start_date:
            conditions.append("`Order Date` >= :start_date")
            params['start_date'] = start_date
        if end_date:
            conditions.append("`Order Date` <= :end_date")
            params['end_date'] = end_date
        if ship_mode:
            conditions.append("`Ship Mode` = :ship_mode")
            params['ship_mode'] = ship_mode
        if country:
            conditions.append("Country = :country")
            params['country'] = country
        if city:
            conditions.append("City = :city")
            params['city'] = city
        if state:
            conditions.append("State = :state")
            params['state'] = state
        if region:
            conditions.append("Region = :region")
            params['region'] = region
        if category:
            conditions.append("Category = :category")
            params['category'] = category
        if sub_category:
            conditions.append("`Sub-Category` = :sub_category")
            params['sub_category'] = sub_category
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Order Date` ORDER BY `Order Date` DESC"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        df['profit_margin'] = df.apply(lambda row: row['profit'] / row['sales'] if row['sales'] > 0 else 0, axis=1)

        df['Order Date'] = pd.to_datetime(df['Order Date'])

        df = df.rename(columns={'Order Date': 'date'})

        return df.to_dict(orient="records")


    def sales_profit_profit_margin_per_year(self, ship_mode=None, country=None, city=None,
                                state=None, region=None, category=None, sub_category=None, segment=None):
        query = """
            SELECT `Order Date`, SUM(Sales) as Total_Sales, SUM(Profit) as Total_Profit
            FROM superstore
        """

        conditions = []
        params = {}
        if ship_mode:
            conditions.append("`Ship Mode` = :ship_mode")
            params['ship_mode'] = ship_mode
        if country:
            conditions.append("Country = :country")
            params['country'] = country
        if city:
            conditions.append("City = :city")
            params['city'] = city
        if state:
            conditions.append("State = :state")
            params['state'] = state
        if region:
            conditions.append("Region = :region")
            params['region'] = region
        if category:
            conditions.append("Category = :category")
            params['category'] = category
        if sub_category:
            conditions.append("`Sub-Category` = :sub_category")
            params['sub_category'] = sub_category
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Order Date` ORDER BY `Order Date` DESC"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df["year"] = df["Order Date"].dt.year

        df = df.groupby("year").agg({"Total_Sales": "sum", "Total_Profit": "sum"}).reset_index()
        df["Profit_margin"] = df.apply(lambda row: row['Total_Profit'] / row['Total_Sales'] if row['Total_Sales'] > 0 else 0, axis=1)
        return df.to_dict(orient="records")


    def sales_profit_profit_margin_year_on_year_growth(self, ship_mode=None, country=None, city=None,
                                state=None, region=None, category=None, sub_category=None, segment=None):

        query = """
                    SELECT `Order Date`, SUM(Sales) as Total_Sales, SUM(Profit) as Total_Profit
                    FROM superstore
                """

        conditions = []
        params = {}
        if ship_mode:
            conditions.append("`Ship Mode` = :ship_mode")
            params['ship_mode'] = ship_mode
        if country:
            conditions.append("Country = :country")
            params['country'] = country
        if city:
            conditions.append("City = :city")
            params['city'] = city
        if state:
            conditions.append("State = :state")
            params['state'] = state
        if region:
            conditions.append("Region = :region")
            params['region'] = region
        if category:
            conditions.append("Category = :category")
            params['category'] = category
        if sub_category:
            conditions.append("`Sub-Category` = :sub_category")
            params['sub_category'] = sub_category
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Order Date` ORDER BY `Order Date` DESC"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df["year"] = df["Order Date"].dt.year

        df = df.groupby("year").agg({"Total_Sales": "sum", "Total_Profit": "sum"}).reset_index()
        df["Profit_margin"] = df.apply(lambda row: row['Total_Profit'] / row['Total_Sales'] if row['Total_Sales'] > 0 else 0, axis=1)

        df["Sales_YoY_Growth"] = df["Total_Sales"].pct_change() * 100
        df["Profit_YoY_Growth"] = df["Total_Profit"].pct_change() * 100
        df["Profit_margin_YoY_Growth"] = df["Profit_margin"].pct_change() * 100

        return df[["Sales_YoY_Growth", "Profit_YoY_Growth", "Profit_margin_YoY_Growth", "year"]].to_dict(orient="records")


    def sales_profit_profit_margin_per_region(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None,
                                state=None, category=None, sub_category=None, segment=None):
        query = """
            SELECT Region, `Order Date`, SUM(Sales) as Total_Sales, SUM(Profit) as Total_Profit
            FROM superstore
        """

        conditions = []
        params = {}
        if start_date:
            conditions.append("`Order Date` >= :start_date")
            params['start_date'] = start_date
        if end_date:
            conditions.append("`Order Date` <= :end_date")
            params['end_date'] = end_date
        if ship_mode:
            conditions.append("`Ship Mode` = :ship_mode")
            params['ship_mode'] = ship_mode
        if country:
            conditions.append("Country = :country")
            params['country'] = country
        if city:
            conditions.append("City = :city")
            params['city'] = city
        if state:
            conditions.append("State = :state")
            params['state'] = state
        if category:
            conditions.append("Category = :category")
            params['category'] = category
        if sub_category:
            conditions.append("`Sub-Category` = :sub_category")
            params['sub_category'] = sub_category
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Region`, `Order Date` ORDER BY `Order Date` DESC"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        # Convert date column to datetime objects for consistent handling
        df['Order Date'] = pd.to_datetime(df['Order Date'])

        df["Profit_margin"] = df.apply(lambda row: row['Total_Profit'] / row['Total_Sales'] if row['Total_Sales'] > 0 else 0, axis=1)

        return df.to_dict(orient="records")


    def sales_profit_profit_margin_per_region_per_year(self, ship_mode=None, country=None, city=None,
                                state=None, category=None, sub_category=None, segment=None):

        query = """
                    SELECT Region, `Order Date`, SUM(Sales) as Total_Sales, SUM(Profit) as Total_Profit
                    FROM superstore
                """

        conditions = []
        params = {}
        if ship_mode:
            conditions.append("`Ship Mode` = :ship_mode")
            params['ship_mode'] = ship_mode
        if country:
            conditions.append("Country = :country")
            params['country'] = country
        if city:
            conditions.append("City = :city")
            params['city'] = city
        if state:
            conditions.append("State = :state")
            params['state'] = state
        if category:
            conditions.append("Category = :category")
            params['category'] = category
        if sub_category:
            conditions.append("`Sub-Category` = :sub_category")
            params['sub_category'] = sub_category
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Region`, `Order Date` ORDER BY `Order Date` DESC"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df["year"] = df["Order Date"].dt.year

        df = df.groupby(["year", "Region"]).agg({"Total_Sales": "sum", "Total_Profit": "sum"}).reset_index()
        df["Profit_margin"] = df.apply(lambda row: row['Total_Profit'] / row['Total_Sales'] if row['Total_Sales'] > 0 else 0, axis=1)
        return df.to_dict(orient="records")

    def sales_profit_profit_margin_per_category(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None, state=None,
                             region=None, segment=None):

        query = """
            SELECT Category, `Order Date`, SUM(Sales) as Total_Sales, SUM(Profit) as Total_Profit
            FROM superstore
        """

        conditions = []
        params = {}
        if start_date:
            conditions.append("`Order Date` >= :start_date")
            params['start_date'] = start_date
        if end_date:
            conditions.append("`Order Date` <= :end_date")
            params['end_date'] = end_date
        if ship_mode:
            conditions.append("`Ship Mode` = :ship_mode")
            params['ship_mode'] = ship_mode
        if country:
            conditions.append("Country = :country")
            params['country'] = country
        if city:
            conditions.append("City = :city")
            params['city'] = city
        if state:
            conditions.append("State = :state")
            params['state'] = state
        if region:
            conditions.append("Region = :region")
            params['region'] = region
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Category`, `Order Date` ORDER BY `Order Date` DESC"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        df['Order Date'] = pd.to_datetime(df['Order Date'])

        df["Profit_margin"] = df.apply(lambda row: row['Total_Profit'] / row['Total_Sales'] if row['Total_Sales'] > 0 else 0, axis=1)

        return df.to_dict(orient="records")


    def sales_profit_profit_margin_per_category_per_year(self, ship_mode=None, country=None, city=None, state=None,
                             region=None, segment=None):

        query = """
                    SELECT Category, `Order Date`, SUM(Sales) as Total_Sales, SUM(Profit) as Total_Profit
                    FROM superstore
                """

        conditions = []
        params = {}
        if ship_mode:
            conditions.append("`Ship Mode` = :ship_mode")
            params['ship_mode'] = ship_mode
        if country:
            conditions.append("Country = :country")
            params['country'] = country
        if city:
            conditions.append("City = :city")
            params['city'] = city
        if state:
            conditions.append("State = :state")
            params['state'] = state
        if region:
            conditions.append("Region = :region")
            params['region'] = region
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Category`, `Order Date` ORDER BY `Order Date` DESC"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df["year"] = df["Order Date"].dt.year

        df = df.groupby(["year", "Category"]).agg({"Total_Sales": "sum", "Total_Profit": "sum"}).reset_index()
        df["Profit_margin"] = df.apply(lambda row: row['Total_Profit'] / row['Total_Sales'] if row['Total_Sales'] > 0 else 0, axis=1)
        return df.to_dict(orient="records")

    def profit_per_unit_product_in_category(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None, state=None,
                             region=None, segment=None):

        query = """
            SELECT Category, `Order Date`, SUM(Profit) as Total_Profit, SUM(Quantity) as Quantity
            FROM superstore
        """

        conditions = []
        params = {}
        if start_date:
            conditions.append("`Order Date` >= :start_date")
            params['start_date'] = start_date
        if end_date:
            conditions.append("`Order Date` <= :end_date")
            params['end_date'] = end_date
        if ship_mode:
            conditions.append("`Ship Mode` = :ship_mode")
            params['ship_mode'] = ship_mode
        if country:
            conditions.append("Country = :country")
            params['country'] = country
        if city:
            conditions.append("City = :city")
            params['city'] = city
        if state:
            conditions.append("State = :state")
            params['state'] = state
        if region:
            conditions.append("Region = :region")
            params['region'] = region
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment

        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " GROUP BY `Category`, `Order Date` ORDER BY `Order Date` DESC"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)
        df["ppupc"] = df.apply(lambda row: row['Total_Profit'] / row['Quantity'] if row['Quantity'] > 0 else 0, axis=1)

        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df['year'] = df['Order Date'].dt.year
        df = df.groupby(['year', 'Category']).agg({'ppupc': 'sum'}).reset_index()

        return df.to_dict(orient="records")