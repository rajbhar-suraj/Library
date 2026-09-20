import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host="aws-0-ap-south-1.pooler.supabase.com",
        # port=5432
        database="postgres",
        user="postgres.gitimlmcsskqsonrcjzg",
        password="Shinichi00816",
        cursor_factory=RealDictCursor  # returns rows as dicts
    )


# host=aws-0-ap-south-1.pooler.supabase.com
# port=5432
# database=postgres
# user=postgres.gitimlmcsskqsonrcjzg
#     DATABASE_URL=postgresql://postgres.gitimlmcsskqsonrcjzg:Shinichi00816@aws-0-ap-south-1.pooler.supabase.com:5432/postgres