import datetime
import os

def clear_console():
    # Clear console screen for different operating systems
    os.system('cls' if os.name == 'nt' else 'clear')

# Define list for rooms with their details
rooms = [
    {
        "room_number": "01",
        "room_name": "Schefryn Chamber Room",
        "room_type": "Queen Size Bed, Pool",
        "price": 999.00
    },
    {
        "room_number": "02",
        "room_name": "Da Vinci Room",
        "room_type": "King Size Bed, Pool",
        "price": 699.69
    },
    {
        "room_number": "03",
        "room_name": "Christian Forge Room",
        "room_type": "Standard single bed",
        "price": 350.00
    },
    {
        "room_number": "04",
        "room_name": "Loydee Room",
        "room_type": "Triple bed",
        "price": 400.00
    },
    {
        "room_number": "05",
        "room_name": "Jay Suite Room",
        "room_type": "Double bed",
        "price": 200.00
    },
    {
        "room_number": "06",
        "room_name": "Rod ni Ney Room",
        "room_type": "Single Bed",
        "price": 150.00
    }
]

card_numbers = [
    {
        "card_number": "000-00-000",
        "security_code": "123",
        "balance": 5000
    },
    {
        "card_number": "123-00-000",
        "security_code": "123",
        "balance": 10000
    }
]

# Define list to store user information
users = []

# Define list to store reservations
reservations = []

# Define a list to store payment history
payment_history = []

# Add a global variable to track the currently logged-in user
current_user = None


def get_terminal_width():
    return os.get_terminal_size().columns


# Function to display centered text
def display_centered_text(text):
    terminal_width = get_terminal_width()
    padding = (terminal_width - len(text)) // 2
    print(" " * padding + text.ljust(terminal_width - padding))


# Function to validate card number format
def validate_card_number_format(card_number):
    # Check if the card number is in the correct format (e.g., 16 digits)
    if len(card_number) == 16 and card_number.isdigit():
        return True
    else:
        print("Invalid card number format. Please enter a 16-digit numeric card number.")
        return False

# Function to validate security code format
def validate_security_code_format(security_code):
    # Check if the security code is in the correct format (e.g., 3 digits)
    if len(security_code) == 3 and security_code.isdigit():
        return True
    else:
        print("Invalid security code format. Please enter a 3-digit numeric security code.")
        return False


# Function to validate card number
def validate_card_number(card_number):
    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        user_input = input("Enter card number: ").strip().lower()
        if user_input == 'b':
            return False  # Indicates user wants to go back
        elif any(card["card_number"] == user_input for card in card_numbers):
            return True  # Indicates valid card number
        else:
            print("Invalid card number. Please try again or press 'B' to go back.")
            attempts += 1
    print("Maximum attempts reached. Exiting.")
    return False

# Function to validate security code
def validate_security_code(card_number, security_code):
    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        user_input = input("Enter security code: ").strip().lower()
        if user_input == 'b':
            return False  # Indicates user wants to go back
        elif any(card["card_number"] == card_number and card["security_code"] == user_input for card in card_numbers):
            return True  # Indicates valid security code
        else:
            print("Invalid security code. Please try again or press 'B' to go back.")
            attempts += 1
    print("Maximum attempts reached. Exiting.")
    return False


# Update validate_card_payment function to allow the user to continue entering card information
def validate_card_payment(username, card_number, security_code, payment_amount):
    while True:
        # Validate card number format
        if not validate_card_number_format(card_number):
            return False

        # Validate security code format
        if not validate_security_code_format(security_code):
            return False

        # Perform card validation against stored card data
        for card in card_numbers:
            if card['card_number'] == card_number and card['security_code'] == security_code:
                if card['balance'] >= payment_amount:
                    # Deduct payment_amount from the card balance
                    card['balance'] -= payment_amount
                    # Find the reservations associated with the current user
                    user_reservations = [reservation for reservation in reservations if reservation['username'] == username]
                    for reservation in user_reservations:
                        if reservation['status'] == 'Unpaid':
                            # Update payment status in the reservation record
                            reservation['status'] = 'Paid'
                    # Add payment record to payment history with current time
                    payment_record = {
                        'username': username,
                        'room_number': None,  # Payment record doesn't belong to a specific room
                        'payment_amount': payment_amount,
                        'time_paid': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'status': 'Paid',  # Status will be 'Paid' for a payment
                        'reservation_status': 'Paid'  # Update reservation status to 'Paid'
                    }
                    payment_history.append(payment_record)
                    return True
                else:
                    print("Insufficient balance. Please try again with a different card or amount.")
                    break  # Break the loop to allow the user to re-enter card information
        else:
            print("Card number or security code is incorrect. Please try again.")
            break  # Break the loop to allow the user to re-enter card information
    return False


