# NEATWrapper

This repository contains a wrapper for the NEAT (Evolving Neural Networks through Augmenting Topologies) Algorithm. And a scenario of using it in the Gym environments from OpenAI

## Work in progress

This is a project that is still in progress. It is not fully working yet. In the cartpole example (cartpole.py) we really does not see any improvements to neither of the agents. This is main priority currently, besides creating good tests, to make sure we do not mess up the methods.

- [X] Create verbosity setting for simulation class
- [ ] Creating tests for all classes
  - [X] Creating tests for Node object
  - [X] Creating tests for Connection object
  - [X] Creating tests for Genome object
  - [X] Creating tests for Innovation object
  - [ ] Creating tests for Species object
  - [X] Creating tests for Population object
- [ ] Optimizing code base
- [X] Implementing crossover for two of the agents
  - [X] Implmenting method for selecting two parent genes for crossover
  - [X] Implement a method for searching similar connections in other parent.