# src/blockchain/consensus/proof_of_stake.py

import random
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Stakeholder:
    def __init__(self, address):
        self.address = address
        self.stake = 0
        self.staking_time = 0

    def stake(self, amount):
        self.stake += amount
        self.staking_time = time.time()  # Record the time of staking
        logging.info(f"{self.address} staked {amount}. Total stake: {self.stake}")

    def unstake(self, amount):
        if amount <= self.stake:
            self.stake -= amount
            logging.info(f"{self.address} unstaked {amount}. Total stake: {self.stake}")
        else:
            logging.warning(f"{self.address} attempted to unstake more than their stake.")

    def calculate_rewards(self):
        # Simple reward calculation based on stake and time
        duration = time.time() - self.staking_time
        rewards = self.stake * (duration / 3600) * 0.01  # 1% reward per hour
        return rewards

class ProofOfStake:
    def __init__(self):
        self.stakers = {}

    def add_staker(self, address):
        if address not in self.stakers:
            self.stakers[address] = Stakeholder(address)
            logging.info(f"Added new staker: {address}")

    def stake(self, address, amount):
        if address in self.stakers:
            self.stakers[address].stake(amount)
        else:
            logging.error(f"Address {address} not found. Please add the address first.")

    def unstake(self, address, amount):
        if address in self.stakers:
            self.stakers[address].unstake(amount)
        else:
            logging.error(f"Address {address} not found. Please add the address first.")

    def get_winner(self):
        total_stake = sum(staker.stake for staker in self.stakers.values())
        if total_stake == 0:
            logging.warning("No stakes available to select a winner.")
            return None

        random_choice = random.uniform(0, total_stake)
        current_sum = 0

        for address, staker in self.stakers.items():
            current_sum += staker.stake
            if current_sum >= random_choice:
                logging.info(f"Winner selected: {address}")
                return address

        return None

    def distribute_rewards(self):
        for address, staker in self.stakers.items():
            rewards = staker.calculate_rewards()
            if rewards > 0:
                logging.info(f"Distributing {rewards} rewards to {address}")
                # Here you would implement the logic to actually distribute the rewards
                # For example, increase the balance of the staker's account
