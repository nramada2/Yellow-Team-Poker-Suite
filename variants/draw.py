"""
**************************************************************************
draw.py is for:

the poker game type WITH card draw mechanics

**************************************************************************
"""

from .base import PokerGame

class Draw(PokerGame):

    """
    *****************************************************************
    Custom dealing options for 7 card stud
    *****************************************************************
    """
     
    def deal_initial_cards(self):
        """Deal 5 hole cards face down to every player"""
        for p in self.players:
            hole_card = self.deck.draw(5)
            p.hand.add_cards(hole_card)

    def discard_and_draw(self, player: Player, indices: list[int]):
        """
        Takes the indices of cards selected from the GUI.
        Removes those cards and deals fresh ones.
        """
        if len(indices) > 3:
            return False # Security check: Don't allow more than 3
            
        # Remove the cards (High to Low index)
        for index in sorted(indices, reverse=True):
            player.hand.cards.pop(index)
            
        # Draw the exact same number of new cards
        new_cards = self.deck.draw(len(indices))
        player.hand.add_cards(new_cards)
        
        return True


    """
    *****************************************************************
    Running the game.
    Im leaving both options for now until states are implemented.
    Im unsure which version will be more appreciated.
    *****************************************************************
    """

    def play_round(self):
        self.start_new_round()
        self.deal_initial_cards()
        self.small_blind()
        self.large_blind()
        self.user_choice()
        self.is_betting_round_over()
        self.discard_and_draw()
        self.user_choice()
        self.is_betting_round_over()
        self.determine_winner()

    def play_round(self):
        """Phase 1: Setup"""
        self.start_new_round()
        self.small_blind()
        self.large_blind()
        self.deal_initial_cards()
        
        """Phase 2: First round of betting (Wait for GUI input)"""
        # The GUI will call user_choice() until is_betting_round_over() is True
        self.user_choice()
        self.is_betting_round_over()
        
        """Phase 3: Draw phase"""
        self.discard_and_draw() 

        """Phase 4: Second round of betting"""
        self.user_choice() 
        self.is_betting_round_over

        """Phase 5: Final Showdown"""
        self.determine_winner()