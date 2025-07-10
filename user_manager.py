import db_manager


class User:
    """Represents a player in the game. Tracking bank, bets, and spin history.
    Players will be deleted 1 week after creation,
    in the final web based game."""

    def __init__(self, name: str, bank: float, bet: float, spin_count: int = 0):
        """Object constructors. Spin count gets initialized to zero as when the player object is first built it has zero spins."""
        self.name = name  # Is used for save and sync account records in the db
        self.bank = bank  # keeps track of the accounts bank value
        self.bet = bet  # Current bet and is used for the payout math
        self.spin_count = spin_count  # Cumulative spin count across sessions
        # Self.creation_time = creation_time ## delete user after 1 week

    def save(self) -> None:
        """makes the players stats persists across sessions while the profile exists"""
        db_manager.account_updater(self.name, self.bank, self.spin_count)  # updates the database
