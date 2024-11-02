// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./GovernanceToken.sol";

contract Voting {
    GovernanceToken public governanceToken;

    struct Proposal {
        string description;
        uint256 voteCount;
        mapping(address => bool) voters;
        bool executed;
    }

    Proposal[] public proposals;

    event ProposalCreated(uint256 proposalId, string description);
    event Voted(uint256 proposalId, address voter);
    event ProposalExecuted(uint256 proposalId);

    constructor(GovernanceToken _governanceToken) {
        governanceToken = _governanceToken;
    }

    function createProposal(string memory description) public {
        proposals.push(Proposal({
            description: description,
            voteCount: 0,
            executed: false
        }));
        emit ProposalCreated(proposals.length - 1, description);
    }

    function vote(uint256 proposalId) public {
        require(proposalId < proposals.length, "Proposal does not exist");
        require(!proposals[proposalId].voters[msg.sender], "You have already voted");

        uint256 voterBalance = governanceToken.balanceOf(msg.sender);
        require(voterBalance > 0, "You must own governance tokens to vote");

        proposals[proposalId].voteCount += voterBalance;
        proposals[proposalId].voters[msg.sender] = true;
        emit Voted(proposalId, msg.sender);
    }

    function executeProposal(uint256 proposalId) public {
        require(proposalId < proposals.length, "Proposal does not exist");
        require(!proposals[proposalId].executed, "Proposal already executed");

        // Here you can add logic to execute the proposal based on the vote count
        proposals[proposalId].executed = true;
        emit ProposalExecuted(proposalId);
    }

    function getProposalCount() public view returns (uint256) {
        return proposals.length;
    }

    function getProposal(uint256 proposalId) public view returns (string memory description, uint256 voteCount, bool executed) {
        require(proposalId < proposals.length, "Proposal does not exist");
        Proposal storage proposal = proposals[proposalId];
        return (proposal.description, proposal.voteCount, proposal.executed);
    }
}
