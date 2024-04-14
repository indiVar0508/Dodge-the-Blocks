import argparse

my_parser = argparse.ArgumentParser(description='Run Game as per User\'s preference')

my_parser.add_argument(
    '--use_agent',
    metavar='use_agent',
    type=int,
    help='specify state for agent to play in 3 state vs 25 state',
    default=None 
)

args = my_parser.parse_args()

if args.use_agent is None:
    from game.main import Game
    Game().startGame()
else:
    from agents_game.main import AgentGame
    game = AgentGame(agent_state=args.use_agent)
    for episode in range(50):
        game.startGame(episode)
        game.reset()

