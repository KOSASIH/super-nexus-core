// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./MintableToken.sol";

contract GovernanceToken is MintableToken {
    struct Proposal {
        address proposer;
        string description;
        uint256 voteCount;
        uint256 endTime;
        bool executed;
        mapping(address => bool) voted;
    }

    Proposal[] public proposals;
    uint256 public quorum; // Minimum votes required for a proposal to pass
    uint256 public votingPeriod; // Duration of the voting period in seconds

    event ProposalCreated(uint256 indexed proposalId, address indexed proposer, string description, uint256 endTime);
    event Voted(uint256 indexed proposalId, address indexed voter);
    event ProposalExecuted(uint256 indexed proposalId);

    constructor(
        string memory _name,
        string memory _symbol,
        uint8 _decimals,
        uint256 _initialSupply,
        uint256 _maxTransferAmount,
        uint256 _quorum,
        uint256 _votingPeriod
    ) MintableToken(_name, _symbol, _decimals, _initialSupply, _maxTransferAmount) {
        quorum = _quorum;
        votingPeriod = _votingPeriod;
    }

    function createProposal(string memory description) public returns (uint256) {
        uint256 proposalId = proposals.length;
        uint256 endTime = block.timestamp + votingPeriod;

        Proposal storage newProposal = proposals.push();
        newProposal.proposer = msg.sender;
        newProposal.description = description;
        newProposal.endTime = endTime;
        newProposal.executed = false;

        emit ProposalCreated(proposalId, msg.sender, description, endTime);
        return proposalId;
    }

    function vote(uint256 proposalId) public {
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp < proposal.endTime, "GovernanceToken: voting period has ended");
        require(!proposal.voted[msg.sender], "GovernanceToken: you have already voted");

        proposal.voted[msg.sender] = true;
        proposal.voteCount += balanceOf(msg.sender); // Count votes based on token balance

        emit Voted(proposalId, msg.sender);
    }

    function executeProposal(uint256 proposalId) public {
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp >= proposal.endTime, "GovernanceToken: voting period has not ended");
        require(!proposal.executed, "GovernanceToken: proposal has already been executed");

        if (proposal.voteCount >= quorum) {
            // Execute the proposal (this can be customized based on the proposal's purpose)
            // For example, it could call another contract or change a state variable.
            // Here we just mark it as executed.
            proposal.executed = true;
            emit ProposalExecuted(proposalId);
        }
    }

    function setQuorum(uint256 _quorum) public onlyOwner {
        quorum = _quorum;
    }

    function setVotingPeriod(uint256 _votingPeriod) public onlyOwner {
        votingPeriod = _votingPeriod;
    }
}
