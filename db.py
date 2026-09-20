import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host="",
    
        ",
        ",
        ",
        cursor_factory=RealDictCursor  # returns rows as dicts
    )
# 