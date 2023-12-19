# Designed and implemented an ETL Pipeline for Financial Data Analytics on GCP.

This project is dedicated to building an efficient Extract, Transform, Load (ETL) pipeline for the Financial Data Set on the Google Cloud Platform (GCP). A key focus is leveraging Infrastructure as Code (IaC) principles, specifically utilizing **GCP Deployment Manager**, to streamline and automate the setup and management of infrastructure.

Automating infrastructure deployment is essential for aligning with best practices in the technology industry.This approach ensures consistency and reproducibility by expressing infrastructure as code, promoting uniform and repeatable deployment processes. It eliminates discrepancies from manual configuration, guaranteeing identical environments and facilitating easy testing, staging, and development environment reproduction.

## Project Overview:
The aim of this project is to build an ETL pipeline on Google Cloud Platform (GCP) for the Financial Data Set. This pipeline facilitates the extraction, transformation, and loading of data from a SQL server to BigQuery, catering to the specific needs of analytics.This pipeline facilitates the extraction, transformation, and loading of data from a SQL server to BigQuery for analytics purposes.

## Dataset Description:
This project uses equity financial data from [BseIndia](https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.html?flag=0), which includes stock price history from various industry segments. A few of the fields included in the dataset are as follows :
- Open_price
- High_price
- Low_price
- Close_price
- No_of_shares
- No_of_Trades
- Total_turnover

## Project Implementation Approach:
- Utilize GCP Deployment Manager to create necessary resources: GCS buckets, BigQuery tables, and a virtual machine.
- Install Apache NiFi on the virtual machine to streamline the extraction process from the SQL server. Apache NiFi will facilitate the smooth transfer of data, efficiently dumping it into a designated GCS bucket.
- Implement a Cloud Function designed to actively monitor the designated GCS bucket for any changes. Upon detecting modifications, this function triggers a PySpark job using Cloud Dataproc, ensuring a dynamic and responsive data processing flow.
- Leverage workflow templates to automate Dataproc cluster creation and PySpark job execution, ensuring a structured and efficient data processing environment.
- Utilize BigQuery to load transformed data for analytics, optionally storing a backup in a designated cloud storage bucket for added data security.

## Architecture :
![Architecture](https://github.com/elterraf/Designed-and-implemented-an-ETL-Pipeline-for-Financial-Data-Analytics-on-GCP./assets/73224299/9883219a-72ae-46cb-b673-39974db2bfaa)



