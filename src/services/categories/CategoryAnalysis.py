import pandas as pd
from sqlalchemy import text

from src.db_connection.connection import DBConnection


class CategoryAnalysis:
    def __init__(self):
        self.db_connection = DBConnection()
        self.engine = self.db_connection.create_db_connection()

    def top_selling_categories(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None,
                               state=None,
                               region=None, segment=None):
        query = """
            SELECT `Category`, SUM(`Sales`) AS Total_Sales, SUM(Profit) as Total_Profits
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

        query += " GROUP BY `Category`"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection)

        return df.to_dict(orient='records')

    def category_sales_per_year(self, ship_mode=None, country=None, city=None, state=None,
                                region=None, segment=None):

        query = """
            SELECT YEAR(`Order Date`) AS Year, `Category`, SUM(`Sales`) AS Total_Sales
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

        query += " GROUP BY Year, `Category`"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection)

        return df.to_dict(orient='records')

    def category_profit_per_year(self, ship_mode=None, country=None, city=None, state=None,
                             region=None, segment=None):

        query = """
                    SELECT YEAR(`Order Date`) AS Year, `Category`, SUM(`Profit`) AS Total_Profits
                    FROM superstore
                    GROUP BY Year, `Category`
                """

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
        if segment:
            query += f" AND Segment = '{segment}'"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection)

        return df.to_dict(orient='records')

    def category_sales_and_profit_count(self, ship_mode=None, country=None, city=None, state=None,
                             region=None, segment=None):
        query = """
        SELECT `Category`, SUM(`Sales`) AS Total_Sales, SUM(`Profit`) AS Total_Profits
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

        query += " GROUP BY `Category`"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection)

        return df.to_dict(orient='records')


s=CategoryAnalysis()
print(s.category_sales_and_profit_count(region='East'))