from db_manager import login, create_account, check_username, create_account
from slots import Slot, check_wins, calculate_payout, pay_table, line_bonus
from t_display import animate_spin, blink_animation, loading_animation
from user_manager import User
import getpass
import os
import sys


max_deposit = 9_000_000_000_000_000_000  # This value wins the game


def login_in() -> User:  # This function creates the player class through user input
    login_prompt = "press '1' to signin '2' to register: "
    user_login = False  # Track the player object creation and user authentication
    user_input = None  # Sets up input order and ensures user flow across while loops
    while user_login == False:  # Starts the login loop
        if user_input not in (
            "1",
            "2",
        ):  # If the users inputs anything other than '1' or '2' re-prompt
            user_input = input(login_prompt)  # Right prompt at loop start
            login_prompt = "Invalid selection, try again. \npress '1' to signin '2' to register: "  # Login ('1') or Register('2') re-try prompt

        if user_input == "1":  # Login selection
            attempts = 0  # Initializes throttling mechanism
            while attempts < 3:  # After 3 attempts user has field out of the loop
                name = input("Username: ")
                password = getpass.getpass("Password: ")
                login_result = login(name, password)
                if login_result and isinstance(login_result, tuple):  # Successful login
                    user_name, result = login_result  # Unpack tuple for player object creation
                    user_login = True  # Flag flip signaling login
                    print(f"You are logged in as {name}")
                    break  # Out of the login loop

                elif login_result == "2":  # Exit out of login in loop db not found
                    loading_animation("Initializing . . .")
                    print("Database initialized.")
                    user_login = False  # User is still not logged in
                    user_input = "2"  # Transfer to the registration loop
                    break

                else:  # User did not input correct login data
                    os.system("cls" if os.name == "nt" else "clear")  # Clear the terminal for dramatic effect
                    print("Wrong username or password.\n")
                    attempts += 1  # Increment attempts by 1

            if user_input == "2":  # To the loop start for registration redirection
                continue

            if not user_login and not user_input == "2":  # Failed out of login loop
                user_input = input(
                    "Exceeded number of attempts. \nPress 2 to register, or any key other key to quit: "
                )  # Options to leave the game or try registering
                if user_input != "2":  # Exit game
                    os.system("cls" if os.name == "nt" else "clear")
                    print("Goodbye!")
                    sys.exit(0)
            continue  # User decided to Login

        elif user_input == "2":
            os.system("cls" if os.name == "nt" else "clear")
            print("Create a user profile")
            while True:  # Gather account creation info
                name = input("Username: ")
                if check_username(name):
                    password = getpass.getpass("Password: ")  # No echo user input
                    password1 = getpass.getpass("Confirm password: ")
                    if password == password1:  # Ensures password creation
                        bank = input_val("deposit")  # Validates deposit input
                        user_name, result = create_account(name, password, bank)
                        loading_animation("Creating user . . .")
                        print(f"You are logged in as {name}")
                        user_login = True  # Auto login after creation
                        break

                    else:
                        os.system("cls" if os.name == "nt" else "clear")
                        blink_animation("Sorry password did not match try again")
                else:
                    os.system("cls" if os.name == "nt" else "clear")
                    blink_animation(f"Username {name} has been taken. Please use another one.")
                    continue

    bank, spin_count = result  # Unpack data for player object
    player = User(user_name, bank, spin_count)  # initialize player
    return player


def input_val(message: str) -> float:
    message1 = f"Place a {message}: "
    message2 = "Invalid amount. Please enter a value grater than zero: "
    message2a = "Invalid amount. Please choose a number less than 9 QUADRILLION!!!: "
    message3 = "That was not a number. Please enter a numeric value: "

    user_input = input(message1)
    while True:
        try:
            new_value = float(user_input)
            if new_value <= 0:  # Values have to be higher than 0
                user_input = input(message2)
            elif new_value > max_deposit:  # Max values for sqlite is 9 quadrillion
                user_input = input(message2a)
            else:
                return new_value

        except ValueError:
            user_input = input(message3)


def main():
    player = login_in()  # Setts up player object
    slot = Slot(input("Select 'a' for 3x3 or 'b' for 3x4: ") or "a")  # Setts up the slot's size
    player.bet = input_val("bet")  # sets Bets
    first_spin = True  # Starts flag for first spin

    while True:  # Spin, bet, play option loop for every spin
        prompt = (
            "Please press 'y' to spin, 'b' to change bet 'n' to quit: "
            if first_spin
            else "Press 'Enter' to spin again,'b' to change bet or 'n' to quit: "
        )  # User must confirm with 'y' fist spin other wise they can just hit 'enter'

        if player.bank < player.bet and player.bank != 0.0:  # If the player's bank can cover the bet
            print("Not enough money for the current bet. Place a new one")
            player.bet = input_val("bet")  # Ask for a new bet
        elif player.bank == 0.0:  # If player's bank hits 0 they lose
            print(f"You spun {player.spin_count} times before losing")
            print("Not enough money. Game over.")
            print("User will now be deleted")

            break  # Game ends

        start = input(prompt).strip().lower()  # User input for spins first and Nth

        while first_spin and start not in ("y", "n", "b"):  # Input validation for start var
            blink_animation(prompt)  # Blink animation for choice emphasis
            start = input("").strip().lower()

        if start == "y" or (not first_spin and start == ""):  # Spins the slot machine
            result = slot.spin()  # Runs the random result generation logic
            winning_lines = check_wins(result, slot.lines)  # Checks if the user won
            player.bank -= player.bet  # Subtracts the bet from player's bank
            payout = calculate_payout(winning_lines, pay_table, line_bonus, player.bet)  # Calculates winnings
            animate_spin(result, winning_lines, slot.initial_slot_state, player.bank, payout)  # Animation logic
            player.bank += payout  # Adds winnings
            player.spin_count += 1  # Increases player's spins
            player.save()  # Saves changes to database
            first_spin = False  # Flips flag for first spin
        elif start == "b":  # Initiates bet changing logic
            player.bet = input_val("bet")
            first_spin = True  # First spin Flag is set back to confirm with 'y'
        elif start == "n":  # Player ends game
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:  # CTRL ends the game gracefully
        os.system("cls" if os.name == "nt" else "clear")
        print("Goodbye! Thanks for playing.")
        sys.exit(0)
