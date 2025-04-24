from sqlalchemy import text

from src.db_connection.connection import DBConnection
import pandas as pd

class Segments:
    def __init__(self):
        self.db_connection = DBConnection()
        self.engine = self.db_connection.create_db_connection()

    def segment_performance_per_year(self, ship_mode=None, country=None, city=None,
                           state=None, regions=None, category=None):
        query = """
            SELECT YEAR(`Order Date`) AS Year, Segment, SUM(Sales) as sales from superstore
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
        if regions:
            conditions.append("Region = :region")
            params['region'] = regions
        if category:
            conditions.append("Category = :category")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY Year, `Segment`"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def top_selling_category_per_segment(self, ship_mode=None, country=None, city=None,
                                         state=None, regions=None, category=None,
                                         start_date=None, end_date=None):

        query = """
            WITH filtered_data AS (
                SELECT 
                    Segment, 
                    Category,
                    SUM(Sales) as total_sales
                FROM 
                    superstore
                WHERE 
                    1=1
        """

        # Build conditions and parameters
        conditions = []
        params = {}

        # Add all filter conditions
        if start_date:
            conditions.append("`Order Date` >= :start_date")
            params["start_date"] = start_date
        if end_date:
            conditions.append("`Order Date` <= :end_date")
            params["end_date"] = end_date
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
        if regions:
            conditions.append("Region = :region")
            params['region'] = regions
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        # Complete the filtered_data CTE
        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += """
                GROUP BY Segment, Category
            ),
            ranked_categories AS (
                SELECT 
                    Segment,
                    Category,
                    total_sales,
                    RANK() OVER (
                        PARTITION BY Segment 
                        ORDER BY total_sales DESC
                    ) as sales_rank
                FROM 
                    filtered_data
            )
            SELECT 
                Segment,
                Category,
                total_sales as sales
            FROM 
                ranked_categories
            WHERE 
                sales_rank = 1
            ORDER BY 
                Segment
        """

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def top_selling_city_per_segment(self, ship_mode=None, country=None, city=None,
                                     state=None, regions=None, category=None, start_date=None, end_date=None):
        base_query = """
            WITH FilteredData AS (
                SELECT 
                    City, 
                    Segment, 
                    Sales
                FROM 
                    superstore
                WHERE 
                    1=1
        """

        conditions = []
        params = {}
        if start_date:
            conditions.append(" `Order Date` >= :start_date")
            params["start_date"] = start_date
        if end_date:
            conditions.append(" `Order Date` <= :end_date")
            params["end_date"] = end_date
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
        if regions:
            conditions.append("Region = :region")
            params['region'] = regions
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        query = base_query
        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += """
            ),
            RankedCities AS (
                SELECT 
                    City, 
                    Segment, 
                    SUM(Sales) AS sales,
                    RANK() OVER (PARTITION BY Segment ORDER BY SUM(Sales) DESC) AS sales_rank
                FROM 
                    FilteredData
                GROUP BY 
                    Segment, City
            )
            SELECT 
                City, 
                Segment, 
                sales
            FROM 
                RankedCities
            WHERE 
                sales_rank = 1
        """

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def top_selling_state_per_segment(self, ship_mode=None, country=None, city=None,
                                     state=None, regions=None, category=None, start_date=None, end_date=None):
        base_query = """
            WITH FilteredData AS (
                SELECT 
                    State, 
                    Segment, 
                    Sales
                FROM 
                    superstore
                WHERE 
                    1=1
        """

        conditions = []
        params = {}
        if start_date:
            conditions.append(" `Order Date` >= :start_date")
            params["start_date"] = start_date
        if end_date:
            conditions.append(" `Order Date` <= :end_date")
            params["end_date"] = end_date
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
        if regions:
            conditions.append("Region = :region")
            params['region'] = regions
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        query = base_query
        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += """
            ),
            RankedStates AS (
                SELECT 
                    State, 
                    Segment, 
                    SUM(Sales) AS sales,
                    RANK() OVER (PARTITION BY Segment ORDER BY SUM(Sales) DESC) AS sales_rank
                FROM 
                    FilteredData
                GROUP BY 
                    Segment, State
            )
            SELECT 
                State, 
                Segment, 
                sales
            FROM 
                RankedStates
            WHERE 
                sales_rank = 1
        """

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

c = Segments()
print(c.top_selling_state_per_segment())