import os
import unittest
import sqlalchemy
from ETL_Pipeline import ETLPipeline
from sqlalchemy.sql import text

class ETLPipelineTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Testing the ETL Pipeline!")

        # Initialize and execute the ETL pipeline
        cls.pipeline = ETLPipeline()
        cls.transformed_data = cls.pipeline.run('nikhilkohli/us-stock-market-data-60-extracted-features')

        cls.engine = sqlalchemy.create_engine("sqlite:///test_stock_data.db", echo=False)
        cls.connection = cls.engine.connect()

    @classmethod
    def tearDownClass(cls):
    
        #Close the database connection and clean up after all tests.
        
        print("Tearing down the ETL Pipeline test cases...")
        cls.connection.close()
        cls.engine.dispose()

        # Remove the test database file
        if os.path.exists('test_stock_data.db'):
            os.remove('test_stock_data.db')

    def test_database_file_exists(self):
        
        #Test if the SQLite database file is created.
        
        print("Checking if the database file exists!")
        self.assertTrue(
            os.path.exists('test_stock_data.db'),
            "Database file does not exist at the specified path."
        )

    def test_table_exists(self):
        
        #Test if the expected table is created in the database.
        
        print("Checking if the table exists in the database...")
        inspector = sqlalchemy.inspect(self.engine)

        try:
            tables = inspector.get_table_names()
            self.assertIn(
                "amazon_stock_data", tables,
                "Table 'amazon_stock_data' is not found in the database."
            )
        except sqlalchemy.exc.OperationalError:
            self.fail("Could not connect to the database.")

    def test_table_data(self):
        
        #Test if the table contains data.
        
        print("Checking if the table contains data!")
        try:
            result = self.connection.execute(
                text("SELECT COUNT(*) FROM amazon_stock_data")
            ).fetchone()

            # Assert that the table has at least one row
            self.assertGreater(result[0], 0, "Table 'amazon_stock_data' is empty.")
        except sqlalchemy.exc.OperationalError:
            self.fail("Could not query the database.")

    def test_data_integrity(self):
        
        #Test if the transformed data matches expectations.
       
        print("Validating data integrity in the transformed dataset...")
        try:
            result = self.connection.execute(
                text("SELECT * FROM amazon_stock_data LIMIT 5")
            ).fetchall()

            # Check if 'daily_return' exists and contains non-null values
            self.assertIn('daily_return', self.transformed_data.columns, "Missing 'daily_return' column in the data.")
            self.assertFalse(self.transformed_data['daily_return'].isnull().any(), "'daily_return' column contains null values.")
        except sqlalchemy.exc.OperationalError:
            self.fail("Could not query the database.")

if __name__ == "__main__":
    unittest.main()
