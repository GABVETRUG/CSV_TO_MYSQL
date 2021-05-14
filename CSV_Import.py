import csv
import pandas as pd
import mysql.connector as msql
from mysql.connector import Error
import time
import progressbar


def list_to_string(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1


def user_input():
    print("Welcome to the CSV_Import script!\n\nPlease write below your .CSV's file path:\n" +
          "P.S. You can use absolute or relative path too\n")
    data = str(input())
    df = pd.read_csv(data, index_col=False, delimiter=',')
    print("\nVery good! Now tell me where I can find your DDL script. It can be .txt or .csv\n ")
    ddl_script = str(input())
    print("\nPerfect! Just to know, where I can read your DML script?\nTip: both .txt & .csv\n")
    dml_script = str(input())
    print("\nLast but not at least: your connection parameters file? :)\n ")
    conn = str(input())
    return df, ddl_script, dml_script, conn


def execute():
    # Variables declaration
    localtime = time.asctime(time.localtime(time.time()))
    total_rows = 0
    query_list = []
    start = time.time()
    data, ddl_script, dml_script, conn = user_input()
    try:
        # MySQL connection
        my_file = open(conn, "r")
        content_list = my_file.read().split(",")
        my_file.close()
        conn = msql.connect(host=content_list[0], user=content_list[1], password=content_list[2], database=content_list[3], auth_plugin='mysql_native_password')
        if conn.is_connected():
            print("\nConnected to the MySQL db")
            time.sleep(2)
            print("\nReading your query from the txt file:")
            time.sleep(1)

            # Reading queries - Cursor must execute 1 query per time. Multiple queries do not work well
            print('\nExecuting query statement(s)...')
            cursor = conn.cursor()
            with open(ddl_script, 'r') as read_obj:
                csv_reader = csv.reader(read_obj, delimiter='\n')
                for row in csv_reader:
                    query_list.append(row)
                    string = list_to_string(row)
                    cursor.execute(string)
                    print(string)

            # Reading rows
            print("\nReading data rows...")
            unknown_bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
            time.sleep(0.5)
            for _ in data.iterrows():
                total_rows += 1
                unknown_bar.update(total_rows)
            print("\nReading completed!\n\nTotal rows read: ", total_rows)
            time.sleep(2)

            # Importing rows
            print("\nImporting .csv file rows:\n")
            max_value_bar = progressbar.ProgressBar(max_value=total_rows)
            with open(dml_script, 'r') as dml_sql:
                for y in dml_sql:
                    temp_str = list_to_string(y)
                sql = temp_str
            for i, row in data.iterrows():
                cursor.execute(sql, tuple(row))
                max_value_bar.update(i)

            # DML Commit
            conn.commit()
            end = time.time()
            total_time = "%.2f" % float((end - start) / 60)
            print("\n\nTotal import time: " + total_time + " minutes")
            return localtime, total_rows, total_time
    except Error as e:
        print("Error while connecting to MySQL", e)
    print("\nExecuted!\n")


def write_stats(loc, tot_r, tot_t):
    stats_file = open('stats.txt', 'a')
    stats = str("Date: " + loc + "\nRows: " + str(tot_r) + "\nTime: " + tot_t + " minutes\n\n"
                + "#######################################" + "\n\n")
    stats_file.write(str(stats))
    stats_file.close()


if __name__ == '__main__':
    loc_time, tot_rows, tot_time = execute()
    write_stats(loc_time, tot_rows, tot_time)