# Function to check if a room is occupied
def is_room_occupied(room_number):
    return any(reservation['room_number'] == room_number for reservation in reservations)


# Function to add payment record to payment history
def add_reservation_to_payment_history(username, room_number, status, payment_amount, payment_status):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reservation_record = {
        'username': username,
        'room_number': room_number,
        'payment_amount': payment_amount,
        'time_paid': current_time,  # Use current time as the time paid
        'check_in_date': 'N/A',  # No check-in date for payment
        'check_out_date': 'N/A',  # No check-out date for payment
        'status': status,
        'payment_status': payment_status,
        'reservation_status': status  # Add reservation status field
    }
    print("Reservation Record:", reservation_record)  # Print reservation record for debugging
    payment_history.append(reservation_record)
    print("Reservation recorded successfully.")


# Function to update reservation status and time created
def update_reservation_status_and_time_created(username, status):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for reservation in reservations:
        if reservation['username'] == username and reservation['status'] != status:
            reservation['status'] = status
            reservation['time_created'] = current_time


# Function for Login Menu
def login():
    global current_user  # Access the global variable
    print("Login Menu:")
    username = input("Username: ")
    password = input("Password: ")
    # Check if username exists in the database
    for user in users:
        if user['username'] == username:
            # Check if the password matches the one associated with the username
            if user['password'] == password:
                current_user = username  # Update the currently logged-in user
                return True, username
            else:
                print("Incorrect password. Please try again.")
                return False, None
    print("Username not found. Please sign up.")
    return False, None


# Function for Sign Up Menu
def sign_up():
    print("Sign Up Menu:")
    username = input("Username: ")
    # Check if username already exists in the database
    for user in users:
        if user['username'] == username:
            print("Username already exists. Please choose a different one.")
            return None, None  # Return None values if username exists
    password = input("Password: ")

    # Add the new user to the database
    users.append({
        'username': username,
        'password': password
    })
    return username, password  # Return username and password on successful sign-up


# Function to display main menu
def display_main_menu():
    clear_console()
    print("*" * get_terminal_width())
    display_centered_text("Welcome to Hotel BBCCDM!")
    print("*" * get_terminal_width())
    print("\nMain Menu:")
    print("1. Rooms/Services")
    print("2. Login")
    print("3. Sign Up")
    print("4. Exit")


# Function to display User Account Menu
def display_user_account_menu():
    global current_user  # Access the global variable
    while current_user:  # Check if a user is logged in
        clear_console()  # Clear the console before displaying the menu
        
        # Display user account menu header
        print(f"\nUser Account Menu (Logged in as {current_user}):")
        print("-" * get_terminal_width())
        
        # Display menu options
        print("{:<4}{:<40}".format("1.", "Rooms/Services"))
        print("{:<4}{:<40}".format("2.", "Payment"))
        print("{:<4}{:<40}".format("3.", "Logout"))
        
        print("-" * get_terminal_width())

        choice = input("Enter your choice: ").strip().lower()

        # Handle user's choice
        if choice == "1":
            # Rooms/Services
            display_rooms_services_menu(current_user)
        elif choice == "2":
            # Payment
            display_payment_menu()
        elif choice == "3":
            # Logout
            current_user = None  # Update the currently logged-in user to None
            print("Logged out successfully.")
            break  # Break out of the loop and return to the Main Menu
        else:
            print("Invalid choice. Please enter a valid option.")


