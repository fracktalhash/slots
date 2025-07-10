import random
from collections import Counter
from slots import Reel, check_wins, LINES_3x3, LINES_3x4


def simulate_wins(reels, lines, spins=100_000):
    wins = 0
    won_symbol_counts = Counter()

    for _ in range(spins):
        # Generate a random spin result
        result = [[random.choice(reels[col]) for col in range(len(reels))] for _ in range(len(lines[0]["coords"]))]

        winning_lines = check_wins(result, lines)

        if winning_lines:
            wins += 1
            for line in winning_lines:
                won_symbol_counts[line["symbol"]] += 1

    for symbol, count in won_symbol_counts.items():
        print(f"Symbol {symbol}: {count} wins")

    print(f"Total wins: {wins} out of {spins} spins")
    print(f"Win rate: {wins / spins * 100:.2f}%")

    return wins, spins


if __name__ == "__main__":
    # Test 3x3 slot config
    print("Simulating 3x3 slot:")
    test_slot_size_3x3 = [[None] * 3 for _ in range(3)]
    reel_config_3x3 = [Reel(test_slot_size_3x3).reel_config for _ in range(3)]
    simulate_wins(reel_config_3x3, LINES_3x3)

    print("\nSimulating 3x4 slot:")
    # Test 3x4 slot config
    test_slot_size_3x4 = [[None] * 4 for _ in range(3)]
    reel_config_3x4 = [Reel(test_slot_size_3x4).reel_config for _ in range(4)]
    simulate_wins(reel_config_3x4, LINES_3x4)
