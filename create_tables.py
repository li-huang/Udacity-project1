import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """
    The function to drop and recreate postgresql database and connect to the created database.         
        Parameters: 
            None.
            
        Returns: 
            cur: The cursor of the created database
            conn: The connection of the created database
    """
    # connect to default database
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()    
    
    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()
    
    return cur, conn


def drop_tables(cur, conn):
    """
    The function to drop tables in a given database. 
  
        Parameters: 
            cur: The cursor of the given database
            conn: The connection of the given database
          
        Returns: 
            None.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    The function to create tables in a given database. 
  
        Parameters: 
            cur: The cursor of the given database
            conn: The connection of the given database
          
        Returns: 
            None.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """The main function to drop and recreate a postgresql database and to drop and recreate tables in the database."""
    cur, conn = create_database()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()