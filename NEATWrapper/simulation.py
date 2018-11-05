# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================

# Built-in libraries
import sys

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

    def run(self, generations, render=False, graph=True):
        """
        Function for running X number of generations of the simulation. 
        """
        for _ in range(generations):
            steps = []
            for i in range(self.pop.size()):
                obs = self.env.reset()
                gene = self.pop.getGene(i)
                r = 0
                for _ in range(self._maxSteps):
                    if render:
                        self.env.render()
                    action = gene.getAction(obs)
                    obs, reward, done, _ = self.env.step(action)
                    r += reward
                    sys.stdout.write(f'\rGene {i+1}) no. steps {r} ')
                    sys.stdout.flush()
                    if done:
                        if self.verbosity == 2:
                            print(f'Gene {i+1}) reward {r}')
                        gene.steps = r
                        steps.append(r)
                        r = 0
                        break
            print(f'\nGeneration Max Reward: {max(steps)}')
            print(f'Generation Min Reward: {min(steps)}')
            if graph:
                self.pop.getGene(steps.index(max(steps))).drawGenome()
            self.pop.naturalSelection()
            print(f'=============== Finished generation {self.currGen} ===============')
            self.currGen += 1

    def runBest(self):
        obs = self.env.reset()
        gene = self.pop.getBestGene()
        score = self.pop.getBestScore()
        r = 0
        for _ in range(self._maxSteps):
            self.env.render()
            action = gene.getAction(obs)
            obs, reward, done, _ = self.env.step(action)
            r += reward
            sys.stdout.write(f'\rBest Gene) no. steps {r} ')
            sys.stdout.flush()
            if done:
                break
        print(f"\nThe best gene got {r} in reward!!")
        print("=====================================================")
        if r < score:
            self.pop.clearBest()
        gene.drawGenome()
