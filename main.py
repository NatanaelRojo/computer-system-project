import gym
import time
import gym_environments
from non_deterministic_montecarlo import NonDeterministicMonteCarlo
from agent_dq import DoubleQLearning


gym.register("TreasureTrail-v1", "battery_maze_env:RobotMazeEnv")


def train(env, agent, episodes):
    for _ in range(episodes):
        observation, _ = env.reset()
        terminated, truncated = False, False
        while not (terminated or truncated):
            action = agent.get_action(observation)
            new_observation, reward, terminated, truncated, _ = env.step(
                action)
            agent.update(observation, action, reward, terminated)
            observation = new_observation


def play(env, agent):
    observation, _ = env.reset()
    terminated, truncated = False, False
    while not (terminated or truncated):
        action = agent.get_best_action(observation)
        observation, _, terminated, truncated, _ = env.step(action)
        env.render()
        time.sleep(1)


if __name__ == "__main__":
    env = gym.make("TreasureTrail-v1")
    agent = NonDeterministicMonteCarlo(
        env.observation_space.n, env.action_space.n, gamma=0.9, epsilon=0.9
    )

    train(env, agent, episodes=400000)
    agent.render()
    env.init_render_mode("human")
    play(env, agent)

    env.close()
