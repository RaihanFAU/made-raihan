import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from sqlalchemy import create_engine
import tempfile
import zipfile


class StockDataPipeline:
    def __init__(self, datasets):
        self.datasets = datasets
        self.dataframes = {}
        self.api = KaggleApi()
        self.api.authenticate()

        self.data_dir = os.path.join(os.getcwd(), "data")  
        os.makedirs(self.data_dir, exist_ok=True)  

    def download_and_load_data(self):
        self.dataframes ['global_stock'] = None
        for i in range(len(self.datasets)):
            with tempfile.TemporaryDirectory() as temp_dir:
                self.api.dataset_download_files(self.datasets[i], path=temp_dir, unzip=False)
                print("Download done.")
            
                zip__path = os.path.join(temp_dir, f"{self.datasets[i].split('/')[-1]}.zip")
                with zipfile.ZipFile(zip__path, 'r') as zip_ref:
                    for file_name in zip_ref.namelist():
                        if file_name.endswith('.csv'):  
                            # for first dataset
                             # only selected file name will be saved
                            with zip_ref.open(file_name) as csv_file:
                                # Load each CSV file into a separate DataFrame
                                if i==0 and file_name.split('/')[-1].replace('.csv', '') in ['AMZN', 'GOOGL'] :

                                    df = pd.read_csv(csv_file, encoding="ISO-8859-1") 
                                    self.dataframes[file_name.split('/')[-1].replace('.csv', '')] = df
                                elif i == 1: 
                                    df = pd.read_csv(csv_file, encoding="ISO-8859-1")
                                    if not isinstance(self.dataframes['global_stock'], pd.DataFrame):
                                        self.dataframes['global_stock'] = pd.DataFrame(columns=df.columns)
   
                                    self.dataframes['global_stock'] = pd.concat([self.dataframes['global_stock'], df], ignore_index=True)        
        

    def preprocess_data(self):
        for name, df in self.dataframes.items():
            print(f"Preprocessing dataset: {name}")
            df.dropna(thresh=2, inplace=True)

            for column in df.columns:
                if pd.api.types.is_numeric_dtype(df[column]):
                    df[column].fillna(df[column].mean(), inplace=True) 
                else:
                    df[column].fillna("Unknown", inplace=True) 

    def save_to_sqlite(self, db_name="stock_data"):
        self.db_path = os.path.join(self.data_dir, f"{db_name}.sqlite")
        engine = create_engine(f"sqlite:///{self.db_path}", echo=False)

        for name, df in self.dataframes.items():
            df.to_sql(name, engine, if_exists='replace', index=False)
            print(f"Data saved to table: {name}")

        engine.dispose()
        print(f"SQLite database saved at: {self.db_path}")

if __name__ == '__main__':
    datasets = ['nikhilkohli/us-stock-market-data-60-extracted-features',
                'pavankrishnanarne/global-stock-market-2008-present']    

    pipeline = StockDataPipeline(datasets)
    pipeline.download_and_load_data()
    pipeline.preprocess_data()
    pipeline.save_to_sqlite()
