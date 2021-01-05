import eval7
import random



class CalcDeck(eval7.Deck):
	def __init__(self):
		eval7.Deck.__init__(self)

	def remove(self, card):
		'''
		Removes the given card from the deck.  Card must be present in the deck
		card - type eval7.Card
		'''
		assert card in self.cards, "Card not found in the deck"
		self.cards.remove(card)


def calc_equity(hole, community, iters):
	'''
	Monte Carlo simulation to provide the win probability for a hand of poker given
	the current game state

	hole - list of exactly 2 strings representing the cards in the hole
		each string formatted <rank><suit>, e.g. 'As', 'Td', '9c', '3h'
	community - same as hole, except the list may be of length at most 5
	iters - the number of rounds to use in the monte carlo simulation
	'''
	assert 0 <= len(community) <= 5, "Incorrect number of community cards, must have at most 5"
	assert len(hole) == 2, "Incorrect number of hand cards, must have 2"

	hole_cards = []
	community_cards = [] #convert hole and community inputs to eval7.Card datatype

	for card in hole:
		hole_cards.append(eval7.Card(card))
	for card in community:
		community_cards.append(eval7.Card(card))

	deck = CalcDeck()

	for card in hole_cards: #remove known cards from deck
		deck.remove(card)
	for card in community_cards:
		deck.remove(card)

	win_count = 0 #init showdown win counter

	for _ in range(iters):
		deck.shuffle()

		num_remaining = 5 - len(community) #deal remainder of community cards
		draw = deck.peek(num_remaining + 2)
		
		opp_hole = draw[:2]
		remaining_comm = draw[2:]
		
		player_hand = hole_cards + community_cards + remaining_comm #compile player and opponent hands
		opp_hand = opp_hole + community_cards + remaining_comm

		player_strength = eval7.evaluate(player_hand) #calculate player and opponent strength
		opp_strength = eval7.evaluate(opp_hand)

		if player_strength > opp_strength: #find winner
			win_count += 1
		

	win_prob = win_count / iters
	return win_prob


	


if __name__ == '__main__':
	random.seed(1)
	hole = ['2c', '5d']
	community = []
	print('\nHole: {}, Board: {}, Strength: {}\n'.format(str(hole), str(community), calc_equity(hole, community, 1000)))
	


