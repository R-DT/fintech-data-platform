#prints a greeting message and personal information
print("Hello, World!")
print("my name is Raphael.")
print ("I am a software deveoper.")

#prints the current time
from datetime import datetime
current_time = datetime.now()
print(f"The current time is: {current_time}")


#creates a list for 20 numbers and does arithmetic operations on them
numbers = [i for i in range(1, 21)]
print(f"Numbers: {numbers}")
print(f"Sum: {sum(numbers)}")
print(f"Average: {sum(numbers) / len(numbers)}")
print(f"Maximum: {max(numbers)}")
print(f"Minimum: {min(numbers)}")


# saves results to a file including greeting message, personal information, current time and arithmetic operations
with open("results.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("my name is Raphael.\n")
    file.write("I am a software developer.\n")
    file.write(f"The current time is: {current_time}\n")
    
    file.write(f"Numbers: {numbers}\n")
    file.write(f"Sum: {sum(numbers)}\n")
    file.write(f"Average: {sum(numbers) / len(numbers)}\n")
    file.write(f"Maximum: {max(numbers)}\n")
    file.write(f"Minimum: {min(numbers)}\n")

    #Create a CSV file containing 100 fictional bank transactions with these columns: 
    # TransactionID, Customer, Amount, TransactionType, Date.
    import csv
    import random
    print("Creating fictional bank transactions...")
    with open("transactions.csv", "w", newline="") as csvfile:
        fieldnames = ["TransactionID", "Customer", "Amount", "TransactionType", "Date"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(1, 101):
            transaction_id = f"T{i:03d}"
            customer = f"Customer_{random.randint(1, 20)}"
            amount = round(random.uniform(10.0, 1000.0), 2)
            transaction_type = random.choice(["Deposit", "Withdrawal"])
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            writer.writerow({
                "TransactionID": transaction_id,
                "Customer": customer,
                "Amount": amount,
                "TransactionType": transaction_type,
                "Date": date
            })

#Read the CSV.
#read the CSV file and print the first 5 transactions
import csv
with open("transactions.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    print("First 5 transactions:")
    for i, row in enumerate(reader):
        if i < 5:
            print(row)
        else:
            break

# calculate the total amount of deposits and withdrawals

total_deposits = 0
total_withdrawals = 0
with open("transactions.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        amount = float(row["Amount"])
        transaction_type = row["TransactionType"]
        
        if transaction_type == "Deposit":
            total_deposits += amount
        elif transaction_type == "Withdrawal":
            total_withdrawals += amount

print(f"Total deposits: {total_deposits}")
print(f"Total withdrawals: {total_withdrawals}")

#Calculate deposits only and withdrawals only, find the largest transaction
#and print the results to a new CSV file called "transaction_summary.csv"

largest_deposit = 0
largest_withdrawal = 0

with open("transactions.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        amount = float(row["Amount"])
        transaction_type = row["TransactionType"]
        
        if transaction_type == "Deposit":
            if amount > largest_deposit:
                largest_deposit = amount
        elif transaction_type == "Withdrawal":
            if amount > largest_withdrawal:
                largest_withdrawal = amount

print(f"Largest deposit: {largest_deposit}")
print(f"Largest withdrawal: {largest_withdrawal}")

# Print the results to a new CSV file
with open("transaction_summary.csv", "w", newline="") as csvfile:
    fieldnames = ["TotalDeposits", "TotalWithdrawals", "LargestDeposit", "LargestWithdrawal"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({
        "TotalDeposits": total_deposits,
        "TotalWithdrawals": total_withdrawals,
        "LargestDeposit": largest_deposit,
        "LargestWithdrawal": largest_withdrawal
    })

#Calls a free public REST API (for example, JSONPlaceholder).
#Retrieves JSON data.
#Converts it into a pandas DataFrame.
#Saves it as a CSV file.

import requests
import pandas as pd

response = requests.get("https://jsonplaceholder.typicode.com/posts")
if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv("api_data.csv", index=False)
    print("API data saved to api_data.csv")

# update the code to include error handling for the API call 
# and file operations, ensuring that any exceptions are caught and logged appropriately.

import logging

logging.basicConfig(level=logging.INFO)

try:
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    response.raise_for_status()  # Raise an error for HTTP errors
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv("api_data.csv", index=False)
    logging.info("API data saved to api_data.csv")
except requests.RequestException as e:
    logging.error(f"Error fetching API data: {e}")
except Exception as e:
    logging.error(f"Unexpected error occurred: {e}")

# combine the API call and file operations into a single code 
# that handles errors gracefully and logs them appropriately.

import requests
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

try:
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    response.raise_for_status()  # Raise an error for HTTP errors
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv("api_data.csv", index=False)
    logging.info("API data saved to api_data.csv")
except requests.RequestException as e:
    logging.error(f"Error fetching API data: {e}")
except Exception as e:
    logging.error(f"Unexpected error occurred: {e}")

#Add Live Timestamps to the Script
import requests
import pandas as pd
import logging
from datetime import datetime

#Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

try:
    logging.info("Starting API data extraction pipeline...")
    response = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=20)
    response.raise_for_status()
    
    # Process the verified connection data
    data = response.json()
    df = pd.DataFrame(data)
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    output_filename = f"api_data_{current_date}.csv"
    
    df.to_csv(output_filename, index=False)
    logging.info(f"API data successfully saved to {output_filename}")

except requests.RequestException as e:
    logging.error(f"Database/API pipeline transport layer failure: {e}")
except Exception as e:
    logging.error(f"Unexpected operational data failure: {e}")















