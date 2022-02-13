CARD_RANKS_ORIGINAL = '23456789TJQKA'
SUITS_ORIGINAL = 'CDHS'


def to_string(cards):
    return [str(cd).upper() for cd in cards]


def get_winner(player_hands, table_cards):
    """Determine the winning hands of multiple players"""
    player_cards_with_table_cards = []
    for player_hand in player_hands:
        player_cards_with_table_cards.append(to_string(player_hand) + to_string(table_cards))

    return eval_best_hands(player_cards_with_table_cards)


def eval_best_hands(hands):
    scores = [(i, _calc_score(hand)) for i, hand in enumerate(hands)]
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return [score[0] for score in scores if score[1] == scores[0][1]]


def _calc_score(hand):
    """Assign a calc_score to the hand so it can be compared with other hands"""
    rcounts = {CARD_RANKS_ORIGINAL.find(r): ''.join(hand).count(r) for r, _ in hand}.items()
    score, card_ranks = zip(*sorted((cnt, rank) for rank, cnt in rcounts)[::-1])

    potential_threeofakind = score[0] == 3
    potential_twopair = score == (2, 2, 1, 1, 1)
    potential_pair = score == (2, 1, 1, 1, 1, 1)

    if score[0:2] == (3, 2) or score[0:2] == (3, 3):  # fullhouse (three of a kind and pair, or two three of a kind)
        card_ranks = (card_ranks[0], card_ranks[1])
        score = (3, 2)
    elif score[0:4] == (2, 2, 2, 1):  # special case: convert three pair to two pair
        score = (2, 2, 1)  # as three pair are not worth more than two pair
        kicker = max(card_ranks[2], card_ranks[3])  # avoid for example 11,8,6,7
        card_ranks = (card_ranks[0], card_ranks[1], kicker)
    elif score[0] == 4:  # four of a kind
        score = (4,)
        sorted_card_ranks = sorted(card_ranks, reverse=True)  # avoid for example 11,8,9
        card_ranks = (sorted_card_ranks[0], sorted_card_ranks[1])
    elif len(score) >= 5:  # high card, flush, straight and straight flush
        # straight
        if 12 in card_ranks:  # adjust if 5 high straight
            card_ranks += (-1,)
        sorted_card_ranks = sorted(card_ranks, reverse=True)  # sort again as if pairs the first rank matches the pair
        for i in range(len(sorted_card_ranks) - 4):
            straight = sorted_card_ranks[i] - sorted_card_ranks[i + 4] == 4
            if straight:
                card_ranks = (
                    sorted_card_ranks[i], sorted_card_ranks[i + 1], sorted_card_ranks[i + 2], sorted_card_ranks[i + 3],
                    sorted_card_ranks[i + 4])
                break

        # flush
        suits = [s for _, s in hand]
        flush = max(suits.count(s) for s in suits) >= 5
        if flush:
            for flush_suit in SUITS_ORIGINAL:  # get the suit of the flush
                if suits.count(flush_suit) >= 5:
                    break

            flush_hand = [k for k in hand if flush_suit in k]  # pylint: disable=undefined-loop-variable
            rcounts_flush = {CARD_RANKS_ORIGINAL.find(r): ''.join(flush_hand).count(r) for r, _ in flush_hand}.items()
            score, card_ranks = zip(*sorted((cnt, rank) for rank, cnt in rcounts_flush)[::-1])
            card_ranks = tuple(
                sorted(card_ranks, reverse=True))  # ignore original sorting where pairs had influence

            # check for straight in flush
            if 12 in card_ranks and -1 not in card_ranks:  # adjust if 5 high straight
                card_ranks += (-1,)
            for i in range(len(card_ranks) - 4):
                straight = card_ranks[i] - card_ranks[i + 4] == 4
                if straight:
                    break

        # no pair, straight, flush, or straight flush
        score = ([(1,), (3, 1, 2)], [(3, 1, 3), (5,)])[flush][straight]

    if score == (1,) and potential_threeofakind:
        score = (3, 1)
    elif score == (1,) and potential_twopair:
        score = (2, 2, 1)
    elif score == (1,) and potential_pair:
        score = (2, 1, 1)

    if score[0] == 5:
        hand_type = "StraightFlush"  # crdRanks=crdRanks[:5] # five card rule makes no difference {:5] would be incorrect
    elif score[0] == 4:
        hand_type = "FoufOfAKind"  # crdRanks=crdRanks[:2] # already implemented above
    elif score[0:2] == (3, 2):
        hand_type = "FullHouse"  # crdRanks=crdRanks[:2] # already implmeneted above
    elif score[0:3] == (3, 1, 3):
        hand_type = "Flush"
        card_ranks = card_ranks[:5]
    elif score[0:3] == (3, 1, 2):
        hand_type = "Straight"
        card_ranks = card_ranks[:5]
    elif score[0:2] == (3, 1):
        hand_type = "ThreeOfAKind"
        card_ranks = card_ranks[:3]
    elif score[0:2] == (2, 2):
        hand_type = "TwoPair"
        card_ranks = card_ranks[:3]
    elif score[0] == 2:
        hand_type = "Pair"
        card_ranks = card_ranks[:4]
    elif score[0] == 1:
        hand_type = "HighCard"
        card_ranks = card_ranks[:5]
    else:
        raise Exception('Card Type error!')

    return score, card_ranks, hand_type


