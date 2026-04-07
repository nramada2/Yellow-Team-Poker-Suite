"""
**************************************************************************
base.py is for:

the poker game functinality.
This actually drives the game.

**************************************************************************
"""

from abc import ABC, abstractmethod
from core.cards import Deck
from core.players import Player

class PokerGame(ABC):
    def __init__(self, players: list[Player]):
        self.players = players
        self.deck = Deck()
        self.pot = 0
        self.current_bet = 0
        self.active_player_index = 0    # Tracks whose turn it is
        self.actions_this_round = 0     # Tracks total moves for the round
        self.community_cards = []
        


    """
    *****************************************************************
    Start a new round of play
    *****************************************************************
    """

    def start_new_round(self):
        """Standard setup for any poker game."""
        self.deck.reset()
        self.deck.shuffle()
        self.pot = 0
        self.actions_this_round = 0
        self.community_cards = []
        for player in self.players:
            player.reset_round_state()

    
    @abstractmethod
    def deal_cards(self):
        """Each variant deals a different number of cards."""
        pass

    @abstractmethod
    def deal_community_cards(self):
        """These deal face up cards"""
        pass

    @abstractmethod
    def play_round(self):
        """The main logic loop for the specific variant."""
        pass


    """
    *****************************************************************
    Force the blinds to play in
    *****************************************************************
    """

    @abstractmethod
    def small_blind(self, amount: int = 10):
        """Force small blind into play"""
        self.handle_bet(self.players[0], amount)

    @abstractmethod
    def large_blind(self, amount: int = 20):
        """Force large blind into play"""
        self.handle_bet(self.players[1], amount)


    """
    *****************************************************************
    Players have 4 options when it's their turn
    *****************************************************************
    """


    def check(self):
        """User passes. Only valid if current_bet matches player's contribution."""
        player = self.players[self.active_player_index]
        if player.current_bet == self.current_bet:
            self.actions_this_round += 1
            self.next_player()
            return True
        return False # Invalid move

    def call(self):
        """User matches the current highest bet."""
        player = self.players[self.active_player_index]
        amount_to_call = self.current_bet - player.current_bet
        self.handle_bet(player, amount_to_call)
        self.actions_this_round += 1
        self.next_player()

    def raised(self, raise_amount: int):    #raise is a reserved word, if you were wondering
        """User increases the current bet by raise_amount."""
        player = self.players[self.active_player_index]
        # Total to take from player = (amount to call) + (the extra raise)
        total_to_remove = (self.current_bet - player.current_bet) + raise_amount
        self.handle_bet(player, total_to_remove)
        self.actions_this_round += 1
        self.next_player()

    def fold(self):
        """User gives up their hand."""
        player = self.players[self.active_player_index]
        player.is_folded = True
        self.actions_this_round += 1
        active_players = [p for p in self.players if not p.is_folded]
        if len(active_players) == 1:
            determine_winner()
        self.next_player()

    def user_choice(self, action: str, amount: int = 0):
        """
        Routes the user's physical input to the correct engine logic.
        'action' would come from a button click (e.g., "fold", "call").
        """
        if action == "check":
            return self.check()
        elif action == "call":
            return self.call()
        elif action == "raise":
            return self.raised(amount)
        elif action == "fold":
            return self.fold()
        else:
            print(f"Invalid action: {action}")
            return False

    """
    *****************************************************************
    Handling a money/chips
    *****************************************************************
    """

    def handle_bet(self, player: Player, amount: int):
        """
        The core betting logic. 
        Updates the player's chips and the game's pot.
        """
        # If player bets more than the current_bet, it's a 'Raise'
        total_contribution = player.current_bet + amount
        
        if total_contribution > self.current_bet:
            self.current_bet = total_contribution
            self.last_raiser = player

        actual_chips_removed = player.remove_chips(amount)
        self.pot += actual_chips_removed

    def collect_blinds(self, small_blind_amt: int, big_blind_amt: int):
        """
        Uses the handle_bet logic to take blinds.
        Small blind is usually players[0], Big is players[1].
        """
        self.handle_bet(self.players[0], small_blind_amt)
        self.handle_bet(self.players[1], big_blind_amt)


    """
    *****************************************************************
    Ending a round
    *****************************************************************
    """

    def is_betting_round_over(self):
        active_players = [p for p in self.players if not p.is_folded]
        # Round is over if only one person is left OR everyone has acted and matched
        if len(active_players) <= 1:
            return True
        return all(p.current_bet == self.current_bet for p in active_players) and self.actions_this_round >= len(active_players)

    def next_player(self):
        """Moves the turn to the next non-folded player."""
        active_players = [p for p in self.players if not p.is_folded]
        if len(active_players) <= 1:
            return # No one else to move to

        self.active_player_index = (self.active_player_index + 1) % len(self.players)
        if self.players[self.active_player_index].is_folded:
            self.next_player()
    
    @abstractmethod
    def determine_winner(self):
        """Uses core.scoring.py to find the best hand."""
        pass

    def get_state(self):
        """Returns a dictionary, masking hidden information."""
        return {
            "pot": self.pot,
            "community": [str(c) if c.is_face_up else "HIDDEN" for c in self.community_cards],
            "players": [
                {
                    "name": p.name,
                    "chips": p.chips,
                    # Only show the cards if they are face up (or if it's the 'Showdown')
                    "hand": [str(c) if c.is_face_up else "HIDDEN" for c in p.hand.cards]
                } for p in self.players
            ],
            "turn": self.players[self.active_player_index].name
        }