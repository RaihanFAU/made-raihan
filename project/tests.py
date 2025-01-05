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
        cls.pipeline = StockDataPipeline(datasets)
        cls.pipeline.download_and_load_data()
        cls.pipeline.save_to_sqlite()
        cls.engine = sqlalchemy.create_engine(f"sqlite:///{cls.pipeline.db_path}", echo=False)
        cls.connection = cls.engine.connect()

    @classmethod
    def tearDownClass(cls): 
       cls.engine.dispose()
       cls.connection.close()    

    def test_database_file_exists(self):
        print("Checking if the database file exists!")
        self.assertTrue(os.path.exists(self.pipeline.db_path), "Database does not exist.")

    def test_table_exists(self):
        self.inspector = sqlalchemy.inspect(self.engine)

        try:
            tables = self.inspector.get_table_names()
            self.assertIn("AMZN", tables,
                          "Table not found.")
        except sqlalchemy.exc.OperationalError:
            self.fail("Could not connect to the database.")

    def test_table_data(self): 
        print("Checking if the table contains data!")
        
        try:
            result = self.connection.execute(
                text("SELECT COUNT(*) FROM AMZN")
            ).fetchone()
            self.assertGreater(result[0], 0, "Table 'AMZN' is empty.")
        except sqlalchemy.exc.OperationalError:
            self.fail("Could not query the database.")
        
        print("Validating data integrity in the transformed dataset...")
        
        try:
            result = self.connection.execute(
                text("SELECT * FROM AMZN LIMIT 5")
            ).fetchall()
        except sqlalchemy.exc.OperationalError:
            self.fail("Could not query the database.")

if __name__ == "__main__":
    unittest.main()
