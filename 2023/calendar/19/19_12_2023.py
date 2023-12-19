"""
--- Day 19: Aplenty ---
The Elves of Gear Island are thankful for your help and send you on your way. They even
have a hang glider that someone stole from Desert Island; since you're already going
that direction, it would help them a lot if you would use it to get down there and
return it to them.

As you reach the bottom of the relentless avalanche of machine parts, you discover
that they're already forming a formidable heap. Don't worry, though - a group of Elves
is already here organizing the parts, and they have a system.

To start, each part is rated in each of four categories:

x: Extremely cool looking
m: Musical (it makes a noise when you hit it)
a: Aerodynamic
s: Shiny
Then, each part is sent through a series of workflows that will ultimately accept or
reject the part. Each workflow has a name and contains a list of rules; each rule
specifies a condition and where to send the part if the condition is true. The first
rule that matches the part being considered is applied immediately, and the part moves
on to the destination described by the rule. (The last rule in each workflow has no
condition and always applies if reached.)

Consider the workflow ex{x>10:one,m<20:two,a>30:R,A}. This workflow is named ex and
contains four rules. If workflow ex were considering a specific part, it would perform
the following steps in order:

Rule "x>10:one": If the part's x is more than 10, send the part to the workflow named
one.
Rule "m<20:two": Otherwise, if the part's m is less than 20, send the part to the
workflow named two.
Rule "a>30:R": Otherwise, if the part's a is more than 30, the part is immediately
rejected (R).
Rule "A": Otherwise, because no other rules matched the part, the part is immediately
accepted (A).
If a part is sent to another workflow, it immediately switches to the start of that
workflow instead and never returns. If a part is accepted (sent to A) or rejected
(sent to R), the part immediately stops any further processing.

The system works, but it's not keeping up with the torrent of weird metal shapes.
The Elves ask if you can help sort a few parts and give you the list of workflows and
some part ratings (your puzzle input). For example:

px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
The workflows are listed first, followed by a blank line, then the ratings of the parts
the Elves would like you to sort. All parts begin in the workflow named in. In this
example, the five listed parts go through the following workflows:

{x=787,m=2655,a=1222,s=2876}: in -> qqz -> qs -> lnx -> A
{x=1679,m=44,a=2067,s=496}: in -> px -> rfg -> gd -> R
{x=2036,m=264,a=79,s=2244}: in -> qqz -> hdj -> pv -> A
{x=2461,m=1339,a=466,s=291}: in -> px -> qkq -> crn -> R
{x=2127,m=1623,a=2188,s=1013}: in -> px -> rfg -> A
Ultimately, three parts are accepted. Adding up the x, m, a, and s rating for each of
the accepted parts gives 7540 for the part with x=787, 4623 for the part with x=2036,
and 6951 for the part with x=2127. Adding all of the ratings for all of the accepted
parts gives the sum total of 19114.

Sort through all of the parts you've been given; what do you get if you add together
all of the rating numbers for all of the parts that ultimately get accepted?

--- Part Two ---
Even with your help, the sorting process still isn't fast enough.

One of the Elves comes up with a new plan: rather than sort parts individually
through all of these workflows, maybe you can figure out in advance which combinations
of ratings will be accepted or rejected.

Each of the four ratings (x, m, a, s) can have an integer value ranging from a minimum
of 1 to a maximum of 4000. Of all possible distinct combinations of ratings, your job
is to figure out which ones will be accepted.

In the above example, there are 167409079868000 distinct combinations of ratings that
will be accepted.

Consider only your list of workflows; the list of part ratings that the Elves wanted
you to sort is no longer relevant. How many distinct combinations of ratings will be
accepted by the Elves' workflows?

"""
from typing import List, Optional, Dict, Tuple
from pathlib import Path
from functools import reduce
from copy import deepcopy


class Range:
    def __init__(self, category: str, min_value: int, max_value: int):
        self.category = category
        self.min_value = min_value
        self.max_value = max_value

    def __len__(self):
        return self.max_value - self.min_value + 1

    @property
    def size(self):
        return len(self)


class CombinationRange:
    def __init__(self, ranges: List[Range]):
        self.ranges: Dict[str, Range] = {r.category: r for r in ranges}
        self.accepted = False

    @property
    def size(self):
        # The product of all the range sizes
        return reduce(lambda x, y: x * y, [self.ranges[r].size for r in self.ranges])

    def copy(self):
        return CombinationRange([deepcopy(r) for r in self.ranges.values()])


