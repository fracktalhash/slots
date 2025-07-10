import copy
from decimal import Decimal, getcontext
import random
from rich.console import Console
from time import sleep
import time

console = Console()

SYMBOL = ["♥", "♠", "Δ", "Ω", "Ψ", "♝", "♞", "♜", "♛", "♚"]


def counter(amount):  # Counter animation flow
    getcontext().prec = len(str(amount))  # control visual float precision

    amount = Decimal(str(amount))  # Converts amount str to a Decimal object
    steps = 200  # Frames per second
    increment = amount / Decimal(steps)  # Total winning divided by the steps (how much does it have to increase per frame)
    sleep_time = 3.5 / steps  # by dividing the desired duration time in sec by the number of steps it gives us the pause value for the for loop

    value = Decimal("0.00")  # Initialized the counter at 0.00
    for _ in range(steps):  # Value incrementing loop
        console.print(f"Bank [bold green]${value:.2f}[/bold green]", end="\r", highlight=False)  # Print with formatting bolded green text with
        value += increment
        time.sleep(sleep_time)

    # Ensure final print is exact
    console.print(f"Bank [bold green]${amount:.2f}[/bold green]")


def loading_animation(message="Loading . . ."):
    steps = 4 * len(message)  # Number of prints * message length = total frames
    sleep_time = 3.5 / steps  # Delay to match the desired duration
    clear_line = " " * (len(message) + 5)  # pad to fully clear leftovers

    for _ in range(4):  # repeat animation 4 times
        for i in range(len(message)):  # Loop for adding letters to the print
            line = f"{message[:i+1]}"  # Adding one letter per inner loop
            print(clear_line, end="\r", flush=True)  # Clear /next frame
            print(line, end="\r", flush=True)  # Print frame
            time.sleep(sleep_time)  # Pause between frames

    print(clear_line, end="\r")  # final clear


def blink_animation(prompt):
    console.clear()
    console.print(f"[bold blink]{prompt}[/bold blink]")


def animate_spin(result, winning_lines, initial_slot_state, bank, payout=0):
    """Renders the different symbols randomly until the actual symbol that resulted from Slot.spin lands in its correct place."""

    spin_reel = copy.deepcopy(SYMBOL)  # Copy the list of symbols to generate the "reels"
    num_columns = len(result[0])  # The length of the result determines how many cols to draw
    start_times = [None] * num_columns  # The start time of each col to simulate a staggard start
    column_done = [False] * num_columns  # Flag to determine whether a col is still spinning
    total_start_time = time.time()  # Snap shot of the starting spinning time

    while not all(column_done):  # loop until all cols are done spinning
        current_time = time.time()

        for col in range(num_columns):
            if start_times[col] is None:
                if current_time - total_start_time >= col * 0.3:  # Staggard start control
                    start_times[col] = current_time

            if start_times[col] is not None and not column_done[col]:
                # While spinning, assign random symbols to each cell
                if current_time - start_times[col] < 3:
                    for row in range(len(result)):
                        initial_slot_state[row][col] = random.choice(spin_reel)

                else:
                    # When done assign final result to all cells
                    for row in range(len(result)):
                        initial_slot_state[row][col] = copy.deepcopy(result[row][col])
                    column_done[col] = True

        display_wins(initial_slot_state, bank)  # show intermediate frames
        time.sleep(0.065)

    display_wins(result, bank, winning_lines, payout)  # Final display


def display_wins(board, bank, winning_lines=[], payout=0):
    """Print logic for the slot machine states including winnings and bank"""
    display_board = copy.deepcopy(board)  # Copy to change the board state with out altering it
    console.clear()

    if winning_lines:
        for line in winning_lines:
            for x, y in line["coords"]:
                display_board[x][y] = f"[bold purple blink]{board[x][y]}[/bold purple blink]"  # Highlight all winning coordinates

        console.print(
            f"[bold purple blink]!!!WINNER!!![/bold purple blink]{'\n'}{' '+'___' * (len(board[0]))}{'\n'}{'|'}{'| \n|'.join([' | '.join(row) for row in display_board])}{'|'}{'\n'}{' '+'¯¯¯' * len(board[0])}"
        )  # Fancy border + formatted winning board display

        counter(bank + payout)  # Payout animation

    else:
        console.clear()
        console.print(f"Bank [bold teal]${bank:.2f}[/bold teal]")
        console.print(
            f"{' '+'___' * (len(board[0]))}{'\n'}{'|'}{'| \n|'.join([' | '.join(row) for row in display_board])}{'|'}{'\n'}{' '+'¯¯¯' * len(board[0])}"
        )  # Fancy border non-win screen
