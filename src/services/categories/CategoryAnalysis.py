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

        query += " GROUP BY `Category`"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def category_sales_per_year(self, ship_mode=None, country=None, city=None, state=None,
                                region=None, segment=None):

        query = """
            SELECT YEAR(`Order Date`) AS Year, `Category`, SUM(`Sales`) AS Total_Sales
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

        query += " GROUP BY Year, `Category`"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def category_profit_per_year(self, ship_mode=None, country=None, city=None, state=None,
                         region=None, segment=None):

        query = """
            SELECT YEAR(`Order Date`) AS Year, `Category`, SUM(`Profit`) AS Total_Profits
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

        query += " GROUP BY Year, `Category`"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def category_sales_and_profit_count(self, ship_mode=None, country=None, city=None, state=None,
                             region=None, segment=None):
        query = """
        SELECT `Category`, SUM(`Sales`) AS Total_Sales, SUM(`Profit`) AS Total_Profits
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

        query += " GROUP BY `Category`"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')