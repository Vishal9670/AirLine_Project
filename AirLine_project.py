import pyodbc  # Import the pyodbc library for SQL Server connection

# Connection to SQL Server
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=DESKTOP-MVGO5U1\\SQLEXPRESS;'  # Replace with your SQL Server name
    'DATABASE=Airlines;'  # Replace with your database name
    'UID=vishal;'  # Replace with your SQL Server username
    'PWD=Vishal;'  # Replace with your SQL Server password
     "Trusted_Connection=yes" 
)

import random
import string

cursor = conn.cursor()

# Function to generate a random PNR ID
def generate_pnr():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Function to insert food items into the database
def insert_food_item(food_name, price):
    cursor.execute("INSERT INTO FoodItems (FoodName, Price) VALUES (?, ?)", (food_name, price))
    conn.commit()
    print(f"Inserted: {food_name} with price {price}")

# Function to add flight details (for source and destination information)
def add_flight(flight_name, departure_place, destination, flight_day, flight_time, price):
    cursor.execute("""
        INSERT INTO FlightDetails (FlightName, DeparturePlace, Destination, FlightDay, FlightTime, Price)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (flight_name, departure_place, destination, flight_day, flight_time, price))
    conn.commit()
    print(f"Flight {flight_name} from {departure_place} to {destination} added successfully!")

# Function to book a flight and generate PNR ID
def book_flight(customer_name, contact_number, flight_id):
    # Insert customer details
    cursor.execute("""
        INSERT INTO CustomerDetails (CustomerName, ContactNumber)
        VALUES (?, ?)
    """, (customer_name, contact_number))
    
    # Get the newly inserted CustomerID
    customer_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]
    
    # Get flight details for the given flight_id
    cursor.execute("SELECT Price FROM FlightDetails WHERE FlightID = ?", (flight_id,))
    flight_price = cursor.fetchone()[0]
    
    # Generate a random PNR ID
    pnr_id = generate_pnr()
    
    # Insert ticket details with the PNR ID and total price
    cursor.execute("""
        INSERT INTO TicketDetails (CustomerID, FlightID, PNR, TotalPrice)
        VALUES (?, ?, ?, ?)
    """, (customer_id, flight_id, pnr_id, flight_price))
    conn.commit()
    
    print(f"Flight booked for {customer_name}.")
    print(f"Your PNR ID is: {pnr_id}")
    print(f"Total Price: {flight_price}")

# Function to retrieve ticket details by PNR ID
def retrieve_ticket_by_pnr(pnr_id):
    cursor.execute("""
        SELECT C.CustomerName, F.FlightName, F.DeparturePlace, F.Destination, F.FlightDay, F.FlightTime, T.TotalPrice
        FROM CustomerDetails C
        JOIN TicketDetails T ON C.CustomerID = T.CustomerID
        JOIN FlightDetails F ON T.FlightID = F.FlightID
        WHERE T.PNR = ?
    """, (pnr_id,))
    
    ticket = cursor.fetchone()
    if ticket:
        print(f"Ticket for {ticket.CustomerName} (PNR: {pnr_id})")
        print(f"Flight: {ticket.FlightName} | From: {ticket.DeparturePlace} | To: {ticket.Destination}")
        print(f"Date: {ticket.FlightDay}, Time: {ticket.FlightTime}, Total Price: {ticket.TotalPrice}")
    else:
        print("No ticket found for this PNR ID.")

# Main Menu
def main_menu():
    while True:
        print("\n1. Add Food Item")
        print("2. Add Flight Details")
        print("3. Book a Flight")
        print("4. Retrieve Ticket by PNR")
        print("5. Exit")
        
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            food_name = input("Enter food name: ")
            price = int(input("Enter price: "))
            insert_food_item(food_name, price)
        
        elif choice == 2:
            flight_name = input("Enter flight name: ")
            departure_place = input("Enter departure place: ")
            destination = input("Enter destination: ")
            flight_day = input("Enter flight date (YYYY-MM-DD): ")
            flight_time = input("Enter flight time (HH:MM): ")
            price = int(input("Enter flight price: "))
            add_flight(flight_name, departure_place, destination, flight_day, flight_time, price)
        
        elif choice == 3:
            customer_name = input("Enter customer name: ")
            contact_number = int(input("Enter contact number: "))
            flight_id = int(input("Enter flight ID: "))
            book_flight(customer_name, contact_number, flight_id)
        
        elif choice == 4:
            pnr_id = input("Enter the PNR ID to retrieve the ticket: ")
            retrieve_ticket_by_pnr(pnr_id)
        
        elif choice == 5:
            print("Exiting...")
            break

# Call the main menu function to start the program
main_menu()

# Close the connection once the operations are done
conn.close()
