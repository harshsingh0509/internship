import os
import requests
from bs4 import BeautifulSoup
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# PostgreSQL config from environment
db_config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

SCHEMA_NAME = "expired_domains_schema"
TABLE_NAME = "expired_domains"

# Function to connect to PostgreSQL
def connect_db():
    return psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        dbname=db_config["dbname"],
        user=db_config["user"],
        password=db_config["password"]
    )

# Function to create schema and table if they don't exist
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    # Create schema if it doesn't exist
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME};")

    # Create table inside the schema
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.{TABLE_NAME} (
            id SERIAL PRIMARY KEY,
            domain_name TEXT,
            tld TEXT,
            domain_type TEXT,
            status TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()

# Function to save data
def save_to_db(data):
    conn = connect_db()
    cursor = conn.cursor()

    for domain in data:
        cursor.execute(f"""
            INSERT INTO {SCHEMA_NAME}.{TABLE_NAME} (domain_name, tld, domain_type, status)
            VALUES (%s, %s, %s, %s);
        """, (domain['domain_name'], domain['tld'], domain['domain_type'], domain['status']))

    conn.commit()
    cursor.close()
    conn.close()

# Scrape data function
def scrape_expired_domains():
    url = 'https://www.expireddomains.net/backorder-expired-domains/'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    print("🌐 Opening website...")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.select('table.base1 tr')
    domain_data = []

    for idx, row in enumerate(rows[1:11], start=1):  # Limit to 10 rows
        cols = [col.text.strip() for col in row.find_all('td')]
        if len(cols) < 5:
            continue

        domain_name_raw = cols[0]
        domain_type = cols[3]
        status = cols[-1]

        try:
            parsed_url = urlparse('http://' + domain_name_raw)
            domain_name = parsed_url.hostname
            tld = domain_name.split('.')[-1] if domain_name else 'unknown'
        except Exception:
            domain_name = domain_name_raw
            tld = 'unknown'

        print(f"Row {idx}: domain_name='{domain_name}', tld='{tld}', domain_type='{domain_type}'")
        domain_data.append({
            'domain_name': domain_name,
            'tld': tld,
            'domain_type': domain_type,
            'status': status
        })

    return domain_data

# Main function
def main():
    create_table()
    domain_data = scrape_expired_domains()
    if domain_data:
        save_to_db(domain_data)
        print("✅ Data successfully saved to PostgreSQL.")
    else:
        print("⚠️ No data to save.")

if __name__ == "__main__":
    main()

