from sqlalchemy import text

from src.db_connection.connection import DBConnection


class Utils:
    def __init__(self):
        self.db_connection = DBConnection()
        self.engine = self.db_connection.create_db_connection()

    def get_state(self):
        query = """
            SELECT DISTINCT State
            FROM superstore;
        """
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            states = [row[0] for row in result]

        return states

    def get_ship_mode(self):
        query = """
            SELECT DISTINCT `Ship Mode`
            FROM superstore;
        """
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            states = [row[0] for row in result]

        return states

    def get_city(self):
        query = """
            SELECT DISTINCT City
            FROM superstore;
        """
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            states = [row[0] for row in result]

        return states

    def get_region(self):
        query = """
            SELECT DISTINCT Region
            FROM superstore;
        """
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            states = [row[0] for row in result]

        return states

    def get_country(self):
        query = """
            SELECT DISTINCT Country
            FROM superstore;
        """
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            states = [row[0] for row in result]

        return states

    def get_category(self):
        query = """
            SELECT DISTINCT Category
            FROM superstore;
        """
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            states = [row[0] for row in result]

        return states

    def get_segment(self):
        query = """
            SELECT DISTINCT Segment
            FROM superstore;
        """
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            states = [row[0] for row in result]

        return states
