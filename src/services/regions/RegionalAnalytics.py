import pandas as pd
from sqlalchemy import text

from src.db_connection.connection import DBConnection


class RegionalAnalytics:
    def __init__(self):
        self.db_connection = DBConnection()
        # Assuming create_db_connection returns a SQLAlchemy engine
        self.engine = self.db_connection.create_db_connection()

    def regional_sales_per_year(self, ship_mode=None, country=None, city=None,
                               state=None, segment=None, category=None):
        query = """
            SELECT Region, SUM(Sales) as Total_Sales
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
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Region`"

        with self.engine.connect() as connection:
            # Pass params to read_sql when using parameterized queries
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def regional_profits_per_year(self, ship_mode=None, country=None, city=None,
                               state=None, segment=None, category=None):
        query = """
            SELECT Region, SUM(Profit) as Total_Profits
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
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Region`"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def top_selling_regions(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None,
                               state=None,
                               category=None, segment=None):
        query = """
            SELECT `Region`, SUM(`Sales`) AS Total_Sales, SUM(Profit) as Total_Profits
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
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Region` ORDER BY Total_Sales DESC"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def top_city_per_region(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None,
                            state=None,
                            category=None, segment=None):
        query = """
            WITH RegionalCitySales AS (
                SELECT
                    Region,
                    City,
                    SUM(Sales) AS Total_Sales,
                    -- Assign a rank to cities within each region based on sales
                    ROW_NUMBER() OVER(PARTITION BY Region ORDER BY SUM(Sales) DESC) as rn
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
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += """
                GROUP BY Region, City -- Group by Region and City to calculate sales per city per region
            )
            SELECT
                Region,
                City AS Top_Selling_City,
                Total_Sales AS Total_Sales_In_City
            FROM RegionalCitySales
            WHERE rn = 1; -- Select only the city with rank 1 for each region
        """

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')


    def regional_profit_margin(self, ship_mode=None, country=None, city=None,
                               state=None, segment=None, category=None):
        query = """
            SELECT
                Region,
                SUM(Profit) / SUM(Sales) AS Profit_Margin
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
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += """
            GROUP BY Region
            HAVING SUM(Sales) > 0 -- Ensure sales are positive to calculate margin
        """

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def regional_quantity_sold(self, ship_mode=None, country=None, city=None,
                               state=None, segment=None, category=None):

        query = """
            SELECT Region, SUM(Quantity) as Total_Quantity
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
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Region`"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def regional_order_count(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None,
                             state=None, segment=None, category=None):
        query = """
            SELECT Region, COUNT(DISTINCT `Order ID`) as Total_Orders
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
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Region`"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def regional_unique_customer_count(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None,
                                       state=None, segment=None, category=None):
        query = """
            SELECT Region, COUNT(DISTINCT `Customer ID`) as Unique_Customers
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
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Region`"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def regional_average_order_value(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None,
                                     state=None, segment=None, category=None):

        query = """
            SELECT Region, SUM(Sales) / COUNT(DISTINCT `Order ID`) as Average_Order_Value
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
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += """
            GROUP BY `Region`
            HAVING COUNT(DISTINCT `Order ID`) > 0 -- Ensure there is at least one order
        """

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def regional_average_profit_per_order(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None,
                                          state=None, segment=None, category=None):

        query = """
            SELECT Region, SUM(Profit) / COUNT(DISTINCT `Order ID`) as Average_Profit_Per_Order
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
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += """
            GROUP BY `Region`
            HAVING COUNT(DISTINCT `Order ID`) > 0 -- Ensure there is at least one order
        """

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def regional_average_discount(self, ship_mode=None, country=None, city=None,
                                  state=None, segment=None, category=None):

        query = """
            SELECT Region, AVG(Discount) as Average_Discount
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
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY `Region`"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def top_category_per_region(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None,
                                state=None, segment=None):

        query = """
            WITH RegionalCategorySales AS (
                SELECT
                    Region,
                    Category,
                    SUM(Sales) AS Total_Sales,
                    -- Assign a rank to categories within each region based on sales
                    ROW_NUMBER() OVER(PARTITION BY Region ORDER BY SUM(Sales) DESC) as rn
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
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += """
                GROUP BY Region, Category -- Group by Region and Category to calculate sales per category per region
            )
            SELECT
                Region,
                Category AS Top_Selling_Category,
                Total_Sales AS Total_Sales_In_Category
            FROM RegionalCategorySales
            WHERE rn = 1; -- Select only the category with rank 1 for each region
        """

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def top_subcategory_per_region(self, start_date=None, end_date=None, ship_mode=None, country=None, city=None,
                                   state=None, segment=None, category=None):

        query = """
            WITH RegionalSubCategorySales AS (
                SELECT
                    Region,
                    `Sub-Category`, -- Assuming 'Sub-Category' column name
                    SUM(Sales) AS Total_Sales,
                    -- Assign a rank to sub-categories within each region based on sales
                    ROW_NUMBER() OVER(PARTITION BY Region ORDER BY SUM(Sales) DESC) as rn
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
        if segment:
            conditions.append("Segment = :segment")
            params['segment'] = segment
        if category:
             conditions.append("Category = :category")
             params['category'] = category

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += """
                GROUP BY Region, `Sub-Category` -- Group by Region and Sub-Category to calculate sales per sub-category per region
            )
            SELECT
                Region,
                `Sub-Category` AS Top_Selling_Sub_Category,
                Total_Sales AS Total_Sales_In_Sub_Category
            FROM RegionalSubCategorySales
            WHERE rn = 1; -- Select only the sub-category with rank 1 for each region
        """

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

s = RegionalAnalytics()
print(s.regional_sales_per_year())