class Part:
    def __init__(self, data: str):
        self._data = data
        self.accepted = False
        self.x, self.m, self.a, self.s = self._parse_data()

    def _parse_data(self):
        data = self._data.replace("{", "").replace("}", "")
        x, m, a, s = data.split(",")
        x = int(x.split("=")[1])
        m = int(m.split("=")[1])
        a = int(a.split("=")[1])
        s = int(s.split("=")[1])
        return x, m, a, s

    @property
    def score(self):
        return self.x + self.m + self.a + self.s


class Operation:
    def __init__(self, category: str, operator: str, value: int):
        self.category = category
        self.operator = operator
        self.value = value

    def evaluate(self, part: Part) -> bool:
        if self.operator == ">":
            return getattr(part, self.category) > self.value
        elif self.operator == "<":
            return getattr(part, self.category) < self.value
        else:
            raise ValueError(f"Invalid operator: {self.operator}")

    def evaluate_range(
        self, combination_range: CombinationRange
    ) -> Tuple[CombinationRange, CombinationRange]:
        """Returns a tuple of the accepted combination range and
        the remainder combination range."""
        if self.operator == ">":
            category_range = combination_range.ranges[self.category]
            if self.value > category_range.max_value:
                # Whole range passes the condition
                return combination_range, None
            elif self.value < category_range.min_value:
                # Whole range fails the condition
                return None, combination_range
            else:
                # Split the range into two
                remainder_range = combination_range.copy()
                remainder_range.ranges[self.category].max_value = self.value
                combination_range.ranges[self.category].min_value = self.value + 1
                return combination_range, remainder_range
        elif self.operator == "<":
            category_range = combination_range.ranges[self.category]
            if self.value < category_range.min_value:
                # Whole range passes the condition
                return combination_range, None
            elif self.value > category_range.max_value:
                # Whole range fails the condition
                return None, combination_range
            else:
                # Split the range into two
                remainder_range = combination_range.copy()
                remainder_range.ranges[self.category].min_value = self.value
                combination_range.ranges[self.category].max_value = self.value - 1
                return combination_range, remainder_range
        else:
            raise ValueError(f"Invalid operator: {self.operator}")


class Rule:
    """m>1111:fq"""

    def __init__(self, data: str):
        self._data = data
        self._condition, self._destination = self._parse_data()
        self.operation: Operation = self._parse_condition()

    def _parse_data(self):
        condition, destination = self._data.split(":")
        return condition, destination

    def _parse_condition(self):
        self.category = self._condition[0]
        self.operator = self._condition[1]
        self.value = int(self._condition[2:])
        return Operation(self.category, self.operator, self.value)

    def evaluate(self, part: Part) -> Optional[str]:
        """Evaluate the rule against the part."""
        if self.operation.evaluate(part):
            return self._destination
        else:
            return None

    def evaluate_range(
        self, combination_range: CombinationRange
    ) -> Tuple[Optional[Tuple[str, CombinationRange]], Optional[CombinationRange]]:
        """Evaluates a combination range and returns a dict of the destination and the
        potentially split-up combination ranges."""
        destination_tuple: Optional[Tuple[str, CombinationRange]] = None
        pass_range, fail_range = self.operation.evaluate_range(combination_range)
        if pass_range:
            destination_tuple = (self._destination, pass_range)
        return destination_tuple, fail_range


class Ruleset:
    def __init__(self, data: str):
        self._data = data
        self.name, self.rules, self.final = self._parse_data()

    def _parse_data(self):
        """rfg{s<537:gd,x>2440:R,A}
        rfg is the name
        s<536:gd is the first rule
        x>2440:R is the second rule
        A is the final destination
        """
        name, rest = self._data.split("{")
        rest = rest.replace("}", "")
        rules_str = rest.split(",")[:-1]
        rules = [Rule(r) for r in rules_str]
        final = rest.split(",")[-1]
        return name, rules, final

    def evaluate(self, part: Part) -> Optional[str]:
        """Evaluate the ruleset against the part."""
        for rule in self.rules:
            if destination := rule.evaluate(part):
                return destination
        return self.final

    def evaluate_range(
        self, combination_range: CombinationRange
    ) -> Dict[str, CombinationRange]:
        """Evaluates a combination range and returns a dict of the destination and the
        potentially split-up combination ranges."""
        destination_list: List[Tuple[str, CombinationRange]] = []
        remainder_range = combination_range.copy()
        for rule in self.rules:
            rule_destination_tuple, remainder_range = rule.evaluate_range(
                remainder_range
            )
            if rule_destination_tuple:
                destination_list.append(rule_destination_tuple)
        if remainder_range:
            destination_list.append((self.final, remainder_range))
        return destination_list


