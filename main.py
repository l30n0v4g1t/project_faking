import sqlite3
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

fake = Faker()


def init_database():
    conn = sqlite3.connect("registrations.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            password TEXT,
            website TEXT
        )
    """)
    conn.commit()
    return conn, cursor


def generate_random_data():
    name = fake.name()
    email = fake.email()
    password = fake.password(length=12)
    return name, email, password

def register_to_website(url, name, email, password):
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        time.sleep(2)
        driver.find_element(By.NAME, "username").send_keys(name)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "confirm_password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        time.sleep(3)
        print(f"Registration successful on {url} for {name}")
    except Exception as e:
        print(f"Error on {url}: {e}")
    finally:
        driver.quit()


def main():
    conn, cursor = init_database()
    websites = [
        "https://example1.com/registe",
        "https://example2.com/register"
    ]
    
    for website in websites:
        name, email, password = generate_random_data()
        
        print(f"Attempting registration on {website}")
        register_to_website(website, name, email, password)
        
        cursor.execute("INSERT INTO registrations (name, email, password, website) VALUES (?, ?, ?, ?)",
                       (name, email, password, website))
        conn.commit()
        print(f"Data saved: {name}, {email}, {website}")
    
    conn.close()
main()
