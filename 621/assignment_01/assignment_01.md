Task: Unity Catalog Setup
Create unity catalog with the naming convention <roll_number>-pa1.  Create bronze, silver and gold
schemas under it.
Reference:
https://learn.microsoft.com/en-us/azure/databricks/catalogs/create-catalog
2. Task: Setup Bronze Layer (Raw Ingestion)
Goal: Ingest the raw Parquet files into a Delta table without modifications.
Dataset Source:OƯicial NYC TLC Trip Record Data
 Target Data: Yellow Taxi Trip Records
 Timeframe: 6 consecutive months from any year
1. Download the files to a temporary directory first.  You need to perform this download within
your notebook using shell and/or dbutils commands.
2. Load all the downloaded Parquet files into a single Spark DataFrame and add a new column
ingestion_timestamp using the current time.
3. Write this DataFrame to a Delta table taxi_trips under bronze schema.
4. Show the transaction log of your table.
5. Demonstrate "Time Travel" by querying the table using a previous version number or
timestamp to show the state before all files were fully merged.
Tips/Reference:
 https://learn.microsoft.com/en-us/azure/databricks/ingestion/file-upload/download-internet-
files
3. Task: Setup Silver Layer (Cleansing & Refining)
Note: Data Dictionary for the Yellow Taxi Trips can be retrieved from the below link:
https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
Goal: Clean the data and ensure it is ready for analysis.
 Perform data quality checks: Filter out records where trip_distance is zero or negative, and
where total_amount is less than 0.
 Standardize the data types for pickup and drop-oƯ times and calculate a new column 
trip_duration_minutes.
 Simulate a data update. Pick 10K random records and change their payment_type. Use the
MERGE INTO command to update these records in your Silver table while maintaining ACID
consistency.
 Add a new dummy column (e.g., driver_notes) to your Silver table. Configure your write
operation to allow forSchema Evolution so the table schema updates automatically. Write the
mapped value of RatecodeId to this column.
 Create delta table in your silver layer with data filtered based on vendor id.  Name the table as
nyc_yellowtaxi_<vendor_id>.   Show percentage of data belongs to each vendor in your
notebooks.
 What is the ratio of tip amount to the fare paid?
 Out of total taxis, what percentage of taxis stored the data in the vehicle memory before
forwarding the saved batch to the server?
4. Task: The Gold Layer (Business Insights)
Goal: Create high-value, aggregated tables for the business.
 Create a table under gold schema that has the Average Fare Amount andTotal Trip Count per
PULocationID (Pickup Zone) for each of the months. Name the table avg_fare.
 Join your taxi data with theTaxi Zone Lookup Table to replace IDs with actual Borough and Zone
names. Same your table as
 Based on the pickup location and drop of locations, group and aggregate data for each to-from
location (total fare paid, total tips paid, total tips, airport fee, etc).  Then look up the IDs from the
respective data dictionary and replace location ID with the actual location name.   Replace all
IDs with their respective values.  Same the table as trip_aggregates_with_locations.
oYou will need theTaxi Zone Lookup Table to replace IDs with actual location and zone
name.
 Delta Lake Performance Optimization: Run the OPTIMIZE command on your Gold table and
applyZ-ORDER  on a column to speed up time-based queries.
oClarify in the notebook which column you picked and why.
Demonstrate query timings updates before and after performing z-ordering.