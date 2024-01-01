from typing import List, Tuple
from z3 import Solver, Ints, Int, sat


def main(particles: List[Tuple[int, int, int, int, int, int]]):
    # Define the solver
    s = Solver()

    # Variables for the 6th particle's position and velocity
    x6, y6, z6 = Ints("x6 y6 z6")
    vx6, vy6, vz6 = Ints("vx6 vy6 vz6")

    # Time variables for each collision
    ts = [Int(f"t{i}") for i in range(5)]

    # Adding constraints for each collision
    for i, (x, y, z, vx, vy, vz) in enumerate(particles):
        s.add(x6 + vx6 * ts[i] == x + vx * ts[i])
        s.add(y6 + vy6 * ts[i] == y + vy * ts[i])
        s.add(z6 + vz6 * ts[i] == z + vz * ts[i])

    # Check if the problem is solvable
    if s.check() == sat:
        m = s.model()
        solution = m[x6], m[y6], m[z6], m[vx6], m[vy6], m[vz6], [m[t] for t in ts]
    else:
        solution = "No solution found"

    print(solution)
    print(solution[0] + solution[1] + solution[2])


if __name__ == "__main__":
    # Given particles' positions and velocities
    TEST_DATA = open("test_data.csv", "r", encoding="utf-8").read().splitlines()
    particles = []
    for line in TEST_DATA:
        position, velocity = line.split(" @ ")
        x, y, z = [int(i) for i in position.split(", ")]
        vx, vy, vz = [int(i) for i in velocity.split(", ")]
        particles.append((x, y, z, vx, vy, vz))
    main(particles)

    DATA = open("data.csv", "r", encoding="utf-8").read().splitlines()
    particles = []
    for line in DATA:
        position, velocity = line.split(" @ ")
        x, y, z = [int(i) for i in position.split(", ")]
        vx, vy, vz = [int(i) for i in velocity.split(", ")]
        particles.append((x, y, z, vx, vy, vz))
    main(particles[:5])
