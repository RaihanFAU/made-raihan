import pandas as pd
import sqlite3
import kaggle
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ETLPipeline:
    def __init__(self):
        # Kaggle dataset details
        self.dataset_kaggle = "nikhilkohli/us-stock-market-data-60-extracted-features"
        self.csv_file_name = "AMZN.csv"  
        # Columns to process
        self.columns_to_numeric = ['open', 'high', 'low', 'close', 'volume', 'adjusted_close']

    def extract(self):
        """
        Download and extract the stock market data from Kaggle.
        """
        try:
            # Download the Kaggle dataset
            logging.info(f"Downloading dataset from Kaggle: {self.dataset_kaggle}")
            kaggle.api.dataset_download_files(self.dataset_kaggle, path='.', unzip=True)
            
            # Check if the specific CSV file exists after extraction
            if os.path.exists(self.csv_file_name):
                stock_df = pd.read_csv(self.csv_file_name)
                logging.info("Successfully extracted the stock market data.")
                
                # Clean up by removing the CSV file after loading
                os.remove(self.csv_file_name)
            else:
                raise FileNotFoundError(f"File {self.csv_file_name} not found in the Kaggle dataset.")
            
            return stock_df
        
        except Exception as e:
            logging.error(f"An error occurred during extraction: {e}")
            raise

    def transform(self, stock_df):
        """
        Clean and preprocess the stock market data.
        """
        try:
            # Convert numeric columns to the correct data type
            stock_df[self.columns_to_numeric] = stock_df[self.columns_to_numeric].apply(pd.to_numeric, errors='coerce')
            
            # Handle missing values by interpolation
            stock_df.interpolate(method='linear', inplace=True)
            
            # Add new calculated features
            stock_df['daily_return'] = stock_df['close'].pct_change()  # Daily percentage return
            
            # Ensure no duplicate entries (based on the 'date' column)
            if 'date' in stock_df.columns:
                stock_df = stock_df.drop_duplicates(subset=['date'])
            
            logging.info("Transformation completed successfully.")
            return stock_df
        
        except Exception as e:
            logging.error(f"An error occurred during transformation: {e}")
            raise

    def load(self, dataframe, db_name, table_name):
        """
        Load the processed data into an SQLite database.
        """
        try:
            # Connect to SQLite database
            conn = sqlite3.connect(db_name)
            # Write the dataframe to a table
            dataframe.to_sql(table_name, conn, if_exists='replace', index=False)
            logging.info(f"Data successfully loaded into database '{db_name}' in table '{table_name}'.")
        except Exception as e:
            logging.error(f"An error occurred during loading: {e}")
            raise
        finally:
            conn.close()

    def run(self, db_name, table_name):
        """
        Run the entire ETL pipeline.
        """
        try:
            # Extract
            stock_df = self.extract()
            logging.info("Extraction step completed.")

            # Transform
            transformed_data = self.transform(stock_df)
            logging.info("Transformation step completed.")

            # Load
            self.load(transformed_data, db_name, table_name)
            logging.info("ETL pipeline completed successfully.")
        
        except Exception as e:
            logging.error(f"An error occurred during the ETL process: {e}")
        
        return transformed_data


# Running the ETL pipeline
etl = ETLPipeline()
transformed_data = etl.run('./us_stock_data.db', 'amazon_stock_data')
