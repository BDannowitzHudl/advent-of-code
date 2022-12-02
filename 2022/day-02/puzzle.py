from enum import Enum


class Outcome(Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6


class Hand(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @property
    def beats(self):
        return {
            Hand.ROCK: Hand.SCISSORS,
            Hand.PAPER: Hand.ROCK,
            Hand.SCISSORS: Hand.PAPER
        }[self]
    
    @property
    def loses_to(self):
        return {
            Hand.ROCK: Hand.PAPER,
            Hand.PAPER: Hand.SCISSORS,
            Hand.SCISSORS: Hand.ROCK,
        }[self]
    
    @property
    def ties_with(self):
        return self

    def get_hand(self, outcome):
        # Return the hand that would result in the given outcome
        return {
            Outcome.LOSE: self.beats,
            Outcome.DRAW: self.ties_with,
            Outcome.WIN: self.loses_to
        }[outcome]


HAND_MAP = {
    "A": Hand.ROCK,
    "B": Hand.PAPER,
    "C": Hand.SCISSORS,
    "X": Hand.ROCK,
    "Y": Hand.PAPER,
    "Z": Hand.SCISSORS,
}

OUTCOME_MAP = {
    "X": Outcome.LOSE,
    "Y": Outcome.DRAW,
    "Z": Outcome.WIN,
}

class Round:
    
    def __init__(self, hand_1: str, hand_2: str):
        self.hand_1 = HAND_MAP[hand_1]
        self.hand_2 = HAND_MAP[hand_2]
        
    def evaluate(self):
        # Draw
        if self.hand_1 == self.hand_2:
            return Outcome.DRAW.value + self.hand_2.value
        # Lose
        elif self.hand_1.beats == self.hand_2:
            return Outcome.LOSE.value + self.hand_2.value
        # Win
        elif self.hand_1.loses_to == self.hand_2:
            return Outcome.WIN.value + self.hand_2.value 

    def __repr__(self):
        return f"Play({self.hand_1} vs. {self.hand_2}), Score: {self.evaluate()}"

        
class RoundRedux(Round):
    
    def __init__(self, hand: str, outcome: str):
        self.hand_1 = HAND_MAP[hand]
        self.outcome = OUTCOME_MAP[outcome]
        self.hand_2 = self.hand_1.get_hand(self.outcome)
        

def main(data_csv: str) -> None:
    with open(data_csv, "r") as f:
        data = f.read().splitlines()
    
    score_1: int = 0
    score_2: int = 0
    for row in data:
        r = Round(*row.split(" "))
        rr = RoundRedux(*row.split(" "))
        score_1 += r.evaluate() 
        score_2 += rr.evaluate() 
    print(f"Original Scoring: {score_1}")
    print(f"New Scoring: {score_2}")
    return None


if __name__ == "__main__":
    main("puzzle_data.csv")