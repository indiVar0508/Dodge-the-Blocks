# Dodge-the-Blocks

Dodge-the-Blocks is an experimental project, i created to learn reinforcement learning algorithms on customizable environment, as beginner(holds true for today also) i was curious how the behaviour of agent will change if number of states available to it change and how does agent learning pattern agent in a markov decision algorithm in Q-Learning algorithm 

<br />

<p align='center'>
  <img src="https://github.com/indiVar0508/Dodge-the-Blocks/blob/master/docs/three_state_agent.gif" height=300 width=350>
  <img src="https://github.com/indiVar0508/Dodge-the-Blocks/blob/master/docs/twenty_five_state_agent.gif" height=300 width=350>
</p>

The game support users also to play themselves but it becomes very hard unless you make some bot or something to score past 15 i think!
The current setup for agent has only two types of state defined for it 
  1. <i><b>three-state-system</b></i> : In this state detection approach, state of agent is decided depending on relative posistion of safe position wrt to agent's current position and accordingly a state is assigned to the agent 
    <ol>
    <li> `0` (Safe block is left to current position of agent) </li>
    <li> `1` (Safe block is just above the current position of agent) </li>
    <li> `2` (Safe block is right to current position of agent) </li>
    </ol>
    Depending upon what position the agent is wrt to agent should figure out what should be the best action for it to take(move left, right or stay)
  2. <i><b>twenty-five-state-system</b></i> : This approach is more detailed and has about 25 state to create search space for learning for agent, the states in this approach are defined wrt abosulte 5 positions that agent can take and 5 possible safe blocks(resulting in 5*5 = 25 states). game/environment is always aware of the position of safe block but agent is not, agent is only aware of the state and has learn/adapt to make decisions to increase the score for each episodes 
# Setup

If you want to give it a try you can clone the project 

```
      git clone https://github.com/indiVar0508/Dodge-the-Blocks.git
```

Install the requirements into your Python virtual environment, make sure you are in `Dodge-the-Blocks` directory

```
    python3 -m venv venv # create virtual environment
    source venv/bin/activate # activate virtual environment in terminal
    pip install -r requirements.txt
```

## how to run?
you can check CLI option to run from Terminal to run game in various mode (play yourself vs let the RL agent play) use the command `python dodge_the_blocks/main.py -h` to check options available
```
    Run Game as per User's preference

    optional arguments:
      -h, --help            show this help message and exit
      -use_agent use_agent  specify state for agent to play in 3 state vs 25 state
```
To run game for yourself use run the command `python dodge_the_blocks/main.py`, if you want to let agent learn and play the game use <i>optional</i> argument `-use_agent` which only expects 3 or 25 as valid states for agent
