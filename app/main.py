import mysql.connector
import requests
from app.config import DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD, SHOPIFY_ACCESS_TOKEN
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI

db_connection = None


def get_db_connection():
    global db_connection
    if db_connection is None or db_connection.close:
        try:
            db_connection = mysql.connector.connect(
                host=DB_SERVER, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
            )
        except Exception as e:
            print(f"Failed to connect to database: {e}")
    return db_connection


def get_products_data():
    # Shopify credentials and store details
    SHOPIFY_STORE = "https://mall.aroomy.com"

    # GraphQL query to get the product listings from the "Featured" collection
    query = """
    {
      collectionByHandle(handle: "featured") {
        title
        products(first: 10) {
          edges {
            node {
              title
              description
              onlineStoreUrl
              priceRange {
                minVariantPrice {
                  amount
                }
              }
              images(first: 5) {
                edges {
                  node {
                    originalSrc
                  }
                }
              }
            }
          }
        }
      }
    }
    """

    # API request to Shopify
    url = f"{SHOPIFY_STORE}/api/2024-01/graphql.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Storefront-Access-Token": SHOPIFY_ACCESS_TOKEN,
    }
    response = requests.post(url, json={"query": query}, headers=headers)

    if response.status_code == 200:
        return response.json()["data"]["collectionByHandle"]["products"]["edges"]

    raise Exception(f"Failed to retrieve products. Status code: {response.status_code}")


def scrape_products_task():
    print(f"Scraping products at {datetime.now()}")
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        products_data = get_products_data()

        # Clear out existing products from the new table
        cursor.execute("DELETE FROM mall_featured_products")

        # Insert new products into the database
        for product in products_data:
            product_node = product["node"]
            title = product_node["title"]
            description = product_node["description"]
            price = float(product_node["priceRange"]["minVariantPrice"]["amount"])
            url = product_node["onlineStoreUrl"]
            image_url = product_node["images"]["edges"][0]["node"]["originalSrc"]

            insert_query = """
            INSERT INTO mall_featured_products (title, description, price, url, image_url)
            VALUES (%s, %s, %s, %s, %s)
            """

            data = (title, description, price, url, image_url)

            cursor.execute(insert_query, data)

        conn.commit()
        print("Products updated successfully in the database.")
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        cursor.close()
        conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    trigger = CronTrigger(hour=0, minute=0, second=0)
    scheduler.add_job(scrape_products_task, trigger=trigger)
    scheduler.start()
    print("Scheduler started")
    yield
    scheduler.shutdown()
    if db_connection is not None:
        db_connection.close()
        print("Database connection closed")


app = FastAPI(lifespan=lifespan)
scheduler = BackgroundScheduler()


@app.get("/health")
def health():
    return {"status": "UP"}


@app.post("/scrape-products")
def scrape_products():
    scrape_products_task()
    return {"message": "Successfully scraped products"}
