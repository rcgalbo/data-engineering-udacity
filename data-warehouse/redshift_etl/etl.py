import configparser
import psycopg2
from create_cluster import create_session, get_connection_str, check_cluster_status
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """Run queries to load data into staging tables"""
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """Run queries to insert data from staging tables"""
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    session = create_session(config['AWS']['KEY'],config['AWS']['SECRET'])
    
    conn_str = get_connection_str(session, config)
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()