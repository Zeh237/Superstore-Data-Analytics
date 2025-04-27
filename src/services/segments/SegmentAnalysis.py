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
            params['category'] = category
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

    def total_profit_per_segment(self, ship_mode=None, country=None, city=None,
                                 state=None, regions=None, category=None, start_date=None, end_date=None):
        query = """
        SELECT Segment, SUM(Profit) AS total_profit
        FROM superstore
        WHERE 1=1
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
        if regions:
            conditions.append("Region = :region")
            params['region'] = regions
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += " GROUP BY Segment"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def profit_margin_per_segment(self, ship_mode=None, country=None, city=None,
                                  state=None, regions=None, category=None, start_date=None, end_date=None):
        query = """
        SELECT Segment, SUM(Profit)/SUM(Sales) AS profit_margin
        FROM superstore
        WHERE 1=1
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
        if regions:
            conditions.append("Region = :region")
            params['region'] = regions
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += " GROUP BY Segment"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def average_profit_per_order_per_segment(self, ship_mode=None, country=None, city=None,
                                             state=None, regions=None, category=None, start_date=None, end_date=None):
        query = """
        WITH OrderSummary AS (
            SELECT `Order ID`, Segment, SUM(Profit) AS order_profit
            FROM superstore
            WHERE 1=1
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
        if regions:
            conditions.append("Region = :region")
            params['region'] = regions
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += """
            GROUP BY `Order ID`, Segment
        )

        SELECT Segment, AVG(order_profit) AS average_profit_per_order
        FROM OrderSummary
        GROUP BY Segment
        """

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def total_quantity_per_segment(self, ship_mode=None, country=None, city=None,
                                   state=None, regions=None, category=None, start_date=None, end_date=None):
        query = """
        SELECT Segment, SUM(Quantity) AS total_quantity
        FROM superstore
        WHERE 1=1
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
        if regions:
            conditions.append("Region = :region")
            params['region'] = regions
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += " GROUP BY Segment"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def number_of_orders_per_segment(self, ship_mode=None, country=None, city=None,
                                     state=None, regions=None, category=None, start_date=None, end_date=None):
        query = """
        SELECT Segment, COUNT(DISTINCT `Order ID`) AS order_count
        FROM superstore
        WHERE 1=1
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
        if regions:
            conditions.append("Region = :region")
            params['region'] = regions
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += " GROUP BY Segment"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def average_quantity_per_order_per_segment(self, ship_mode=None, country=None, city=None,
                                               state=None, regions=None, category=None, start_date=None, end_date=None):
        query = """
        SELECT Segment, SUM(Quantity)*1.0/COUNT(DISTINCT `Order ID`) AS avg_quantity_per_order
        FROM superstore
        WHERE 1=1
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
        if regions:
            conditions.append("Region = :region")
            params['region'] = regions
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += " GROUP BY Segment"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def breakdown_by_ship_mode_per_segment(self, ship_mode=None, country=None, city=None,
                                           state=None, regions=None, category=None, start_date=None, end_date=None):
        query = """
        SELECT Segment, `Ship Mode`, SUM(Sales) as sales
        FROM superstore
        WHERE 1=1
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
        if regions:
            conditions.append("Region = :region")
            params['region'] = regions
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += " GROUP BY Segment, `Ship Mode`"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def breakdown_by_region_per_segment(self, ship_mode=None, country=None, city=None,
                                        state=None, regions=None, category=None, start_date=None, end_date=None):
        query = """
        SELECT Segment, Region, SUM(Sales) as sales
        FROM superstore
        WHERE 1=1
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
        if regions:
            conditions.append("Region = :region")
            params['region'] = regions
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += " GROUP BY Segment, Region"

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def top_n_products_per_segment(self, n=1, ship_mode=None, country=None, city=None,
                                   state=None, regions=None, category=None, start_date=None, end_date=None):
        query = """
        WITH ProductSales AS (
            SELECT Segment, `Product Name`, SUM(Sales) as total_sales
            FROM superstore
            WHERE 1=1
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
        if regions:
            conditions.append("Region = :region")
            params['region'] = regions
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += """
            GROUP BY Segment, `Product Name`
        ),
        RankedProducts AS (
            SELECT Segment, `Product Name`, total_sales,
                   RANK() OVER (PARTITION BY Segment ORDER BY total_sales DESC) as p_rank
            FROM ProductSales
        )
        SELECT Segment, `Product Name`, total_sales
        FROM RankedProducts
        WHERE p_rank <= :n
        ORDER BY Segment, p_rank
        """

        params['n'] = n

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def top_n_customers_per_segment(self, n=1, ship_mode=None, country=None, city=None,
                                    state=None, regions=None, category=None, start_date=None, end_date=None):
        query = """
        WITH CustomerSales AS (
            SELECT Segment, `Customer ID`, SUM(Sales) as total_sales
            FROM superstore
            WHERE 1=1
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
        if regions:
            conditions.append("Region = :region")
            params['region'] = regions
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += """
            GROUP BY Segment, `Customer ID`
        ),
        RankedCustomers AS (
            SELECT Segment, `Customer ID`, total_sales,
                   RANK() OVER (PARTITION BY Segment ORDER BY total_sales DESC) as s_rank
            FROM CustomerSales
        )
        SELECT Segment, `Customer ID`, total_sales
        FROM RankedCustomers
        WHERE s_rank <= :n
        ORDER BY Segment, s_rank
        """

        params['n'] = n

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')

    def year_over_year_growth_per_segment(self, ship_mode=None, country=None, city=None,
                                          state=None, regions=None, category=None, start_date=None, end_date=None):
        query = """
        WITH YearlySales AS (
            SELECT Segment, YEAR(`Order Date`) as year, SUM(Sales) as total_sales
            FROM superstore
            WHERE 1=1
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
        if regions:
            conditions.append("Region = :region")
            params['region'] = regions
        if category:
            conditions.append("Category = :category")
            params['category'] = category

        if conditions:
            query += " AND " + " AND ".join(conditions)

        query += """
            GROUP BY Segment, YEAR(`Order Date`)
        )
        SELECT 
            current.Segment,
            current.year,
            current.total_sales,
            previous.total_sales as previous_year_sales,
            CASE 
                WHEN previous.total_sales IS NULL THEN NULL
                ELSE (current.total_sales - previous.total_sales) / previous.total_sales
            END as growth_rate
        FROM YearlySales current
        LEFT JOIN YearlySales previous
          ON current.Segment = previous.Segment
         AND current.year = previous.year + 1
        ORDER BY current.Segment, current.year
        """

        with self.engine.connect() as connection:
            df = pd.read_sql(text(query), connection, params=params)

        return df.to_dict(orient='records')
