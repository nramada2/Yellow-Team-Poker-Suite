"""
**************************************************************************
stud.py is for:

the poker game type WITHOUT card drawing mechanics

**************************************************************************
"""


from .base import PokerGame

class Stud(PokerGame):

    """
    *****************************************************************
    Custom dealing options for 7 card stud
    *****************************************************************
    """
     
    def deal_initial_cards(self):
        """Deal 2 hole cards face down to every player"""
        for p in self.players:
            hole_card = self.deck.draw(2)
            p.hand.add_cards(hole_card)

            """Deal 1 door card face up to every player"""
            door_card = self.deck.draw(1)
            door_card.is_face_up = True  #Make it visible to all
            p.hand.add_cards([door_card])


    def deal_subsequent_street(self, is_final_street=False):
        """4-6th street cards are up. 7th is down."""
        for player in self.players:
            if not player.is_folded:
                new_card = self.deck.draw(1)[0]
                
                if not is_final_street:
                    new_card.is_face_up = True
                
                player.hand.add_cards([new_card])

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
        self.deal_subsequent_street()
        self.determine_winner()

    def play_round(self):
        """Phase 1: Setup"""
        self.start_new_round()
        self.small_blind()
        self.large_blind()
        self.deal_initial_cards()
        
        """Phase 2: Betting (Wait for GUI input)"""
        # The GUI will call user_choice() until is_betting_round_over() is True
        self.user_choice()
        self.is_betting_round_over()
        
        """Phase 3: 4th Street - repeat 3x """
        self.deal_subsequent_street() 
        self.user_choice()
        self.is_betting_round_over

        """Phase 7: Final Showdown"""
        self.determine_winner()