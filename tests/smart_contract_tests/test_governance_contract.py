import unittest
from src.smart_contracts.governance.governance_contract import GovernanceContract

class TestGovernanceContract(unittest.TestCase):
    def setUp(self):
        """Set up a new governance contract instance for testing."""
        self.governance_contract = GovernanceContract()
        self.governance_contract.create_proposal("Increase block size", "Proposal to increase the block size to 2MB.")

    def test_proposal_creation(self):
        """Test that a proposal can be created successfully."""
        proposals = self.governance_contract.get_proposals()
        self.assertEqual(len(proposals), 1)
        self.assertEqual(proposals[0]['title'], "Increase block size")
        self.assertEqual(proposals[0]['description'], "Proposal to increase the block size to 2MB.")
        self.assertEqual(proposals[0]['votes_for'], 0)
        self.assertEqual(proposals[0]['votes_against'], 0)

    def test_vote_on_proposal(self):
        """Test that a user can vote on a proposal."""
        self.governance_contract.vote("Alice", 0, True)  # Vote for the first proposal
        proposal = self.governance_contract.get_proposals()[0]
        self.assertEqual(proposal['votes_for'], 1)
        self.assertEqual(proposal['votes_against'], 0)

    def test_vote_against_proposal(self):
        """Test that a user can vote against a proposal."""
        self.governance_contract.vote("Bob", 0, False)  # Vote against the first proposal
        proposal = self.governance_contract.get_proposals()[0]
        self.assertEqual(proposal['votes_for'], 1)
        self.assertEqual(proposal['votes_against'], 1)

    def test_vote_invalid_proposal(self):
        """Test that voting on a non-existent proposal raises an error."""
        with self.assertRaises(ValueError):
            self.governance_contract.vote("Alice", 999, True)  # Attempt to vote on a non-existent proposal

    def test_double_vote(self):
        """Test that a user cannot vote more than once on the same proposal."""
        self.governance_contract.vote("Alice", 0, True)  # First vote
        with self.assertRaises(ValueError):
            self.governance_contract.vote("Alice", 0, False)  # Attempt to vote again

    def test_get_proposal_results(self):
        """Test that the results of a proposal can be retrieved correctly."""
        self.governance_contract.vote("Alice", 0, True)
        self.governance_contract.vote("Bob", 0, False)
        results = self.governance_contract.get_proposal_results(0)
        self.assertEqual(results['votes_for'], 1)
        self.assertEqual(results['votes_against'], 1)

if __name__ == "__main__":
    unittest.main()
