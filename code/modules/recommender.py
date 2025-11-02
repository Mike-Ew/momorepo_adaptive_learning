import numpy as np


class MultiArmedBanditRecommender:
    """
    Simple implementation of a multi-armed bandit for content recommendation
    """

    def __init__(self, content_items, exploration_param=0.2):
        self.content_items = content_items  # List of content options
        self.exploration_param = exploration_param
        self.rewards = {item: 0 for item in content_items}
        self.attempts = {item: 0 for item in content_items}

    def get_recommendation(self, student_profile=None):
        """
        Get content recommendation for a student
        Using Upper Confidence Bound (UCB) algorithm
        """
        # If we have some items that haven't been tried yet, try them first
        untried = [item for item, count in self.attempts.items() if count == 0]
        if untried:
            return np.random.choice(untried)

        # Calculate UCB for each item
        total_attempts = sum(self.attempts.values())
        ucb_values = {}
        for item in self.content_items:
            average_reward = self.rewards[item] / self.attempts[item]
            exploration_bonus = self.exploration_param * np.sqrt(
                2 * np.log(total_attempts) / self.attempts[item]
            )
            ucb_values[item] = average_reward + exploration_bonus

        # Return the item with the highest UCB value
        return max(ucb_values, key=ucb_values.get)

    def update_reward(self, item, reward):
        """
        Update the reward for an item after a student interaction
        """
        self.rewards[item] += reward
        self.attempts[item] += 1
