from db_manager import login, create_account, check_username, create_account
from slots import Slot, check_wins, calculate_payout, pay_table, line_bonus
from t_display import animate_spin, blink_animation, loading_animation
from user_manager import User
import getpass
import os
import sys


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