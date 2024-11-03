import unittest
from src.smart_contracts.governance.governance_contract import GovernanceContract

class TestGovernanceContract(unittest.TestCase):
    def setUp(self):
        self.governance_contract = GovernanceContract()
        self.governance_contract.create_proposal("Increase block size", "Proposal to increase the block size to 2MB.")

    def test_proposal_creation(self):
        proposals = self.governance_contract.get_proposals()
        self.assertEqual(len(proposals), 1)
        self.assertEqual(proposals[0]['title'], "Increase block size")

    def test_vote_on_proposal(self):
        self.governance_contract.vote("Alice", 0, True)  # Vote for the first proposal
        proposal = self.governance_contract.get_proposals()[0]
        self.assertEqual(proposal['votes_for'], 1)

    def test_vote_invalid_proposal(self):
        with self.assertRaises(ValueError):
            self.governance_contract.vote("Alice", 999,
