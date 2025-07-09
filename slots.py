import copy
import random

SYMBOL = ["♥", "♠", "Δ", "Ω", "Ψ", "♝", "♞", "♜", "♛", "♚"]

SYMBOL_WEIGHTS_3x4 = {"♥": 0.3, "♠": 0.3, "Δ": 0.1, "Ω": 0.1, "Ψ": 0.1, "♝": 0.025, "♞": 0.025, "♜": 0.005, "♛": 0.005, "♚": 0.002}

SYMBOL_WEIGHTS_3x3 = {"♥": 0.13, "♠": 0.13, "Δ": 0.13, "Ω": 0.13, "Ψ": 0.07, "♝": 0.07, "♞": 0.07, "♜": 0.07, "♛": 0.07, "♚": 0.02}

LINES_3x4 = [
    {"coords": [(0, 0), (0, 1), (0, 2), (0, 3)], "type": "horizontal"},
    {"coords": [(1, 0), (1, 1), (1, 2), (1, 3)], "type": "horizontal"},
    {"coords": [(2, 0), (2, 1), (2, 2), (2, 3)], "type": "horizontal"},
    {"coords": [(0, 0), (1, 1), (1, 2), (2, 3)], "type": "diagonal"},
    {"coords": [(2, 0), (1, 1), (1, 2), (0, 3)], "type": "diagonal"},
    {"coords": [(0, 0), (1, 1), (0, 2), (1, 3)], "type": "zigzag"},
    {"coords": [(1, 0), (0, 1), (1, 2), (0, 3)], "type": "zigzag"},
    {"coords": [(1, 0), (2, 1), (1, 2), (2, 3)], "type": "zigzag"},
    {"coords": [(2, 0), (1, 1), (2, 2), (1, 3)], "type": "zigzag"},
]  # winning lines in a 2d matrix for 3X4 config

LINES_3x3 = [
    {"coords": [(0, 0), (0, 1), (0, 2)], "type": "horizontal"},
    {"coords": [(1, 0), (1, 1), (1, 2)], "type": "horizontal"},
    {"coords": [(2, 0), (2, 1), (2, 2)], "type": "horizontal"},
    {"coords": [(0, 0), (1, 1), (2, 2)], "type": "diagonal"},
    {"coords": [(2, 0), (1, 1), (0, 2)], "type": "diagonal"},
    {"coords": [(0, 0), (1, 1), (0, 2)], "type": "zigzag"},
    {"coords": [(1, 0), (0, 1), (1, 2)], "type": "zigzag"},
    {"coords": [(1, 0), (2, 1), (1, 2)], "type": "zigzag"},
    {"coords": [(2, 0), (1, 1), (2, 2)], "type": "zigzag"},
]  # winning lines in a 2d matrix for 3X3 config

pay_table = {
    "♥": {3: 2, 4: 4},
    "♠": {3: 2, 4: 4},
    "Δ": {3: 5, 4: 10},
    "Ω": {3: 5, 4: 10},
    "Ψ": {3: 5, 4: 10},
    "♝": {3: 15, 4: 30},
    "♞": {3: 15, 4: 30},
    "♜": {3: 50, 4: 100},
    "♛": {3: 50, 4: 100},
    "♚": {3: 100, 4: 200},
}

line_bonus = {"horizontal": 1.0, "diagonal": 1.5, "zigzag": 2.0}


class Slot:
    """Represents a machine in the game. Tracking size, winning lines, and start and end states of the slot(used for animation)."""

    def __init__(self, select: str):

        self.slot_size = self.config(select)  # Initialize slot size based on input
        self.lines = LINES_3x3 if len(self.slot_size[0]) == 3 else LINES_3x4
        # Used to determine wins
        self.reels = {i: Reel(self.slot_size).reel_config for i in range(len(self.slot_size[0]))}
        # Sets up the slot symbols in a particular configuration for that session
        self.initial_slot_state = [[random.choice(SYMBOL) for _ in range(len(self.slot_size[0]))] for _ in range(len(self.slot_size))]
        # Sets up the initial stat used for animation

    @staticmethod
    def config(select) -> list[list[None]]:  # Takes user input and determines the slot size

        valid_selection = {"a": 3, "b": 4}  # Number of columns

        while True:
            if select in valid_selection:
                return [[None for _ in range(int(valid_selection[select]))] for _ in range(3)]

            else:
                select = (
                    input("Invalid selection. Please select 'a' for 3x3 or 'b' for 3x4: ").strip().lower()
                )  # Slot config input loop is handled here

    def spin(self):

        spun_slot = copy.deepcopy(self.slot_size)  # creates a copy to prevent editing of the original reels
        for row in range(len(self.slot_size)):  # Per row
            for col in range(len(self.slot_size[0])):  # Per column
                symbol = random.choice(self.reels[col])  # randomization logic
                spun_slot[row][col] = symbol  # Place it in the right spot

        return spun_slot


