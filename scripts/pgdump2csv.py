"""
This script loads from a pg dump file and exports each table to a separate CSV file.
"""
from argparse import ArgumentParser
import psycopg2
import os
import csv

def parse_args():
    parser = ArgumentParser(description="Export PostgreSQL db to multiple CSV file.")
    parser.add_argument("--db", help="Name of the db to export")
    parser.add_argument("--output_dir", help="Output dir for CSVs files path")
    parser.add_argument("--host", default="localhost", help="Database host")
    parser.add_argument("--port", default=5432, type=int, help="Database port")
    parser.add_argument("--user", required=True, help="Database user")
    parser.add_argument("--password", required=True, help="Database password")
    return parser.parse_args()

def retrieve_table_names(cursor: psycopg2.extensions.cursor, db_name: str):
    """
    Retrieve all table names from the specified PostgreSQL database.

    :param cursor: psycopg2 cursor object
    :param db_name: Name of the database
    :return: List of table names
    """
    cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    return [row[0] for row in cursor.fetchall()]

def retrieve_db_table(cursor: psycopg2.extensions.cursor, db_name: str, table_name: str):
    """
    Retrieve all data from a specified table in the PostgreSQL database.

    :param cursor: psycopg2 cursor object
    :param db_name: Name of the database
    :param table_name: Name of the table to retrieve data from
    :return: List of tuples containing the rows of data
    """
    cursor.execute(f"SELECT * FROM {table_name}")
    return cursor.fetchall()


def main():
    args = parse_args()

    # Connect to the PostgreSQL database
    try:
        connection = psycopg2.connect(
            dbname=args.db,
            user=args.user,
            password=args.password,
            host=args.host,
            port=args.port
        )
        cursor = connection.cursor()

        # Retrieve all table names
        table_names = retrieve_table_names(cursor, args.db)
        if not table_names:
            print("No tables found in the database.")
            return

        # Create output directory if it doesn't exist
        os.makedirs(args.output_dir, exist_ok=True)

        # Export each table to a CSV file
        for table_name in table_names:
            print(f"Exporting table: {table_name}")
            rows = retrieve_db_table(cursor, args.db, table_name)

            # Get column names
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
            columns = [col[0] for col in cursor.fetchall()]

            # Define CSV file path
            csv_file_path = os.path.join(args.output_dir, f"{table_name}.csv")

            # Write rows to CSV
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(columns)  # Write the header (column names)
                writer.writerows(rows)  # Write all data rows

            print(f"Table {table_name} exported to {csv_file_path}")

        print("Data export complete.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    main()