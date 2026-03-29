import httpx
import time
from datetime import date

BASE_URL_AUTH = "http://localhost:8081"
BASE_URL_TXN = "http://localhost:8082"

EMAIL = "prabhu@test.com"
PASSWORD = "secret123"


def login() -> str:
    response = httpx.post(
        f"{BASE_URL_AUTH}/api/auth/login",
        json={"email": EMAIL, "password": PASSWORD}
    )
    response.raise_for_status()
    return response.json()["token"]


TRANSACTIONS = [
    # October 2025
    {"amount": 85000, "type": "INCOME", "category": "Salary", "description": "Monthly salary credit", "transactionDate": "2025-10-01"},
    {"amount": 22000, "type": "EXPENSE", "category": "Rent", "description": "House rent October", "transactionDate": "2025-10-01"},
    {"amount": 4500, "type": "EXPENSE", "category": "Groceries", "description": "Big Basket monthly order", "transactionDate": "2025-10-03"},
    {"amount": 1200, "type": "EXPENSE", "category": "Food", "description": "Swiggy dinner", "transactionDate": "2025-10-05"},
    {"amount": 800, "type": "EXPENSE", "category": "Transport", "description": "Uber rides", "transactionDate": "2025-10-06"},
    {"amount": 599, "type": "EXPENSE", "category": "Entertainment", "description": "Netflix subscription", "transactionDate": "2025-10-07"},
    {"amount": 2100, "type": "EXPENSE", "category": "Food", "description": "Zomato orders", "transactionDate": "2025-10-10"},
    {"amount": 3500, "type": "EXPENSE", "category": "Shopping", "description": "Myntra clothing", "transactionDate": "2025-10-12"},
    {"amount": 1100, "type": "EXPENSE", "category": "Utilities", "description": "Electricity bill", "transactionDate": "2025-10-15"},
    {"amount": 500, "type": "EXPENSE", "category": "Utilities", "description": "Internet bill", "transactionDate": "2025-10-15"},
    {"amount": 650, "type": "EXPENSE", "category": "Transport", "description": "Ola rides", "transactionDate": "2025-10-18"},
    {"amount": 1800, "type": "EXPENSE", "category": "Food", "description": "Restaurant dinner with friends", "transactionDate": "2025-10-20"},
    {"amount": 999, "type": "EXPENSE", "category": "Entertainment", "description": "Amazon Prime renewal", "transactionDate": "2025-10-22"},
    {"amount": 2200, "type": "EXPENSE", "category": "Groceries", "description": "DMart weekly shopping", "transactionDate": "2025-10-25"},
    {"amount": 5000, "type": "EXPENSE", "category": "Health", "description": "Gym annual membership", "transactionDate": "2025-10-28"},

    # November 2025
    {"amount": 85000, "type": "INCOME", "category": "Salary", "description": "Monthly salary credit", "transactionDate": "2025-11-01"},
    {"amount": 22000, "type": "EXPENSE", "category": "Rent", "description": "House rent November", "transactionDate": "2025-11-01"},
    {"amount": 4200, "type": "EXPENSE", "category": "Groceries", "description": "Big Basket monthly order", "transactionDate": "2025-11-02"},
    {"amount": 15000, "type": "EXPENSE", "category": "Shopping", "description": "Diwali shopping clothes and gifts", "transactionDate": "2025-11-05"},
    {"amount": 8000, "type": "EXPENSE", "category": "Shopping", "description": "Electronics - Bluetooth speaker", "transactionDate": "2025-11-06"},
    {"amount": 1500, "type": "EXPENSE", "category": "Food", "description": "Swiggy Diwali orders", "transactionDate": "2025-11-08"},
    {"amount": 599, "type": "EXPENSE", "category": "Entertainment", "description": "Netflix subscription", "transactionDate": "2025-11-07"},
    {"amount": 1100, "type": "EXPENSE", "category": "Utilities", "description": "Electricity bill", "transactionDate": "2025-11-15"},
    {"amount": 500, "type": "EXPENSE", "category": "Utilities", "description": "Internet bill", "transactionDate": "2025-11-15"},
    {"amount": 3200, "type": "EXPENSE", "category": "Food", "description": "Zomato and restaurant spending", "transactionDate": "2025-11-18"},
    {"amount": 1200, "type": "EXPENSE", "category": "Transport", "description": "Uber and Ola rides", "transactionDate": "2025-11-20"},
    {"amount": 5000, "type": "INCOME", "category": "Freelance", "description": "Freelance project payment", "transactionDate": "2025-11-25"},
    {"amount": 2800, "type": "EXPENSE", "category": "Groceries", "description": "DMart shopping", "transactionDate": "2025-11-26"},

    # December 2025
    {"amount": 85000, "type": "INCOME", "category": "Salary", "description": "Monthly salary credit", "transactionDate": "2025-12-01"},
    {"amount": 22000, "type": "EXPENSE", "category": "Rent", "description": "House rent December", "transactionDate": "2025-12-01"},
    {"amount": 4800, "type": "EXPENSE", "category": "Groceries", "description": "Big Basket monthly order", "transactionDate": "2025-12-03"},
    {"amount": 25000, "type": "EXPENSE", "category": "Travel", "description": "Goa trip flights and hotel", "transactionDate": "2025-12-20"},
    {"amount": 8000, "type": "EXPENSE", "category": "Travel", "description": "Goa trip food and activities", "transactionDate": "2025-12-22"},
    {"amount": 599, "type": "EXPENSE", "category": "Entertainment", "description": "Netflix subscription", "transactionDate": "2025-12-07"},
    {"amount": 1100, "type": "EXPENSE", "category": "Utilities", "description": "Electricity bill", "transactionDate": "2025-12-15"},
    {"amount": 500, "type": "EXPENSE", "category": "Utilities", "description": "Internet bill", "transactionDate": "2025-12-15"},
    {"amount": 2500, "type": "EXPENSE", "category": "Food", "description": "December dining out", "transactionDate": "2025-12-10"},
    {"amount": 1800, "type": "EXPENSE", "category": "Shopping", "description": "Christmas gifts", "transactionDate": "2025-12-18"},
    {"amount": 900, "type": "EXPENSE", "category": "Transport", "description": "Cab rides December", "transactionDate": "2025-12-12"},

    # January 2026
    {"amount": 85000, "type": "INCOME", "category": "Salary", "description": "Monthly salary credit", "transactionDate": "2026-01-01"},
    {"amount": 22000, "type": "EXPENSE", "category": "Rent", "description": "House rent January", "transactionDate": "2026-01-01"},
    {"amount": 4100, "type": "EXPENSE", "category": "Groceries", "description": "Big Basket monthly order", "transactionDate": "2026-01-04"},
    {"amount": 599, "type": "EXPENSE", "category": "Entertainment", "description": "Netflix subscription", "transactionDate": "2026-01-07"},
    {"amount": 1100, "type": "EXPENSE", "category": "Utilities", "description": "Electricity bill", "transactionDate": "2026-01-15"},
    {"amount": 500, "type": "EXPENSE", "category": "Utilities", "description": "Internet bill", "transactionDate": "2026-01-15"},
    {"amount": 1800, "type": "EXPENSE", "category": "Food", "description": "Swiggy and Zomato", "transactionDate": "2026-01-12"},
    {"amount": 700, "type": "EXPENSE", "category": "Transport", "description": "Uber rides January", "transactionDate": "2026-01-14"},
    {"amount": 12000, "type": "EXPENSE", "category": "Health", "description": "Dental treatment", "transactionDate": "2026-01-18"},
    {"amount": 2200, "type": "EXPENSE", "category": "Groceries", "description": "DMart shopping", "transactionDate": "2026-01-22"},
    {"amount": 3500, "type": "EXPENSE", "category": "Shopping", "description": "Winter clothing", "transactionDate": "2026-01-25"},
    {"amount": 10000, "type": "INCOME", "category": "Freelance", "description": "Freelance project payment", "transactionDate": "2026-01-28"},

    # February 2026
    {"amount": 85000, "type": "INCOME", "category": "Salary", "description": "Monthly salary credit", "transactionDate": "2026-02-01"},
    {"amount": 22000, "type": "EXPENSE", "category": "Rent", "description": "House rent February", "transactionDate": "2026-02-01"},
    {"amount": 4300, "type": "EXPENSE", "category": "Groceries", "description": "Big Basket monthly order", "transactionDate": "2026-02-03"},
    {"amount": 599, "type": "EXPENSE", "category": "Entertainment", "description": "Netflix subscription", "transactionDate": "2026-02-07"},
    {"amount": 1100, "type": "EXPENSE", "category": "Utilities", "description": "Electricity bill", "transactionDate": "2026-02-15"},
    {"amount": 500, "type": "EXPENSE", "category": "Utilities", "description": "Internet bill", "transactionDate": "2026-02-15"},
    {"amount": 3800, "type": "EXPENSE", "category": "Food", "description": "Valentine's dinner and food delivery", "transactionDate": "2026-02-14"},
    {"amount": 2100, "type": "EXPENSE", "category": "Food", "description": "Zomato orders February", "transactionDate": "2026-02-18"},
    {"amount": 800, "type": "EXPENSE", "category": "Transport", "description": "Cab rides February", "transactionDate": "2026-02-20"},
    {"amount": 6500, "type": "EXPENSE", "category": "Shopping", "description": "Laptop bag and accessories", "transactionDate": "2026-02-22"},
    {"amount": 2500, "type": "EXPENSE", "category": "Groceries", "description": "DMart shopping", "transactionDate": "2026-02-25"},

    # March 2026
    {"amount": 85000, "type": "INCOME", "category": "Salary", "description": "Monthly salary credit", "transactionDate": "2026-03-01"},
    {"amount": 22000, "type": "EXPENSE", "category": "Rent", "description": "House rent March", "transactionDate": "2026-03-01"},
    {"amount": 4600, "type": "EXPENSE", "category": "Groceries", "description": "Big Basket monthly order", "transactionDate": "2026-03-03"},
    {"amount": 599, "type": "EXPENSE", "category": "Entertainment", "description": "Netflix subscription", "transactionDate": "2026-03-07"},
    {"amount": 1100, "type": "EXPENSE", "category": "Utilities", "description": "Electricity bill", "transactionDate": "2026-03-15"},
    {"amount": 500, "type": "EXPENSE", "category": "Utilities", "description": "Internet bill", "transactionDate": "2026-03-15"},
    {"amount": 2200, "type": "EXPENSE", "category": "Food", "description": "Swiggy and Zomato March", "transactionDate": "2026-03-10"},
    {"amount": 900, "type": "EXPENSE", "category": "Transport", "description": "Uber rides March", "transactionDate": "2026-03-12"},
    {"amount": 45000, "type": "EXPENSE", "category": "Shopping", "description": "MacBook Pro purchase", "transactionDate": "2026-03-15"},
    {"amount": 2800, "type": "EXPENSE", "category": "Groceries", "description": "DMart shopping", "transactionDate": "2026-03-20"},
    {"amount": 1500, "type": "EXPENSE", "category": "Health", "description": "Annual health checkup", "transactionDate": "2026-03-22"},
    {"amount": 15000, "type": "INCOME", "category": "Freelance", "description": "Freelance project payment", "transactionDate": "2026-03-25"},
]


def seed():
    print("Logging in...")
    token = login()
    print(f"Token acquired. Seeding {len(TRANSACTIONS)} transactions...\n")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    success = 0
    failed = 0

    for txn in TRANSACTIONS:
        response = httpx.post(
            f"{BASE_URL_TXN}/api/transactions",
            json=txn,
            headers=headers
        )
        if response.status_code == 201:
            print(f"✅ {txn['transactionDate']} | {txn['type']} | {txn['category']} | ₹{txn['amount']}")
            success += 1
        else:
            print(f"❌ Failed: {txn} → {response.status_code} {response.text}")
            failed += 1
        time.sleep(0.1)

    print(f"\nDone. {success} succeeded, {failed} failed.")


if __name__ == "__main__":
    seed()