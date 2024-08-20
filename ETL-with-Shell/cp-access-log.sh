echo "Downloading the log file"
wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Bash%20Scripting/ETL%20using%20shell%20scripting/web-server-access-log.txt.gz"

echo "Unzipping the file"
gunzip -f web-server-access-log.txt.gz

echo "Extracting the Data"
cut -d"#" -f1-4 < web-server-access-log.txt | tr "#" "," > extracted-data.csv

echo "Writing CSV to database"
echo "\c template1; \COPY access_log FROM extracted-data.csv DELIMITERS ',' CSV HEADER;" | psql --username=postgres --host=postgres

echo "SELECT * FROM access_log LIMIT 5;" | psql --username=postgres --host=postgres template1
