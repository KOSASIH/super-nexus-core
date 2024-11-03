// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Wallet {
    address[] public owners;
    mapping(address => bool) public isOwner;
    uint public requiredSignatures;

    struct Transaction {
        address to;
        uint amount;
        bool executed;
        uint confirmations;
        mapping(address => bool) isConfirmed;
    }

    Transaction[] public transactions;

    event Deposit(address indexed sender, uint amount);
    event TransactionCreated(uint indexed transactionId, address indexed to, uint amount);
    event TransactionExecuted(uint indexed transactionId);
    event Confirmation(uint indexed transactionId, address indexed owner);

    modifier onlyOwner() {
        require(isOwner[msg.sender], "Not an owner");
        _;
    }

    constructor(address[] memory _owners, uint _requiredSignatures) {
        require(_owners.length > 0, "Owners required");
        require(_requiredSignatures > 0 && _requiredSignatures <= _owners.length, "Invalid number of required signatures");

        for (uint i = 0; i < _owners.length; i++) {
            isOwner[_owners[i]] = true;
        }
        owners = _owners;
        requiredSignatures = _requiredSignatures;
    }

    receive() external payable {
        emit Deposit(msg.sender, msg.value);
    }

    function createTransaction(address _to, uint _amount) public onlyOwner {
        uint transactionId = transactions.length;
        transactions.push();
        Transaction storage t = transactions[transactionId];
        t.to = _to;
        t.amount = _amount;
        t.executed = false;
        t.confirmations = 0;

        emit TransactionCreated(transactionId, _to, _amount);
    }

    function confirmTransaction(uint _transactionId) public onlyOwner {
        Transaction storage t = transactions[_transactionId];
        require(!t.isConfirmed[msg.sender], "Transaction already confirmed");
        require(!t.executed, "Transaction already executed");

        t.isConfirmed[msg.sender] = true;
        t.confirmations += 1;

        emit Confirmation(_transactionId, msg.sender);

        if (t.confirmations >= requiredSignatures) {
            executeTransaction(_transactionId);
        }
    }

    function executeTransaction(uint _transactionId) internal {
        Transaction storage t = transactions[_transactionId];
        require(t.confirmations >= requiredSignatures, "Not enough confirmations");
        require(!t.executed, "Transaction already executed");

        t.executed = true;
        payable(t.to).transfer(t.amount);

        emit TransactionExecuted(_transactionId);
    }

    function getTransactionCount() public view returns (uint) {
        return transactions.length;
    }

    function getTransaction(uint _transactionId) public view returns (address, uint, bool, uint) {
        Transaction storage t = transactions[_transactionId];
        return (t.to, t.amount, t.executed, t.confirmations);
    }
}
