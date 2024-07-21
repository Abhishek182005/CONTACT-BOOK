# create_database.py
import MySQLdb
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contact_book.settings')
django.setup()

from django.conf import settings

def create_database():
    try:
        # Connect to MySQL server without specifying the database
        conn = MySQLdb.connect(
            host=settings.DATABASES['default']['HOST'],
            user=settings.DATABASES['default']['USER'],
            passwd=settings.DATABASES['default']['PASSWORD']
        )
        cursor = conn.cursor()
        
        # Create the database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.DATABASES['default']['NAME']}")
        print(f"Database {settings.DATABASES['default']['NAME']} ensured to exist.")
        
        # Close the connection
        cursor.close()
        conn.close()
    except MySQLdb.Error as e:
        print(f"Error {e}")

if __name__ == "__main__":
    create_database()
