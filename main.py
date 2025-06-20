from slots import Slot, User, check_wins, calculate_payout, pay_table, line_bonus
from display import animate_spin, display_wins, wrong_input
from db_setup import login, create_user

def main():

    name = input("Username: ")
    password = input("Password: ")
    bank = int(input("bank: "))
    bet = int(input("bet: "))
    player = User(name=name, bank=bank, bet=bet)
    slot = Slot(input("Select 'a' for 3x3 or 'b' for 3x4: ") or 'a')
    first_spin = True
    # Collect login/creation input
    #logged_in = login(name, password)
    #if not logged_in:
    #    print("Login failed.")
    #    return
    #profile, name, bank, spins = logged_in

    while True:
        prompt = "Please press 'y' to spin, 'b' to change bet 'n' to quit: " if first_spin else "Press 'Enter' to spin again,'b' to change bet or 'n' to quit: "

        if player.bank < player.bet:
            print("Not enough money. Game over.")
            break

        start = input(prompt).strip().lower()

        while first_spin and start not in ('y', 'n'):
            wrong_input(prompt)
            start = input("").strip().lower()

        if start == 'y' or (not first_spin and start == ''):
            result = slot.spin()
            winning_lines = check_wins(result, slot.lines)
            player.bank -= player.bet
            payout = calculate_payout(winning_lines, pay_table, line_bonus, player.bet)
            
            animate_spin(result, winning_lines, slot.initial_slot_state, player.bank, payout)

            player.bank += payout
            first_spin = False

        elif start == 'b':
            try:
                new_bet = float(input("New bet amount: "))
                player.bet = new_bet

            except ValueError:
                print("Invalid amount.")

        elif start == 'n':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()