import configparser
import psycopg2
from create_cluster import create_session, get_connection_str, check_cluster_status
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    '''Drop all tables from db'''
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    '''Create staging and dimension tables'''
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    
    session = create_session(config['AWS']['KEY'],config['AWS']['SECRET'])
    
    conn_str = get_connection_str(session, config)
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()

    drop_tables(cur, conn)
    print('----    creating tables    ----')
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()