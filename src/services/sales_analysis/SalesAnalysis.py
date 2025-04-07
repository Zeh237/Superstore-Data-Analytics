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
            WHERE 
                1=1
        """

        if start_date:
            query += f" AND `Order Date` >= '{start_date}'"
        if end_date:
            query += f" AND `Order Date` <= '{end_date}'"
        if ship_mode:
            query += f" AND `Ship Mode` = '{ship_mode}'"
        if country:
            query += f" AND Country = '{country}'"
        if city:
            query += f" AND City = '{city}'"
        if state:
            query += f" AND State = '{state}'"
        if region:
            query += f" AND Region = '{region}'"
        if category:
            query += f" AND Category = '{category}'"
        if sub_category:
            query += f" AND `Sub-Category` = '{sub_category}'"
        if segment:
            query += f" AND Segment = '{segment}'"

        with self.engine.connect() as connection:
            result = connection.execute(text(query))
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
        if start_date:
            conditions.append(f"`Order Date` >= '{start_date}'")
        if end_date:
            conditions.append(f"`Order Date` <= '{end_date}'")
        if ship_mode:
            conditions.append(f"`Ship Mode` = '{ship_mode}'")
        if country:
            conditions.append(f"Country = '{country}'")
        if city:
            conditions.append(f"City = '{city}'")
        if state:
            conditions.append(f"State = '{state}'")
        if region:
            conditions.append(f"Region = '{region}'")
        if category:
            conditions.append(f"Category = '{category}'")
        if sub_category:
            conditions.append(f"`Sub-Category` = '{sub_category}'")
        if segment:
            conditions.append(f"Segment = '{segment}'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Order Date` ORDER BY 'Order Date' Desc"

        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            sales_data = [{"date": row[0], "sales": row[1]} for row in result.fetchall()]
            return sales_data


    def profits_over_time(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None,
                                state=None, region=None, category=None, sub_category=None, segment=None):

        query = """
                    SELECT `Order Date`, SUM(Profit) as Total_Sales
                    FROM superstore
                """

        conditions = []
        if start_date:
            conditions.append(f"`Order Date` >= '{start_date}'")
        if end_date:
            conditions.append(f"`Order Date` <= '{end_date}'")
        if ship_mode:
            conditions.append(f"`Ship Mode` = '{ship_mode}'")
        if country:
            conditions.append(f"Country = '{country}'")
        if city:
            conditions.append(f"City = '{city}'")
        if state:
            conditions.append(f"State = '{state}'")
        if region:
            conditions.append(f"Region = '{region}'")
        if category:
            conditions.append(f"Category = '{category}'")
        if sub_category:
            conditions.append(f"`Sub-Category` = '{sub_category}'")
        if segment:
            conditions.append(f"Segment = '{segment}'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Order Date` ORDER BY 'Order Date' Desc"

        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            profit_data = [{"date": row[0], "profit": row[1]} for row in result.fetchall()]
            return profit_data


    def profit_margins_over_time(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None,
                                state=None, region=None, category=None, sub_category=None, segment=None):

        query = """
            SELECT 'Order Date', SUM(Profit) as profit, SUM(Sales) as sales
            FROM superstore
        """

        conditions = []
        if start_date:
            conditions.append(f"`Order Date` >= '{start_date}'")
        if end_date:
            conditions.append(f"`Order Date` <= '{end_date}'")
        if ship_mode:
            conditions.append(f"`Ship Mode` = '{ship_mode}'")
        if country:
            conditions.append(f"Country = '{country}'")
        if city:
            conditions.append(f"City = '{city}'")
        if state:
            conditions.append(f"State = '{state}'")
        if region:
            conditions.append(f"Region = '{region}'")
        if category:
            conditions.append(f"Category = '{category}'")
        if sub_category:
            conditions.append(f"`Sub-Category` = '{sub_category}'")
        if segment:
            conditions.append(f"Segment = '{segment}'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Order Date` ORDER BY 'Order Date' Desc"

        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            profit_margin_data = [{"date": row[0], "profit": row[1], "sales": row[2], "profit_margin": row[1]/row[2]} for row in result.fetchall()]
            return profit_margin_data


    def sales_profit_profit_margin_per_year(self, ship_mode=None, country=None, city=None,
                                state=None, region=None, category=None, sub_category=None, segment=None):
        query = """
            SELECT `Order Date`, SUM(Sales) as Total_Sales, SUM(Profit) as Total_Profit
            FROM superstore
        """

        conditions = []
        if ship_mode:
            conditions.append(f"`Ship Mode` = '{ship_mode}'")
        if country:
            conditions.append(f"Country = '{country}'")
        if city:
            conditions.append(f"City = '{city}'")
        if state:
            conditions.append(f"State = '{state}'")
        if region:
            conditions.append(f"Region = '{region}'")
        if category:
            conditions.append(f"Category = '{category}'")
        if sub_category:
            conditions.append(f"`Sub-Category` = '{sub_category}'")
        if segment:
            conditions.append(f"Segment = '{segment}'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Order Date` ORDER BY 'Order Date' Desc"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection)

        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df["year"] = df["Order Date"].dt.year

        df = df.groupby("year").agg({"Total_Sales": "sum", "Total_Profit": "sum"}).reset_index()
        df["Profit_margin"] = df["Total_Profit"] / df["Total_Sales"]
        return df.to_dict(orient="records")


    def sales_profit_profit_margin_year_on_year_growth(self, ship_mode=None, country=None, city=None,
                                state=None, region=None, category=None, sub_category=None, segment=None):

        query = """
                    SELECT `Order Date`, SUM(Sales) as Total_Sales, SUM(Profit) as Total_Profit
                    FROM superstore
                """

        conditions = []
        if ship_mode:
            conditions.append(f"`Ship Mode` = '{ship_mode}'")
        if country:
            conditions.append(f"Country = '{country}'")
        if city:
            conditions.append(f"City = '{city}'")
        if state:
            conditions.append(f"State = '{state}'")
        if region:
            conditions.append(f"Region = '{region}'")
        if category:
            conditions.append(f"Category = '{category}'")
        if sub_category:
            conditions.append(f"`Sub-Category` = '{sub_category}'")
        if segment:
            conditions.append(f"Segment = '{segment}'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Order Date` ORDER BY 'Order Date' Desc"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection)

        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df["year"] = df["Order Date"].dt.year

        df = df.groupby("year").agg({"Total_Sales": "sum", "Total_Profit": "sum"}).reset_index()
        df["Profit_margin"] = df["Total_Profit"] / df["Total_Sales"]

        df["Sales_YoY_Growth"] = df["Total_Sales"].pct_change() * 100
        df["Profit_YoY_Growth"] = df["Total_Profit"].pct_change() * 100
        df["Profit_margin_YoY_Growth"] = df["Profit_margin"].pct_change() * 100

        return df[["Total_Sales", "Total_Profit", "Profit_margin", "Sales_YoY_Growth", "Profit_YoY_Growth", "Profit_margin_YoY_Growth"]].to_dict(orient="records")


    def sales_profit_profit_margin_per_region(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None,
                                state=None, category=None, sub_category=None, segment=None):
        query = """
            SELECT Region, `Order Date`, SUM(Sales) as Total_Sales, SUM(Profit) as Total_Profit
            FROM superstore
        """

        conditions = []
        if start_date:
            conditions.append(f"`Order Date` >= '{start_date}'")
        if end_date:
            conditions.append(f"`Order Date` <= '{end_date}'")
        if ship_mode:
            conditions.append(f"`Ship Mode` = '{ship_mode}'")
        if country:
            conditions.append(f"Country = '{country}'")
        if city:
            conditions.append(f"City = '{city}'")
        if state:
            conditions.append(f"State = '{state}'")
        if category:
            conditions.append(f"Category = '{category}'")
        if sub_category:
            conditions.append(f"`Sub-Category` = '{sub_category}'")
        if segment:
            conditions.append(f"Segment = '{segment}'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Region`, `Order Date` ORDER BY `Order Date` Desc"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection)

        return df.to_dict(orient="records")


    def sales_profit_profit_margin_per_region_per_year(self, ship_mode=None, country=None, city=None,
                                state=None, category=None, sub_category=None, segment=None):

        query = """
                    SELECT Region, `Order Date`, SUM(Sales) as Total_Sales, SUM(Profit) as Total_Profit
                    FROM superstore
                """

        conditions = []
        if ship_mode:
            conditions.append(f"`Ship Mode` = '{ship_mode}'")
        if country:
            conditions.append(f"Country = '{country}'")
        if city:
            conditions.append(f"City = '{city}'")
        if state:
            conditions.append(f"State = '{state}'")
        if category:
            conditions.append(f"Category = '{category}'")
        if sub_category:
            conditions.append(f"`Sub-Category` = '{sub_category}'")
        if segment:
            conditions.append(f"Segment = '{segment}'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Region`, `Order Date` ORDER BY `Order Date` Desc"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection)

        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df["year"] = df["Order Date"].dt.year

        df = df.groupby("year").agg({"Total_Sales": "sum", "Total_Profit": "sum"}).reset_index()
        df["Profit_margin"] = df["Total_Profit"] / df["Total_Sales"]
        return df.to_dict(orient="records")

    def sales_profit_profit_margin_per_category(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None, state=None,
                             region=None, segment=None):

        query = """
            SELECT Category, `Order Date`, SUM(Sales) as Total_Sales, SUM(Profit) as Total_Profit
            FROM superstore
        """

        conditions = []
        if start_date:
            conditions.append(f"`Order Date` >= '{start_date}'")
        if end_date:
            conditions.append(f"`Order Date` <= '{end_date}'")
        if ship_mode:
            conditions.append(f"`Ship Mode` = '{ship_mode}'")
        if country:
            conditions.append(f"Country = '{country}'")
        if city:
            conditions.append(f"City = '{city}'")
        if state:
            conditions.append(f"State = '{state}'")
        if region:
            conditions.append(f"Region = '{region}'")
        if segment:
            conditions.append(f"Segment = '{segment}'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Category`, `Order Date` ORDER BY `Order Date` Desc"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection)

        return df.to_dict(orient="records")


    def sales_profit_profit_margin_per_category_per_year(self, ship_mode=None, country=None, city=None, state=None,
                             region=None, segment=None):

        query = """
                    SELECT Category, `Order Date`, SUM(Sales) as Total_Sales, SUM(Profit) as Total_Profit
                    FROM superstore
                """

        conditions = []
        if ship_mode:
            conditions.append(f"`Ship Mode` = '{ship_mode}'")
        if country:
            conditions.append(f"Country = '{country}'")
        if city:
            conditions.append(f"City = '{city}'")
        if state:
            conditions.append(f"State = '{state}'")
        if region:
            conditions.append(f"Region = '{region}'")
        if segment:
            conditions.append(f"Segment = '{segment}'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Category`, `Order Date` ORDER BY `Order Date` Desc"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection)

        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df["year"] = df["Order Date"].dt.year

        df = df.groupby("year").agg({"Total_Sales": "sum", "Total_Profit": "sum"}).reset_index()
        df["Profit_margin"] = df["Total_Profit"] / df["Total_Sales"]
        return df.to_dict(orient="records")

    def profit_per_unit_per_unit_product_in_category(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None, state=None,
                             region=None, segment=None):

        query = """
            SELECT Category, `Order Date`, SUM(Profit) as Total_Profit, SUM(Quantity) as Quantity
            FROM superstore
        """

        conditions = []
        if start_date:
            conditions.append(f"`Order Date` >= '{start_date}'")
        if end_date:
            conditions.append(f"`Order Date` <= '{end_date}'")
        if ship_mode:
            conditions.append(f"`Ship Mode` = '{ship_mode}'")
        if country:
            conditions.append(f"Country = '{country}'")
        if city:
            conditions.append(f"City = '{city}'")
        if state:
            conditions.append(f"State = '{state}'")
        if region:
            conditions.append(f"Region = '{region}'")
        if segment:
            conditions.append(f"Segment = '{segment}'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Category`, `Order Date` ORDER BY `Order Date` Desc"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection)

        df["ppupc"] = df['Total_Profit']/df['Quantity']
        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df['year'] = df['Order Date'].dt.year
        df = df.groupby(['year', 'Category']).agg({'ppupc': 'sum'}).reset_index()

        return df.to_dict(orient="records")

# sales_analytics = SalesAnalysis()
# s = SalesAnalysis()
# print(s.sales_over_time(category="Office Supplies", start_date="2014-01-01", end_date="2017-12-31"))
# print(s.profits_over_time(category="Office Supplies", start_date="2014-01-01", end_date="2017-12-31"))
# print(s.sales_and_profit_sum(start_date="2014-01-01", end_date="2017-12-31"))
# print(s.sales_profit_profit_margin_per_year())
# print(s.profit_margins_over_time())
# print(s.sales_profit_profit_margin_year_on_year_growth())
# print(s.sales_profit_profit_margin_per_region_per_year())
# print(s.sales_profit_profit_margin_per_category())
# print(s.sales_profit_profit_margin_per_category_per_year())
# print(s.profit_per_unit_per_unit_product_in_category())