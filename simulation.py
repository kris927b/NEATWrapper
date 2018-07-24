# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================

# Third-party libraries
import gym

# Custom libraries
from population import Population

class Simulation:
    """
    Class for doing a simulation using the NEAT Algorithm
    """
    def __init__(self, env, pop_size):
        self.env = gym.make(env)
        self.input = self.env.action_space.n
        self.output = self.env.observation_space.shape[0]
        self.pop = Population(pop_size, self.input, self.output)

    def run(self, generations):
        for g in range(generations):
            for i in range(self.pop.size()):
                obs = self.env.reset()
                gene = self.pop.getGene(i)
                for step in range(100):
                    self.env.render()
                    action = gene.getAction(obs)
                    obs, _, done, _ = self.env.step(action)
                    if done:
                        print("Gene {}) no. steps {}".format(i, step+1))
                        gene.steps = step + 1
                        break
            self.pop.naturalSelection()
            print("Finished generation {}".format(g+1))