# Function to display rooms/services menu
def display_rooms_services_menu(username=None):
    clear_console()  # Clear the console before displaying the menu
    
    # Display all available rooms
    print("\nAll Rooms:")
    print("-" * get_terminal_width())
    print("{:<8} {:<30} {:<25} {:<15} {:<10}".format("Room", "Name", "Amenities", "Price/Night (₱)", "Status"))
    print("-" * get_terminal_width())
    
    for room in rooms:
        status = "Occupied" if is_room_occupied(room['room_number']) else "Unoccupied"
        print("{:<8} {:<30} {:<25} {:<15.2f} {:<10}".format(room['room_number'], room['room_name'], room['room_type'], room['price'], status))

    print("")

    if username:
        print("Your Reservation Room:")
        user_reservations = [reservation for reservation in reservations if reservation['username'] == username]
        if user_reservations:
            for reservation in user_reservations:
                print(f"Room {reservation['room_number']}:")
                print(f"Check-in Date: {reservation['check_in_date']}")
                print(f"Check-out Date: {reservation['check_out_date']}")
        else:
            print("No Reservation.")
    else:
        print("No Reservation.")

    # Prompt the user to make a choice
    print("\nOptions:")
    print("-" * get_terminal_width())
    print("{:<4} {:<25}".format("1.", "Make a Reservation"))
    print("{:<4} {:<25}".format("2.", "Cancel Reservation"))
    print("{:<4} {:<25}".format("3.", "Back"))
    print("-" * get_terminal_width())

    while True:
        choice = input("Enter your choice: ").strip()

        # Handle the user's choice
        if choice == '1':
            if username:
                # Proceed with reservation
                make_reservation(username)
                return  # Return to the user account menu
            else:
                print("You need to sign up or log in first.")
        elif choice == '2':
            if username:
                # Proceed with cancellation
                cancel_reservation(username)
                return  # Return to the user account menu
            else:
                print("You need to sign up or log in first.")
        elif choice == '3':
            # Go back to the previous menu or user account menu
            if username:
                return  # Return to the user account menu
            else:
                break  # Break the loop and return to the main menu
        else:
            print("Invalid choice. Please try again.")