if __name__ == '__main__':
    def test_evaluator1():
        """Hand evaluator test"""
        cards = [['3H', '3S', '4H', '4S', '8S', '8C', 'QH'],
                 ['KH', '6C', '4H', '4S', '8S', '8C', 'QH']]
        expected = [1]
        winner = eval_best_hands(cards)
        assert winner == expected


    def test_evaluator2():
        """Hand evaluator test"""
        cards = [['8H', '8D', 'QH', '7H', '9H', 'JH', 'TH'],
                 ['KH', '6C', 'QH', '7H', '9H', 'JH', 'TH']]
        expected = [1]
        winner = eval_best_hands(cards)
        assert winner == expected


    def test_evaluator3():
        """Hand evaluator test"""
        cards = [['AS', 'KS', 'TS', '9S', '7S', '2H', '2H'],
                 ['AS', 'KS', 'TS', '9S', '8S', '2H', '2H']]
        expected = [1]
        winner = eval_best_hands(cards)
        assert winner == expected


    def test_evaluator4():
        """Hand evaluator test"""
        cards = [['8S', 'TS', '8H', 'KS', '9S', 'TH', 'KH'],
                 ['TD', '7S', '8H', 'KS', '9S', 'TH', 'KH']]
        expected = [0, 1]
        winner = eval_best_hands(cards)
        assert winner == expected


    def test_evaluator5():
        """Hand evaluator test"""
        cards = [['2D', '2H', 'AS', 'AD', 'AH', '8S', '7H'],
                 ['7C', '7S', '7H', 'AD', 'AS', '8S', '8H']]
        expected = [0]
        winner = eval_best_hands(cards)
        assert winner == expected


    def test_evaluator6():
        """Hand evaluator test"""
        cards = [['7C', '7S', '7H', 'AD', 'KS', '5S', '8H'],
                 ['2D', '3H', 'AS', '4D', '5H', '8S', '7H']]
        expected = [1]
        winner = eval_best_hands(cards)
        assert winner == expected


    def test_evaluator6b():
        """Hand evaluator test"""
        cards = [['7C', '7C', 'AC', 'AC', '8C', '8S', '7H'],
                 ['2C', '3C', '4C', '5C', '6C', '8S', 'KH']]
        expected = [1]
        winner = eval_best_hands(cards)
        assert winner == expected


    def test_evaluator7():
        """Hand evaluator test"""
        cards = [['AC', 'JS', 'AS', '2D', '5H', '3S', '3H'],
                 ['QD', 'JD', 'TS', '9D', '6H', '8S', 'KH'],
                 ['2D', '3D', '4S', '5D', '6H', '8S', 'KH']]
        expected = [1]
        winner = eval_best_hands(cards)
        assert winner == expected


    def test_evaluator8():
        """Hand evaluator test"""
        cards = [['7C', '5S', '3S', 'JD', '8H', '2S', 'KH'],
                 ['AD', '3D', '4S', '5D', '9H', '8S', 'KH']]
        expected = [1]
        winner = eval_best_hands(cards)
        assert winner == expected


    def test_evaluator9():
        """Hand evaluator test"""
        cards = [['2C', '2D', '4S', '4D', '4H', '8S', 'KH'],
                 ['7C', '7S', '7D', '7H', '8H', '8S', 'JH']]
        expected = [1]
        winner = eval_best_hands(cards)
        assert winner == expected


    def test_evaluator10():
        """Hand evaluator test"""
        cards = [['7C', '5S', '3S', 'JD', '8H', '2S', 'KH'],
                 ['AD', '3D', '3S', '5D', '9H', '8S', 'KH']]
        expected = [1]
        winner = eval_best_hands(cards)
        assert winner == expected


    def test_evaluator11():
        """Hand evaluator test"""
        cards = [['7H', '7S', '3S', 'JD', '8H', '2S', 'KH'],
                 ['7D', '3D', '3S', '7C', '9H', '8S', 'KH']]
        expected = [1]
        winner = eval_best_hands(cards)
        assert winner == expected


    def test_evaluator12():
        """Hand evaluator test"""
        cards = [['AS', '8H', 'TS', 'JH', '3H', '2H', 'AH'],
                 ['QD', 'QH', 'TS', 'JH', '3H', '2H', 'AH']]
        expected = [1]
        winner = eval_best_hands(cards)
        assert winner == expected


    def test_evaluator13():
        """Hand evaluator test"""
        cards = [['9S', '7H', 'KS', 'KH', 'AH', 'AS', 'AC'],
                 ['8D', '2H', 'KS', 'KH', 'AH', 'AS', 'AC']]
        expected = [0, 1]
        winner = eval_best_hands(cards)
        assert winner == expected


    test_evaluator1()
    test_evaluator2()
    test_evaluator3()
    test_evaluator4()
    test_evaluator5()
    test_evaluator6()
    test_evaluator6b()
    test_evaluator7()
    test_evaluator8()
    test_evaluator9()
    test_evaluator10()
    test_evaluator11()
    test_evaluator12()
    test_evaluator13()
