import kaggle_environments


env = kaggle_environments.make(
    "rps", configuration={"episodeSteps": 100}, debug=True)
outcomes = env.run(['kumoko/agent.py', 'kumoko/agent.py'])

