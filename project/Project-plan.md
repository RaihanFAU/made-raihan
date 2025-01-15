# Project Plan

## Title
<!-- Give your project a short title. -->
Analysis and Visualization of Stock Market Trends in Major Tech and Financial Companies Using python.


## Main Question

<!-- Think about one main question you want to answer based on the data. -->

1. Do Amazon stock trends align with global stock market indices during key economic events?



## Description
 This project uses U.S. stock market(Amazon stock) data to analyze trends and explore the pricing alignment with global stock data. By identifying patterns in stock prices, volumes, and technical metrics, this project aims to gain indices relationship between Amazon stock and global stock market over the time.<br />

## Datasources
### Datasource: U.S. Stock Market Data & Technical Indicators(Amazon stock data 2010-2021)
-*Metadata URL:* https://www.kaggle.com/datasets/nikhilkohli/us-stock-market-data-60-extracted-features <br/>
-*Data URL:* https://www.kaggle.com/datasets/nikhilkohli/us-stock-market-data-60-extracted-features?select=AMZN.csv<br />
-*Data Type:* CSV<br />
The dataset includes daily stock data for various companies, featuring price data (open, high, low, close), volume, and 60+ technical indicators.
### Datasource: Global Stock Market (2008-2023)
-*Metadata URL:* https://www.kaggle.com/datasets/pavankrishnanarne/global-stock-market-2008-present <br/>
-*Data URL:* https://www.kaggle.com/datasets/pavankrishnanarne/global-stock-market-2008-present?select=2008_Globla_Markets_Data.csv<br />
-*Data Type:* CSV<br />
The dataset includes daily stock data for various companies, featuring price data (open, high, low, close), volume, and 10+ technical indicators
# Work Packages
### Data Collection
- Import data for each stock into a pandas DataFrame.
### Data Cleaning
- Identify and handle any missing values, remove duplicates, and standardize formats. Verify the accuracy of values and check that all dates, prices, and indicators are within reasonable ranges.
### Work Package 3: Exploratory Analysis
- Analyze stock price trends over time, including daily, weekly, and monthly trends. Study the relationship between trading volume, volatility, and stock performance. Examine the effectiveness of various technical indicators (e.g., moving averages, RSI).
### Work Package 4: Data Pipeline
- Design an ETL pipeline for data extraction and transformation, including data cleaning steps. Storage Setup: Implement a storage solution for the cleaned data, such as a relational database. Automate Ingestion: Set up automated data ingestion to update the analysis as new stock data becomes available.
### Work Package 5: Reporting and Documentation
- Summarize trends and insights in a final report.Create visualizations (e.g., line charts, candlestick charts) to highlight key insights. Prepare a presentation summarizing findings and insights.









