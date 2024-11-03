import React, { useState, useEffect } from 'react';
import Web3 from 'web3';
import WalletContract from '../contracts/Wallet.json';

const Wallet = () => {
    const [account, setAccount] = useState('');
    const [owners, setOwners] = useState([]);
    const [requiredSignatures, setRequiredSignatures] = useState(0);
    const [transactions, setTransactions] = useState([]);
    const [toAddress, setToAddress] = useState('');
    const [amount, setAmount] = useState(0);
    const web3 = new Web3(Web3.givenProvider || 'http://localhost:7545');
    const contract = new web3.eth.Contract(WalletContract.abi, WalletContract.networks[5777].address);

    useEffect(() => {
        const loadAccount = async () => {
            const accounts = await web3.eth.getAccounts();
            setAccount(accounts[0]);
            loadWalletDetails();
        };
        loadAccount();
    }, []);

    const loadWalletDetails = async () => {
        const ownersList = await contract.methods.owners().call();
        const required = await contract.methods.requiredSignatures().call();
        const transactionCount = await contract.methods.getTransactionCount().call();
        
        setOwners(ownersList);
        setRequiredSignatures(required);
        
        const txs = [];
        for (let i = 0; i < transactionCount; i++) {
            const tx = await contract.methods.getTransaction(i).call();
            txs.push(tx);
        }
        setTransactions(txs);
    };

    const createTransaction = async () => {
        await contract.methods.createTransaction(toAddress, web3.utils.toWei(amount.toString(), 'ether')).send({ from: account });
        loadWalletDetails(); // Reload wallet details after creating a transaction
        setToAddress('');
        setAmount(0);
    };

    const confirmTransaction = async (transactionId) => {
        await contract.methods.confirmTransaction(transactionId).send({ from: account });
        loadWalletDetails(); // Reload wallet details after confirming a transaction
    };

    return (
        <div>
            <h1>Multi-Signature Wallet</h1>
            <h2>Account: {account}</h2>
            <h3>Owners:</h3>
            <ul>
                {owners.map((owner, index) => (
                    <li key={index}>{owner}</li>
                ))}
            </ul>
            <h3>Required Signatures: {requiredSignatures}</h3>

            <h2>Create Transaction</h2>
            <input
                type="text"
                value={toAddress}
                onChange={(e) => setToAddress(e.target.value)}
                placeholder="Recipient Address"
            />
            <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="Amount in ETH"
            />
            <button onClick={createTransaction}>Create Transaction</button>

            <h2>Pending Transactions</h2>
            <ul>
                {transactions.map((tx, index) => (
                    <li key={index}>
                        <p>To: {tx[0]}</p>
                        <p>Amount: {web3.utils.fromWei(tx[1], 'ether')} ETH</p>
                        <p>Executed: {tx[2] ? 'Yes' : 'No'}</p>
                        <p>Confirmations: {tx[3]}</p>
                        {!tx[2] && (
                            <button onClick={() => confirmTransaction(index)}>Confirm Transaction</button>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Wallet;
