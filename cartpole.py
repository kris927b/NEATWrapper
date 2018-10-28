# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================

# Custom libraries
from NEATWrapper import Simulation


def main():
    env = 'CartPole-v1'
    sim = Simulation(env, 100)

    print("================ Starting simulation ================")
    sim.run(10)
    print("================= Ended  simulation =================")

if __name__ == '__main__':
    main()
