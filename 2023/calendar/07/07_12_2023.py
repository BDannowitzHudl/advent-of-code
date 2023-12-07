"""
--- Day 7: Camel Cards ---
Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship.
(At least it's a cool airship!) It drops you off at the edge of a vast desert and
descends back to Island Island.

"Did you bring the parts?"

You turn around to see an Elf completely covered in white clothing, wearing goggles,
and riding a large camel.

"Did you bring the parts?" she asks again, louder this time. You aren't sure what parts
she's looking for; you're here to figure out why the sand stopped.

"The parts! For the sand, yes! Come with me; I will show you." She beckons you onto
the camel.

After riding a bit across the sands of Desert Island, you can see what look like very
large rocks covering half of the horizon. The Elf explains that the rocks are all
along the part of Desert Island that is directly above Island Island, making it hard
to even get there. Normally, they use big machines to move the rocks and filter the
sand, but the machines have broken down because Desert Island recently stopped
receiving the parts they need to fix the machines.

You've already assumed it'll be your job to figure out why the parts stopped when she
asks if you can help. You agree automatically.

Because the journey will take a few days, she offers to teach you the game of Camel
Cards. Camel Cards is sort of similar to poker except it's designed to be easier to
play while riding a camel.

In Camel Cards, you get a list of hands, and your goal is to order them based on the
strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9,
8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where
A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different
label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a
different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are
each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and
the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different
label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456
Hands are primarily ordered based on type; for example, every full house is stronger
than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by
comparing the first card in each hand. If these cards are different, the hand with
the stronger first card is considered stronger. If the first card in each hand have
the same label, however, then move on to considering the second card in each hand.
If they differ, the hand with the higher second card wins; otherwise, continue with
the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its
first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888
is stronger because its third card is stronger (and both hands have the same first
and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your
puzzle input). For example:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
This example shows five hands; each hand is followed by its bid amount. Each hand
wins an amount equal to its bid multiplied by its rank, where the weakest hand gets
rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand.
Because there are five hands in this example, the strongest hand will have rank 5
and its bid will be multiplied by 5.

So, the first step is to put the hands in order of strength:

32T3K is the only one pair and the other hands are all a stronger type, so it gets
rank 1.
KK677 and KTJJT are both two pair. Their first cards both have the same label, but
the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets
rank 3.
T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets
rank 5 and T55J5 gets rank 4.
Now, you can determine the total winnings of this set of hands by adding up the result
of multiplying each hand's bid with its rank
(765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this
example are 6440.

Find the rank of every hand in your set. What are the total winnings?

--- Part Two ---
To make things a little more interesting, the Elf introduces one additional rule.
Now, J cards are jokers - wildcards that can act like whatever card would make the
hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2.
The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand
type; for example, QJJQ2 is now considered four of a kind. However, for the purpose
of breaking ties between two hands of the same type, J is always treated as J, not the
card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
32T3K is still the only one pair; it doesn't contain any jokers, so its strength
doesn't increase.
KK677 is now the only two pair, making it the second-weakest hand.
T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets
rank 4, and KTJJT gets rank 5.
With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new
total winnings?

"""
from typing import List, Dict, Set
from pathlib import Path
from itertools import combinations_with_replacement
from enum import Enum
import pandas as pd


card_dict: Dict[str, int] = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


class HandType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

    def __lt__(self, other: "HandType"):
        return self.value < other.value

    def __gt__(self, other: "HandType"):
        return self.value > other.value

    def __eq__(self, other: "HandType"):
        return self.value == other.value


