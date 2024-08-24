CREATE_EMPLOYEE_TABLE = """
CREATE TABLE IF NOT EXISTS EMPLOYEES (
    "SERIAL_NUMBER" NUMERIC PRIMARY KEY,
    "COMPANY_NAME" VARCHAR(100),
    "EMPLOYEE MARKME" TEXT,
    "LEAVE" INTEGER
);"""

CREATE_EMPLOYEE_TEMP_TABLE = """
DROP TABLE IF EXISTS EMPLOYEES_TEMP;
CREATE TABLE EMPLOYEES_TEMP (
    "Serial Number" NUMERIC PRIMARY KEY,
    "Company Name" TEXT,
    "Employee Markme" TEXT,
    "Description" TEXT,
    "Leave" INTEGER
);""",

MERGE_DATA_QUERY = """
    INSERT INTO EMPLOYEES
    SELECT * FROM (
        SELECT DISTINCT * FROM EMPLOYEES_TEMP
    ) t
    ON CONFLICT ("Serial Number") DO UPDATE
    SET
        "Employee Markme" = excluded."Employee Markme",
        "Description" = excluded."Description",
        "Leave" = excluded."Leave";        
"""