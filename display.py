import copy
from pprint import pformat
import random
from rich.console import Console
from time import sleep
import time

console = Console()

SYMBOL = ['♥', '♠', 'Δ', 'Ω', 'Ψ',
          '♝', '♞', '♜', '♛', '♚']

def wrong_input(prompt):

    console.clear()
    console.print(f"[bold blink]{prompt}[/bold blink]")

def animate_spin(result, winning_lines, initial_slot_state, bank, payout =0):

    spin_reel = copy.deepcopy(SYMBOL)
    num_columns = len(result[0])
    start_times = [None] * num_columns
    column_done = [False] * num_columns
    total_start_time = time.time()

    while not all(column_done):
        current_time = time.time()
        
        for col in range(num_columns):
            if start_times[col] is None:
                if current_time - total_start_time >= col * 0.3:
                    start_times[col] = current_time

            if start_times[col] is not None and not column_done[col]:
                if current_time - start_times[col] < 3:
                    for row in range(len(result)):
                        initial_slot_state[row][col] = random.choice(spin_reel)
                        
                else:
                    for row in range(len(result)):
                        initial_slot_state[row][col] = copy.deepcopy(result[row][col])
                    column_done[col] = True

        display_wins(initial_slot_state, bank, [])
        time.sleep(0.065)

    display_wins(result, bank, winning_lines, payout)

def display_wins(board, bank, winning_lines =[], payout =0):
    
    console.clear()
    display_board = copy.deepcopy(board)
    console.print(f"Bank ${bank:.2f}")
    
    for line in winning_lines:
        for x, y in line["coords"]:
            display_board[x][y] = f"[bold purple blink]{board[x][y]}[/bold purple blink]"

    for row in display_board:
        console.print(" | ".join(row))

    if winning_lines:
        console.print(f"[bold green]Winner!!![/bold green]")

    else:
        console.clear()
        print(f"Bank ${bank:.2f}")
        console.print("\n".join([" | ".join(row) for row in board]))