class Hand:
    def __init__(self, cards_str: str, bet: int, part: int = 1) -> None:
        self.cards = pd.Series([c for c in cards_str])
        self.part = part
        self.card_values: List[int] = [card_dict[c] for c in cards_str]
        # In part 2, J's are worth 1 for evaluation in the case of tied hand types
        if self.part == 2:
            self.card_values = [card_dict[c] if c != "J" else 1 for c in cards_str]
        self.bet = bet
        self.hand_type: HandType = self._parse_hand_type()
        if self.part == 2:
            # Get the number of jokers
            joker_count = len([c for c in cards_str if c == "J"])
            # Remove the J's from the card string
            new_card_str = cards_str.replace("J", "")
            # Get all possible unique combinations of cards that the jokers can make
            joker_combos: List[str] = self._get_joker_combos(joker_count)
            # Try them all out and see which hand type is best
            best_hand_type: HandType = self.hand_type
            for combo in joker_combos:
                new_hand = Hand(new_card_str + combo, bet)
                if new_hand.hand_type > best_hand_type:
                    best_hand_type = new_hand.hand_type
            self.hand_type = best_hand_type

    def _get_joker_combos(self, joker_count: int) -> Set[str]:
        combos = [
            "".join(c)
            for c in combinations_with_replacement("AKQT98765432", joker_count)
        ]
        return combos

    def _parse_hand_type(self) -> HandType:
        counts = self.cards.value_counts()
        if counts.max() == 5:
            return HandType.FIVE_OF_A_KIND
        elif counts.max() == 4:
            return HandType.FOUR_OF_A_KIND
        elif counts.max() == 3:
            if counts.min() == 2:
                return HandType.FULL_HOUSE
            else:
                return HandType.THREE_OF_A_KIND
        elif counts.max() == 2:
            if counts.value_counts()[2] == 2:
                return HandType.TWO_PAIR
            else:
                return HandType.ONE_PAIR
        else:
            return HandType.HIGH_CARD

    def __lt__(self, other: "Hand"):
        if self.hand_type < other.hand_type:
            return True
        elif self.hand_type > other.hand_type:
            return False
        else:
            for i in range(5):
                if self.card_values[i] < other.card_values[i]:
                    return True
                elif self.card_values[i] > other.card_values[i]:
                    return False
        return False

    def __eq__(self, other: "Hand") -> bool:
        if self.card_values == other.card_values:
            return True
        return False

    def __gt__(self, other: "Hand"):
        if not self < other and not self == other:
            return True
        return False

    def __repr__(self) -> str:
        return f"{self.cards.values} {self.hand_type} {self.bet}"


def part_one(data: List[str]) -> int:
    hands: List[Hand] = []
    for line in data:
        cards, bet = line.split()
        hands.append(Hand(cards, int(bet)))
    hands.sort()
    score = sum([hand.bet * (i + 1) for i, hand in enumerate(hands)])
    return score


def part_two(data: List[str]) -> int:
    hands: List[Hand] = []
    for line in data:
        cards, bet = line.split()
        hands.append(Hand(cards, int(bet), part=2))
    hands.sort()
    score = sum([hand.bet * (i + 1) for i, hand in enumerate(hands)])
    return score


if __name__ == "__main__":
    WORKING_DIR = Path(__file__).parent
    DATA = open(WORKING_DIR / "data.csv", encoding="utf-8").read().splitlines()

    TEST_DATA: List[str] = [
        "32T3K 765",
        "T55J5 684",
        "KK677 28",
        "KTJJT 220",
        "QQQJA 483",
    ]

    # Starting Part One at 9:25AM CST

    PART_ONE_EXPECTED_VALUE = 6440
    print(f"Part One: {part_one(TEST_DATA)} (expected {PART_ONE_EXPECTED_VALUE})")
    print(f"Part One: {part_one(DATA)}")

    # Completed Part One at 10:34AM CST

    # Starting Part Two at 10:38AM CST

    PART_TWO_EXPECTED_VALUE = 5905
    print(f"Part Two: {part_two(TEST_DATA)} (expected {PART_TWO_EXPECTED_VALUE})")
    print(f"Part Two: {part_two(DATA)}")

    # Completed Part Two at 10:58AM CST
