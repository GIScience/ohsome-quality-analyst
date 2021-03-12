import os
import unittest

from psycopg2._psycopg import connection as psycopg_connection
from psycopg2._psycopg import cursor as psycopg_cursor
from psycopg2.errors import OperationalError

from ohsome_quality_analyst.geodatabase.auth import PostgresDB


class TestPostgres(unittest.TestCase):
    def test_connection(self):
        os.unsetenv("POSTGRES_HOST")  # Unset variable for the use of this script
        os.unsetenv("POSTGRES_PORT")
        os.unsetenv("POSTGRES_DB")
        os.unsetenv("POSTGRES_USER")
        os.unsetenv("POSTGRES_PASSWORD")
        db_client = PostgresDB()
        self.assertIsInstance(db_client._connection, psycopg_connection)
        self.assertIsInstance(db_client._cursor, psycopg_cursor)

    def test_connection_fails(self):
        os.environ["POSTGRES_HOST"] = ""
        os.environ["POSTGRES_PORT"] = ""
        os.environ["POSTGRES_DB"] = ""
        os.environ["POSTGRES_USER"] = ""
        os.environ["POSTGRES_PASSWORD"] = ""
        with self.assertRaises(OperationalError):
            PostgresDB()


if __name__ == "__main__":
    unittest.main()