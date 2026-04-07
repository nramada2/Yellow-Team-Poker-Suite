"""
**************************************************************************

holdem.py is for:

the poker game type with community cards and river cards.

**************************************************************************
"""

from .base import PokerGame

class TexasHoldem(PokerGame):
    def deal_initial_cards(self):
        """Deal 2 hole cards face down to every player"""
        for p in self.players:
            hole_card = self.deck.draw(2)
            p.hand.add_cards(hole_card)

    def deal_community_cards(self, count: int):
        """Draws cards from the deck, flips them, and adds to the public pool"""
        new_cards = self.deck.draw(count)
        for card in new_cards:
            card.is_face_up = True  # Publicly visible
        self.community_cards.extend(new_cards)


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
        self.deal_community_cards(3) #the flop
        self.user_choice()
        self.is_betting_round_over()
        self.deal_community_cards(1) #the turn
        self.user_choice()
        self.is_betting_round_over()
        self.deal_community_cards(1) #the river
        self.user_choice()
        self.is_betting_round_over()
        self.determine_winner()

    def play_round(self):
        """Phase 1: Setup"""
        self.start_new_round()
        self.small_blind()
        self.large_blind()
        self.deal_initial_cards()
        
        """Phase 2: First round of betting pre-flop"""
        # The GUI will call user_choice() until is_betting_round_over() is True
        self.user_choice()
        self.is_betting_round_over()
        self.deal_community_cards(3)
        
        """Phase 3: Second round of betting post-flop"""
        self.user_choice()
        self.is_betting_round_over()
        self.deal_community_cards(1)

        """Phase 4: Third round of betting post-turn"""
        self.user_choice()
        self.is_betting_round_over()
        self.deal_community_cards(1)

        """Phase 5: Fourth round of betting post-river"""
        self.user_choice()
        self.is_betting_round_over()

        """Phase 6: Final Showdown"""
        self.determine_winner()