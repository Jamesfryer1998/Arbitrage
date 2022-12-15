import os
import sys
import time
import pandas as pd
from datetime import datetime
import psycopg2
import psycopg2.extras as extras
sys.path.insert(0, '/Users/james/Projects/arbitrage')
from useful_functions import load_json
tri_arb_path = '/Users/james/Projects/arbitrage/arbitrage_system/triangular_arbitrage.json'

class PostgresSQL:
    def __init__(self, file_path):
        self.connect_SQL_server()
        self.conn = psycopg2.connect(self.connect_string)
        self.tables = None
        self.time = datetime.now()
        self.file_path = file_path
        self.df = None
        self.convert_to_df()
        self.connect_SQL_server()

    def connect_SQL_server(self):
        postgres_login = load_json('/Users/james/Projects/SQL/dashboard/crypto/postgres_login.json')
        self.connect_string = f"host={postgres_login['host']} dbname=postgres user={postgres_login['user']} password={postgres_login['password']}"

    def convert_to_df(self):
        file = load_json(self.file_path)
        data = [x for x in file]
        list_dict = []

        for i in range(0, len(data)):
            data_keys = list(data[i].keys())
            data_values = list(data[i].values())
            dict = {
                'base': data_keys[0],
                'base_price':data_values[0],
                'inter': data_keys[1],
                'inter_price':data_values[1],
                'end_': data_keys[2],
                'end_price':data_values[2],
                'final_investment':data[i]['final_investment'],
                'profit': data[i]['profit'],
                'date':data[i]['time']            
            }
            list_dict.append(dict)

        self.df = pd.DataFrame(list_dict)

        print(self.df)

    def create_table(self):
        query = f'''
        CREATE TABLE IF NOT EXISTS TRI_ARB (
            id SERIAL PRIMARY KEY,
            base CHAR(100),
            base_price FLOAT(4),
            inter CHAR(100),
            inter_price FLOAT(4),
            end_ CHAR(100),
            end_price FLOAT(4),
            final_investment FLOAT(4),
            profit FLOAT(4),
            date DATE
        );
        '''
        with self.conn:
            with self.conn.cursor() as cur:
                try:
                    cur.execute(query)
                    self.conn.commit()
                    print('TRI_ARB SQL table created.')
                except psycopg2.errors.DuplicateTable as err:
                    pass

    def check_tables(self):
        with self.conn:
            with self.conn.cursor() as cur:
                fetch_sql = '''SELECT table_name
                FROM information_schema.tables
                WHERE table_schema='public'
                '''
                cur.execute(fetch_sql)
                tables = cur.fetchall()
                self.tables = tables
                cur.close()

        print(self.tables)

    def execute_values(self):
        """
        Using psycopg2.extras.execute_values() to insert df to database
        """
        tuples = [tuple(x) for x in self.df.to_numpy()]
        cols = ','.join(list(self.df.columns))

        query  = f'''INSERT INTO TRI_ARB ({cols})
        VALUES %s
        '''
        with self.conn:
            with self.conn.cursor() as cur:
                fetch_sql = f'''
                SELECT COUNT(*)
                FROM TRI_ARB
                '''
                cur.execute(fetch_sql)
                table_len = cur.fetchone()[0]

                if table_len >= len(self.df):
                    print('Table at sufficient count.')
                    pass
                elif table_len <= len(self.df):
                    try:
                        self.remove_table(['TRI_ARB'])
                        
                        time.sleep(1)
                        extras.execute_values(cur, query, tuples, page_size=len(self.df))
                        self.conn.commit()
                        print('All TRI_ARB values uploaded.')
                    except (Exception, psycopg2.DatabaseError) as error:
                        print("Error: %s" % error)
                        self.conn.rollback()
                        cur.close()
                        return None
                    # print(f"    Values populated to {self.ticker}")
                    cur.close()

    def remove_table(self, table_name):
        print(f'Deleting {len(table_name)}...')
        with self.conn:
            with self.conn.cursor() as cur:
                for table in table_name:
                    query = f'''DROP TABLE {table}
                    '''
                    try:
                        cur.execute(query)
                        print(f'Deleted {table}')
        
                    except (Exception, psycopg2.errors.UndefinedTable) as error:
                        print(f'    {table} does not exist.')  

SQL = PostgresSQL(tri_arb_path)
SQL.create_table()
SQL.check_tables()
SQL.execute_values()
# SQL.remove_table(['TRI_ARB'])