class RulesetCollection:
    def __init__(self, rulesets: List[Ruleset]):
        self.rulesets: Dict[str, Ruleset] = {r.name: r for r in rulesets}
        self.first_ruleset = self.rulesets["in"]

    def process(self, part: Part):
        """Process the part through the rulesets."""
        current_ruleset = self.first_ruleset
        while True:
            if destination := current_ruleset.evaluate(part):
                if destination == "A":
                    part.accepted = True
                    break
                elif destination == "R":
                    break
                else:
                    current_ruleset = self.rulesets[destination]
            else:
                break


def get_combinations(
    combination_range: CombinationRange,
    ruleset_collection: RulesetCollection,
    entrypoint: str,
) -> int:
    """Get the number of combinations that will be accepted."""
    combinations = 0
    current_ruleset = ruleset_collection.rulesets[entrypoint]
    destination_list = current_ruleset.evaluate_range(combination_range)
    for destination_tuple in destination_list:
        destination = destination_tuple[0]
        destination_range = destination_tuple[1]
        if destination == "A":
            combinations += destination_range.size
        elif destination == "R":
            pass
        else:
            combinations += get_combinations(
                destination_range, ruleset_collection, destination
            )
    return combinations


def part_one(data: List[str]) -> int:
    rulesets: List[Ruleset] = []
    for ix, line in enumerate(data):
        if line == "":
            break
        rulesets.append(Ruleset(line))

    parts: List[Part] = []
    for line in data[ix + 1 :]:
        parts.append(Part(line))

    ruleset_collection = RulesetCollection(rulesets)
    for part in parts:
        ruleset_collection.process(part)

    score = sum([part.score for part in parts if part.accepted])

    return score


def part_two(data: List[str]) -> int:
    rulesets: List[Ruleset] = []
    for ix, line in enumerate(data):
        if line == "":
            break
        rulesets.append(Ruleset(line))
    ruleset_collection = RulesetCollection(rulesets)
    ranges = [
        Range("x", 1, 4000),
        Range("m", 1, 4000),
        Range("a", 1, 4000),
        Range("s", 1, 4000),
    ]
    cr = CombinationRange(ranges)
    combinations = get_combinations(
        combination_range=cr,
        ruleset_collection=ruleset_collection,
        entrypoint="in",
    )

    return combinations


if __name__ == "__main__":
    WORKING_DIR = Path(__file__).parent
    DATA = open(WORKING_DIR / "data.csv", encoding="utf-8").read().splitlines()

    TEST_DATA: List[str] = [
        "px{a<2006:qkq,m>2090:A,rfg}",
        "pv{a>1716:R,A}",
        "lnx{m>1548:A,A}",
        "rfg{s<537:gd,x>2440:R,A}",
        "qs{s>3448:A,lnx}",
        "qkq{x<1416:A,crn}",
        "crn{x>2662:A,R}",
        "in{s<1351:px,qqz}",
        "qqz{s>2770:qs,m<1801:hdj,R}",
        "gd{a>3333:R,R}",
        "hdj{m>838:A,pv}",
        "",
        "{x=787,m=2655,a=1222,s=2876}",
        "{x=1679,m=44,a=2067,s=496}",
        "{x=2036,m=264,a=79,s=2244}",
        "{x=2461,m=1339,a=466,s=291}",
        "{x=2127,m=1623,a=2188,s=1013}",
    ]

    # Starting Part One at 7:55AM CST

    PART_ONE_EXPECTED_VALUE: int = 19114
    print(f"Part One: {part_one(TEST_DATA)} (expected {PART_ONE_EXPECTED_VALUE})")
    print(f"Part One: {part_one(DATA)}")

    # Completed Part One at

    # Starting Part Two at

    PART_TWO_EXPECTED_VALUE: int = 167409079868000
    print(f"Part Two: {part_two(TEST_DATA)} (expected {PART_TWO_EXPECTED_VALUE})")
    print(f"Part Two: {part_two(DATA)}")

    # Completed Part Two at 9:59AM CST
