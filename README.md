# CSV_TO_MYSQL

This script help you to insert data from a .csv file into your MySQL DB. 

# Features:

- Input-prompt & files based == just run and go 
- Low memory usage
- Easy to maintain
- Status visualization: easy to know where your steps go
- Simple and effortless analytics exported in a .txt file

# Required libraries:

- Pandas
- Mysql-connector
- Progressbar (search for progressbar2)
- Time 

# What you need:

- config parameters file (host, user, password, db)   -->   A normal .txt file      -->   separator: ','
- DDL file                                            -->   .txt || .csv            -->   separator: ';'
- DML file                                            -->   .txt || .csv            -->   separator: ';'
- .CSV file                                           -->   It MUST be a .CSV       -->   Header == True, separator: ','


# Example:

- CSV file:             
- Config params:        localhost, root, your_password, db
- DDL file:             your SQLs.
  Content:
  
  USE EMPLOYEE;
  DROP TABLE IF EXISTS EMP_DATA;
  CREATE TABLE emp_data(Type varchar(255),Area varchar(255),year varchar(255),geo_count varchar(255),ec_count varchar(255));
  
- DML file:             your SQLs

  INSERT INTO employee.emp_data VALUES (%s,%s,%s,%s,%s);
  
  
# TESTING

1.000.000 rows, 1 table     -->   05.98 minutes