# Function to make a reservation
def make_reservation(username):
    global current_user
    print("Making a reservation...")
    available_rooms = [room for room in rooms if not is_room_occupied(room['room_number'])]
    if not available_rooms:
        print("No available rooms.")
        return

    print("Available Rooms:")
    for room in available_rooms:
        print(f"Room {room['room_number']}: {room['room_name']} - Price per Night: ₱{room['price']:.2f}")

    while True:
        room_number = input("Enter room number: ").strip()
        if room_number.isdigit():
            room_number = int(room_number)
            room_number = f"{room_number:02d}"  # Format as a two-digit string with leading zeros
            if is_room_occupied(room_number):
                print("This room is already occupied. Please choose another room.")
            elif room_number not in [room['room_number'] for room in rooms]:
                print("Invalid room number. Please choose a valid room.")
            else:
                break
        else:
            print("Invalid input. Please enter a valid room number.")

    check_in_date = input("Enter check-in date and time (MM/DD/YYYY HH:MM): ")
    check_out_date = input("Enter check-out date and time (MM/DD/YYYY HH:MM): ")
    
    # Default payment amount is derived from the room price
    room_price = next((room['price'] for room in rooms if room['room_number'] == room_number), 0)
    payment_amount = room_price
    payment_status = 'Unpaid'  # Default payment status
    
    # Add reservation with unpaid status and time created
    reservations.append({'username': current_user, 'room_number': room_number, 'check_in_date': check_in_date, 'check_out_date': check_out_date, 'status': 'Unpaid', 'time_created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    print("Reservation made successfully!")

    # Add the reservation to payment history
    add_reservation_to_payment_history(username, room_number, 'Reserved', payment_amount, payment_status)


# Function to cancel a reservation
def cancel_reservation(username):
    global current_user
    print("Canceling a reservation...")
    user_reservations = [reservation for reservation in reservations if reservation['username'] == username]
    if not user_reservations:
        print("You have no reservations.")
        return

    print("Your Reservations:")
    for reservation in user_reservations:
        print(f"Room {reservation['room_number']}: Check-in Date: {reservation['check_in_date']}, Check-out Date: {reservation['check_out_date']}")

    while True:
        room_number_to_cancel = input("Enter room number to cancel reservation: ").strip()
        if room_number_to_cancel.isdigit():
            room_number_to_cancel = int(room_number_to_cancel)
            room_number_to_cancel = f"{room_number_to_cancel:02d}"  # Format as a two-digit string with leading zeros
            if room_number_to_cancel in [reservation['room_number'] for reservation in user_reservations]:
                for reservation in user_reservations:
                    if reservation['room_number'] == room_number_to_cancel:
                        # Remove the reservation from the list
                        canceled_reservation = reservation
                        reservations.remove(reservation)
                        print("Reservation canceled successfully!")
                        # Add cancellation record to payment history with payment amount set to 0 and payment status set to 'Unpaid'
                        add_reservation_to_payment_history(username, room_number_to_cancel, 'Cancelled', 0, 'Unpaid')
                        return
            else:
                print("No reservation found for the entered room number.")
        else:
            print("Invalid input. Please enter a valid room number.")


def display_payment_menu():
    clear_console()  # Clear the console before displaying the menu
    print("Payment Menu:")
    print("1. Make Payment")
    print("2. View Payment History")
    print("3. Back")

    choice = input("Enter your choice: ").strip()

    if choice == '1':
        make_payment(current_user)
    elif choice == '2':
        display_payment_history(current_user)
    elif choice == '3':
        # Go back to the previous menu
        pass
    else:
        print("Invalid choice. Please enter a valid option.")


# Update make_payment function to correctly update total amount due after payment and call process_payment
def make_payment(username):
    clear_console()
    total_amount = calculate_total_amount(username)
    print("Total Amount Due: ₱{:.2f}".format(total_amount))
    if total_amount == 0:
        print("No payment due. Your bill is already settled.")
        return

    print("Available Payment Methods:")
    print("1. Credit/Debit Card")
    print("2. Back")
    
    choice = input("Enter your choice: ").strip()

    if choice == '1':
        # Process credit/debit card payment
        card_number = input("Enter card number: ").strip()
        security_code = input("Enter security code: ").strip()
        while True:
            payment_input = input("Enter payment amount: ₱").strip()
            if payment_input:
                try:
                    payment_amount = float(payment_input)
                    if payment_amount <= 0:
                        print("Payment amount must be greater than zero.")
                    elif payment_amount > total_amount:
                        print("Payment amount exceeds the total amount due.")
                    else:
                        break  # Break the loop if payment amount is valid
                except ValueError:
                    print("Invalid input. Please enter a valid numeric value.")
            else:
                print("Payment amount cannot be empty.")
        else:
            print("Invalid choice. Please enter a valid option.")
            return

        if validate_card_payment(username, card_number, security_code, payment_amount):
            if process_payment(username, total_amount, payment_amount, card_number, security_code):
                print("Payment successful!")
                # Update the total amount due
                total_amount -= payment_amount
                if total_amount < 0:
                    total_amount = 0  # Ensure total amount due is not negative
                print("Updated Total Amount Due: ₱{:.2f}".format(total_amount))
                return  # Return after successful payment
            else:
                print("Payment failed. Please try again.")
        else:
            print("Payment failed. Please try again.")
    elif choice == '2':
        # Go back
        pass
    else:
        print("Invalid choice. Please enter a valid option.")



# Update process_payment function to correctly record payment in payment history
def process_payment(username, total_amount, payment_amount, card_number, security_code):
    for card in card_numbers:
        if card['card_number'] == card_number and card['security_code'] == security_code:
            if card['balance'] >= payment_amount:
                # Deduct payment_amount from the card balance
                card['balance'] -= payment_amount
                # Update the reservation status to 'Paid'
                for reservation in reservations:
                    if reservation['username'] == username and reservation['status'] == 'Unpaid':
                        reservation['status'] = 'Paid'
                        break
                # Add payment record to payment history with current time
                payment_record = {
                    'username': username,
                    'room_number': None,  # Payment record doesn't belong to a specific room
                    'payment_amount': payment_amount,
                    'time_paid': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'status': 'Paid',  # Status will be 'Paid' for a payment
                    'reservation_status': 'Paid'  # Update reservation status to 'Paid'
                }
                payment_history.append(payment_record)
                # Update the total amount due
                total_amount -= payment_amount
                if total_amount < 0:
                    total_amount = 0  # Ensure total amount due is not negative
                return True
            else:
                print("Insufficient balance. Please try again with a different card or amount.")
                return False
    print("Card number or security code is incorrect. Please try again.")
    return False



# Function to calculate total amount due
def calculate_total_amount(username):
    total_amount = 0
    for reservation in reservations:
        if reservation['username'] == username and 'payment_status' not in reservation:
            room_number = reservation['room_number']
            # Find the room in the rooms list based on its room number
            room = next((room for room in rooms if room['room_number'] == room_number), None)
            if room:
                total_amount += room['price']
    return total_amount


# Update display_view_bill_menu function to correctly call make_payment
def display_view_bill_menu(username):
    clear_console()  # Clear the console before displaying the menu
    total_amount = calculate_total_amount(username)
    print("Total Amount Due: ₱{:.2f}".format(total_amount))
    if total_amount == 0:
        print("No payment due. Your bill is already settled.")
        input("\nPress Enter to continue...")
        return

    print("Available Payment Methods:")
    print("1. Credit/Debit Card")
    print("2. Back")
    
    choice = input("Enter your choice: ").strip()

    if choice == '1':
        # Process credit/debit card payment
        card_number = input("Enter card number: ").strip()
        security_code = input("Enter security code: ").strip()
        while True:
            payment_input = input("Enter payment amount: ₱").strip()
            if payment_input:
                try:
                    payment_amount = float(payment_input)
                    break  # Break the loop if conversion is successful
                except ValueError:
                    print("Invalid input. Please enter a valid numeric value.")
            else:
                print("Payment amount cannot be empty.")
        if validate_card_payment(username, card_number, security_code, payment_amount):
            if process_payment(username, total_amount, payment_amount, card_number, security_code):
                print("Payment successful!")
                input("\nPress Enter to continue...")
                return
            else:
                print("Payment failed. Please try again.")
        else:
            print("Payment failed. Please try again.")
    elif choice == '2':
        # Go back
        pass
    else:
        print("Invalid choice. Please enter a valid option.")


# Function to display payment menu
def display_payment_history(username):
    clear_console()  # Clear the console before displaying the menu
    print("Payment History:")
    user_payment_history = [record for record in payment_history if record['username'] == username]
    if not user_payment_history:
        print("No payment history for this user.")
        input("\nPress Enter to continue...")
        return

    print("{:<20} {:<15} {:<15} {:<20}".format("Time Paid", "Payment Amount", "Payment Status", "Room"))  
    print("-" * get_terminal_width())

    for record in user_payment_history:
        time_paid = record.get('time_paid', 'N/A')  
        payment_amount = record.get('payment_amount', 'N/A')
        payment_status = record.get('status', 'N/A')  
        room_number = record.get('room_number', 'N/A')
        
        if None in (time_paid, payment_amount, payment_status):
            print("Some payment details are missing.")
        else:
            print("{:<20} {:<15.2f} {:<15} {:<20}".format(time_paid, payment_amount, payment_status, room_number))

    input("\nPress Enter to continue...")



# Update display_payment_history function to fetch payment amount and payment status correctly
def display_payment_history(username):
    clear_console()  # Clear the console before displaying the menu
    print("Payment History:")
    user_payment_history = [record for record in payment_history if record['username'] == username]
    if not user_payment_history:
        print("No payment history.")
        input("\nPress Enter to continue...")
        return

    print("{:<15} {:<15} {:<15} {:<20}".format("Room", "Payment Amount", "Time Paid", "Payment Status"))  # Update column header
    print("-" * get_terminal_width())

    for record in user_payment_history:
        room_number = record.get('room_number', 'N/A')
        payment_amount = record.get('payment_amount', 'N/A')
        time_paid = record.get('time_paid', 'N/A')  # Update to 'time_paid'
        payment_status = record.get('reservation_status', 'N/A')  # Update to 'reservation_status'
        
        if None in (room_number, payment_amount, time_paid):
            print("Some payment details are missing.")
        else:
            print("{:<15} {:<15.2f} {:<15} {:<20}".format(room_number, payment_amount, time_paid, payment_status))

    input("\nPress Enter to continue...")


# Main Program Loop
while True:
    display_main_menu()

    choice = input("\nEnter your choice: ").strip()

    if choice == '1':
        # Rooms/Services
        display_rooms_services_menu()
    elif choice == '2':
        # Login
        success, username = login()
        if success:
            display_user_account_menu()  # Display user account menu after successful login
    elif choice == '3':
        # Sign Up
        username, _ = sign_up()  # Discard the password from sign-up
        if username:
            print(f"Sign up successful! Welcome, {username}.")
            display_user_account_menu()  # Display user account menu after successful sign-up
    elif choice == '4':
        # Exit
        clear_console()
        print("*" * get_terminal_width())
        display_centered_text("Thank you for using Hotel BBCCDM.")
        display_centered_text("Goodbye, Have a Good Day!")
        print("*" * get_terminal_width())
        break
    else:
        print("Invalid choice. Please enter a valid option.")
