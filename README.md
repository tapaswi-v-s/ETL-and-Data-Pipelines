# 🚀 Welcome to My Data Engineering Playground!

Hey there! 👋 Welcome to my little corner of the internet where data pipelines come to life. Whether you're here to learn, get inspired, or just curious about what I’ve been up to, I’m thrilled to have you. This repo is all about showcasing my skills in the fascinating world of Data Engineering, specifically around ETL (Extract, Transform, Load) processes. Ready? Let’s dive in! 🌊

## 🎡 The Grand Tour

This repo is divided into three exciting sections, each offering a different flavor of data engineering magic. Here’s what you’ll find:

### 1. 🏗️ Apache Airflow Data Pipelines

Imagine a world where data flows effortlessly, tasks are automated, and everything just clicks. That’s what Apache Airflow is all about! In this section, you’ll find data pipelines (also known as DAGs—Directed Acyclic Graphs, but let’s not get too technical) that I’ve built to show off some cool automation tricks.

#### 🎢 The DAGs:

- **employee_DAG.py**:
    - **What’s Inside**: Picture this—a pipeline that grabs employee data from an online CSV file and neatly tucks it into a local PostgreSQL database. It’s like a data concierge service!
    - **Tasks Include**:
        - `create_output_directory()`: Ensures your files have a cozy home.
        - `create_employee_table`: Prepares a table in the database, ready to welcome data.
        - `create_employees_temp_table`: Sets up a temporary table for some behind-the-scenes magic.
        - `get_data()`: Fetches the employee data, saving it locally and in the database.
        - `merge_data()`: Filters out the noise and keeps only the unique records.
    - **How It Flows**: `[create_output_directory(), create_employee_table, create_employees_temp_table] >> get_data() >> merge_data()`

- **ETL_toll_data.py**:
    - **What’s Inside**: Ever wondered how data from different toll plazas, each with its own IT setup, gets consolidated? This DAG does exactly that! It’s built to analyze toll data collected from highways operated by different companies, each using its own file format. The DAG pulls all this data together into a single, unified file.
    - **Tasks Include**:
        - `download_data`: Grabs a tarball file containing all the toll data.
        - `unzip_data`: Extracts the contents from the tarball.
        - `extract_data_from_csv`: Pulls out the Rowid, Timestamp, Anonymized Vehicle Number, and Vehicle Type fields from the `vehicle-data.csv` file and saves them to `csv_data.csv`.
        - `extract_data_from_tsv`: Extracts the Number of Axles, Tollplaza ID, and Tollplaza Code fields from the `tollplaza-data.tsv` file (a tab-separated file) and saves them to `tsv_data.csv`.
        - `extract_data_from_fixed_width`: Retrieves the Type of Payment Code and Vehicle Code fields from the fixed-width file `payment-data.txt` and saves them to `fixed_width_data.csv`.
        - `consolidate_data`: Combines all the extracted data into a single file named `extracted_data.csv`.
        - `transform_data`: Transforms the `vehicle_type` field in `extracted_data.csv` to uppercase and saves it as `transformed_data.csv`.
    - **How It Flows**: `download_data >> unzip_data >> extract_data_from_csv_task >> extract_data_from_tsv_task >> extract_data_from_fixed_width_task >> consolidate_data_task >> transform_data_task`

- **AWS_FAQs_Extraction.py**:
    - **Status**: 🚧 Under Construction! I’ll be working on this soon to extract FAQs from AWS docs.

- **toy_dag.py**:
    - **What’s Inside**: This one’s just for fun—a simple pipeline that takes data from a file, transforms it into a CSV, loads it up, and then prints it out. Think of it as a warm-up exercise!
    - **How It Flows**: `extract >> transform >> load >> check`

#### 🚀 How to Get These Pipelines Running:

1. **Prep the Stage**: Make sure these directories are ready: `./dags`, `./logs`, `./config`, `./plugins`.
2. **Fire Up Airflow**:
    - Initialize the environment: `docker compose up airflow-init`
    - Get it running: `docker compose up`
3. **Spin Up the Database**:
    - Run the PostgreSQL container: `docker compose -f database-compose.yml up`

> 📝 **Pro Tip**: Don’t forget to connect Airflow to your PostgreSQL database!

### 2. 📡 Streaming Pipelines with Kafka

**Status**: Stay tuned—more streaming adventures are coming your way! This section will be where real-time data meets the magic of Kafka.

### 3. 🐚 ETL with Shell Scripts

Sometimes, simplicity is key. In this section, I’ve got some basic, yet powerful, ETL pipelines built with good old shell scripts.

#### 🎬 The Scripts:

- **cp-access-log.sh**:
    - **The Story**: This script plays detective—grabbing a compressed log file, unzipping it, turning it into a CSV, and then storing it in a PostgreSQL database. It even gives you a sneak peek at the first 5 records!

- **csv2db.sh**:
    - **The Story**: Think of this script as a data translator. It takes the `/etc/passwd` file, extracts the data into a CSV, transforms it by swapping `:` for `,`, and then loads it into PostgreSQL. Voilà—your data is ready to go!

---

### 🎉 That’s a Wrap!

I hope you enjoy exploring this repo as much as I enjoyed creating it! If you’ve got any feedback, ideas, or just want to chat about data engineering, don’t hesitate to reach out. Contributions are welcome, and curiosity is encouraged.

Happy coding! 🚀
