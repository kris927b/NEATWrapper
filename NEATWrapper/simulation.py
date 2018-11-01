# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================

# Third-party libraries
import gym

# Custom libraries
from NEATWrapper.population import Population

class Simulation:
    """
    Class for doing a simulation using the NEAT Algorithm
    @param env: string, gym environment name
    @param pop_size: int, size of the population
    @param verbosity: int, the level of verbosity [1, 2]. 1 is the lowest level and 2 is the highest level. Optional, defaults to 1
    """
    def __init__(self, env, pop_size, verbosity=1):
        self.env = gym.make(env)
        self._maxSteps = self.env._max_episode_steps
        self.pop = Population(pop_size, self.env.observation_space.shape[0], self.env.action_space.n)
        self.verbosity = verbosity
        self.currGen = 1

    def run(self, generations, render=False):
        """
        Function for running X number of generations of the simulation. 
        """
        for _ in range(generations):
            steps = []
            for i in range(self.pop.size()):
                obs = self.env.reset()
                gene = self.pop.getGene(i)
                for step in range(self._maxSteps):
                    # self.env.render()
                    action = gene.getAction(obs)
                    obs, _, done, _ = self.env.step(action)
                    if done:
                        if self.verbosity == 2:
                            print(f'Gene {i}) no. steps {step+1}')
                        gene.steps = step + 1
                        steps.append(gene.steps)
                        break
            self.pop.naturalSelection()
            print(f'Generation Best: Steps: {max(steps)}')
            print(f'Finished generation {self.currGen}')
            self.currGen += 1

    def runBest(self):
        obs = self.env.reset()
        gene = self.pop.getBestGene()
        for step in range(500):
            self.env.render()
            action = gene.getAction(obs)
            obs, reward, done, _ = self.env.step(action)
            sys.stdout.write('\r' + str(reward + step))
            sys.stdout.flush()
            if done:
                break
        print("\nThe best gene got {} in reward!!".format(reward + step))
        # self.pop.showBest()