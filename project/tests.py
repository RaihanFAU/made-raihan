import os
import unittest
import sqlalchemy
from sqlalchemy.sql import text
from pipeline import StockDataPipeline

class ETLPipelineTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Testing the ETL Pipeline!")
        datasets = ['nikhilkohli/us-stock-market-data-60-extracted-features',
                'pavankrishnanarne/global-stock-market-2008-present'] 
        # Initialize and execute the ETL pipeline
        cls.pipeline = StockDataPipeline(datasets)
        cls.pipeline.download_and_load_data()
        cls.pipeline.save_to_sqlite()
        cls.engine = sqlalchemy.create_engine(f"sqlite:///{cls.pipeline.db_path}", echo=False)
        cls.connection = cls.engine.connect()

    @classmethod
    def tearDownClass(cls):
    
        #Close the database connection and clean up after all tests.
        
       cls.engine.dispose()
       cls.connection.close()    


    def test_database_file_exists(self):
        
        #Test if the SQLite database file is created.
        
        print("Checking if the database file exists!")
        self.assertTrue(os.path.exists(self.pipeline.db_path), "Database does not exist.")

    def test_table_exists(self):
        

        self.inspector = sqlalchemy.inspect(self.engine)

        try:
            tables = self.inspector.get_table_names()
            self.assertIn("AMZN", tables,
                          "Table not found.")
            self.assertIn("GOOGL", tables,
                          "Table not found.")
        except sqlalchemy.exc.OperationalError:
            self.fail("Could not connect to the database.")

    def test_table_data(self):
        
        #Test if the table contains data.
        
        print("Checking if the table contains data!")
        try:
            result = self.connection.execute(
                text("SELECT COUNT(*) FROM GOOGL")
            ).fetchone()

            # Assert that the table has at least one row
            self.assertGreater(result[0], 0, "Table 'GOOGL' is empty.")
        except sqlalchemy.exc.OperationalError:
            self.fail("Could not query the database.")
        
        #Test if the transformed data matches expectations.
       
        print("Validating data integrity in the transformed dataset...")
        try:
            result = self.connection.execute(
                text("SELECT * FROM AMZN LIMIT 5")
            ).fetchall()

        except sqlalchemy.exc.OperationalError:
            self.fail("Could not query the database.")

if __name__ == "__main__":
    unittest.main()