class Reel:
    """Represents a the reels of the slot machine. Track how many of each symbol are in each reel."""

    def __init__(self, slot_size: list):  # Uses the machine size to determine the reel length

        self.slot_size = slot_size
        self.reel_config = self.configure_reel()

    def configure_reel(self) -> list:

        if len(self.slot_size[0]) == 4:  # Uses the correct list to calculate the symbols and their re occurrence
            return list(SYMBOL_WEIGHTS_3x4.keys()) + random.choices(list(SYMBOL_WEIGHTS_3x4.keys()), list(SYMBOL_WEIGHTS_3x4.values()), k=60)

        else:
            return list(SYMBOL_WEIGHTS_3x3.keys()) + random.choices(list(SYMBOL_WEIGHTS_3x3.keys()), list(SYMBOL_WEIGHTS_3x3.values()), k=25)


def check_wins(result, lines) -> list[tuple]:
    """Checks each winning set of coordinates and determines if the same symbol is in them"""
    winning_lines = []

    for line in lines:
        coords = line["coords"]
        symbols = [result[row][col] for row, col in coords]
        if all(symbol == symbols[0] for symbol in symbols):
            winning_lines.append({"coords": coords, "symbol": symbols[0], "match_count": len(symbols), "line_type": line["type"]})

    return winning_lines


def calculate_payout(winning_lines, pay_table, line_bonus, bet=10) -> float:
    """Calculates the winnings by pay table and bonuses"""

    total = 0

    for line in winning_lines:
        base = pay_table.get(line["symbol"], {}).get(line["match_count"], 0)
        bonus = line_bonus.get(line["line_type"], 1.0)
        payout = base * bonus * bet
        total += payout

    return total

def spinning(result, winning_lines, initial_slot_state):
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

        print_board(initial_slot_state, [])
        time.sleep(0.065)

    console.print(f"Bank ${player.bank:.2f}")
    print_board(result, winning_lines)

def print_board(board, winning_lines=[]):
    console.clear()
    display_board = copy.deepcopy(board)
    for line in winning_lines:
        for x, y in line["coords"]:
            display_board[x][y] = f"[bold purple blink]{board[x][y]}[/bold purple blink]"
    for row in display_board:
        console.print(" | ".join(row))
    if winning_lines:
        console.print(f"[bold green]Winner![/bold green]")
        
          # Newline after each row

    else:
        console.clear()
        print(f"Bank ${player.bank}")
        console.print("\n".join([" | ".join(row) for row in board]))

def simulate_wins(reels, lines, spins=1000000):
    wins = 0
    won_line_symbol_counts = Counter()
    for _ in range(spins):
        # Generate a random spin
        result = [[random.choice(reels[col]) for col in range(len(reels))] for _ in range(len(lines[0]))]

        winning_lines, winning_symbol_line = check_wins(result, lines)

        if winning_lines:
            wins += 1
            won_line_symbol_counts.update(winning_symbol_line)
    for (line_num, symbol), count in won_line_symbol_counts.items():
        print(f"Line {line_num}, Symbol {symbol}: {count} wins")
    print(f"Total wins: {wins} out of {spins} spins")

    return wins,spins

if __name__ == "__main__":
    machine0 = Slot(input("Select 'a' for 3x3 or 'b' for 3x4: ") or 'a')
    player = User(input("Enter your name: ")[:10] or "Player1", float(input("Enter your initial deposit: ") or 100), float(input("How much would you like to bet?: ")or 10))
    console.print(f"Welcome {player.name}, you have ${player.bank:.2f} in the bank.")


    first_spin = True
    while True:

        if player.bank < player.bet:
            console.print(f"[bold red]You don't have enough money to continue. Game over![/bold red]")
            player.bet = float(input("How much money would you like to add?: "))


        prompt = "Please press 'y' to spin, 'b' to change bet 'n' to quit: " if first_spin else "Press 'Enter' to spin again,'b' to change bet or 'n' to quit: "

        start = input(prompt).strip().lower()

        while first_spin and start not in ('y', 'n'):

            console.clear()

            console.print(f"[bold blink]{prompt}[/bold blink]")

            start = input("").strip().lower()

        if start == 'y' or (not first_spin and start == ''):
            result = machine0.spin()

            winning_lines = check_wins(result, machine0.lines)
            player.bank -= player.bet # subtract bet
            # Animate first
            spinning(result, winning_lines, machine0.initial_slot_state)

            # Then calculate and apply payout
            payout = calculate_payout(winning_lines, pay_table, line_bonus)

            player.bank += payout  # add win

            first_spin = False

        elif start == 'b':
            player.bet = input("how much money would you like to add?: ")

        elif start == 'n':
            console.clear()
            print(f"Thank you for playing!")
            break