# This script
# Extracts data from /etc/passwd file into a CSV file.

# The csv data file contains the user name, user id and
# home directory of each user account defined in /etc/passwd

# Transforms the text delimiter from ":" to ",".
# Loads the data from the CSV file into a table in PostgreSQL database.

echo "Extracting data..."
cut -d":" -f1,3,6 /etc/passwd > extracted-data.txt

echo "Transforming data..."
tr ":" "," < extracted-data.txt > transformed-data.csv

echo "Loading Data"
export PGPASSWORD=j4kURRHH5WD9AbH1xWa4yL2L;

echo "\c template1;\COPY users FROM '/home/project/transformed-data.csv' DELIMITERS ',' CSV;" | psql --username=postgres --host=postgres

echo "SELECT * FROM users;" | psql --username=postgres --host=postgres template1
