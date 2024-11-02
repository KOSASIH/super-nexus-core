# src/blockchain/consensus/delegated_proof_of_stake.py

import random
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Voter:
    def __init__(self, address):
        self.address = address
        self.stake = 0
        self.delegate = None
        self.last_delegation_time = 0

    def delegate_stake(self, amount, delegate):
        if amount <= self.stake:
            if self.delegate and time.time() - self.last_delegation_time < 60:  # 1 minute cooldown
                logging.warning(f"{self.address} cannot change delegate yet. Please wait.")
                return
            
            self.stake -= amount
            delegate.add_vote(self.address, amount)
            self.delegate = delegate
            self.last_delegation_time = time.time()
            logging.info(f"{self.address} delegated {amount} to {delegate.address}.")
        else:
            logging.warning(f"{self.address} attempted to delegate more than their stake.")

    def un_delegate(self):
        if self.delegate:
            amount = self.delegate.get_votes(self.address)
            self.delegate.remove_vote(self.address, amount)
            self.stake += amount
            logging.info(f"{self.address} undelegated {amount} from {self.delegate.address}.")
            self.delegate = None
        else:
            logging.warning(f"{self.address} has no delegate to undelegate from.")

    def add_stake(self, amount):
        self.stake += amount
        logging.info(f"{self.address} added stake. Total stake: {self.stake}")

class Delegate:
    def __init__(self, address):
        self.address = address
        self.votes = 0
        self.voters = {}

    def add_vote(self, voter_address, amount):
        self.votes += amount
        self.voters[voter_address] = amount
        logging.info(f"{voter_address} voted for {self.address}. Total votes: {self.votes}")

    def remove_vote(self, voter_address, amount):
        if voter_address in self.voters:
            self.votes -= self.voters[voter_address]
            del self.voters[voter_address]
            logging.info(f"{voter_address} removed their vote from {self.address}. Total votes: {self.votes}")

    def get_votes(self, voter_address):
        return self.voters.get(voter_address, 0)

class DelegatedProofOfStake:
    def __init__(self, reward_rate=0.01, voter_reward_rate=0.005, max_delegates=5):
        self.voters = {}
        self.delegates = {}
        self.elected_delegates = []
        self.reward_rate = reward_rate
        self.voter_reward_rate = voter_reward_rate
        self.max_delegates = max_delegates

    def add_voter(self, address):
        if address not in self.voters:
            self.voters[address] = Voter(address)
            logging.info(f"Added new voter: {address}")

    def add_delegate(self, address):
        if address not in self.delegates:
            self.delegates[address] = Delegate(address)
            logging.info(f"Added new delegate: {address}")

    def delegate_stake(self, voter_address, amount, delegate_address):
        if voter_address in self.voters and delegate_address in self.delegates:
            self.voters[voter_address].delegate_stake(amount, self.delegates[delegate_address])
        else:
            logging.error("Invalid voter or delegate address.")

    def un_delegate(self, voter_address):
        if voter_address in self.voters:
            self.voters[voter_address].un_delegate()
        else:
            logging.error("Invalid voter address.")

    def elect_delegates(self):
        # Sort delegates by votes and select the top N
        sorted_delegates = sorted(self.delegates.values(), key=lambda d: d.votes, reverse=True)
        self.elected_delegates = sorted_delegates[:self.max_delegates]
        logging.info(f"Elected delegates: {[delegate.address for delegate in self.elected_delegates]}")

    def distribute_rewards(self):
        for delegate in self.elected_delegates:
            # Calculate rewards based on votes
            rewards = delegate.votes * self.reward_rate  # Example reward calculation
            logging.info(f"Distributing {rewards} rewards to delegate {delegate.address}")
            # Here you would implement the logic to actually distribute the rewards

        for voter in self.voters.values():
            if voter.delegate:
                # Calculate rewards for voters based on their stake
                voter_rewards = voter.stake * self.voter_reward_rate  # Example reward calculation
                logging.info(f"Distributing {voter_rewards} rewards to voter {voter.address}")

    def get_elected_delegates(self):
        return [delegate.address for delegate in self.elected_delegates]

    def get_delegate_votes(self, delegate_address):
        if delegate_address in self.delegates:
            return self.delegates[delegate_address].votes
        else:
            logging.error("Delegate not found.")
            return 0

    def get_voter_stake(self, voter_address):
        if voter_address in self.voters:
            return self.voters[voter_address].stake
        else:
            logging.error("Voter not found.")
            return 0

# Example usage
if __name__ == "__main__":
    dpos = DelegatedProofOfStake()
    
    # Adding voters and delegates
    dpos.add_voter("voter1")
    dpos.add_voter("voter2")
    dpos.add_delegate("delegate1")
    dpos.add_delegate("delegate2")

    # Voters adding stake
    dpos.voters["voter1"].add_stake(100)
    dpos.voters["voter2"].add_stake(200)

    # Delegating stakes
    dpos.delegate_stake("voter1", 50, "delegate1")
    dpos.delegate_stake("voter2", 150, "delegate2")

    # Electing delegates
    dpos.elect_delegates()

    # Distributing rewards
    dpos.distribute_rewards()

    # Un-delegating
    dpos.un_delegate("voter1")

    # Re-electing delegates after changes
    dpos.elect_delegates()

    # Displaying elected delegates
    print("Elected Delegates:", dpos.get_elected_delegates())
