import React, { useState, useEffect } from 'react';
import Web3 from 'web3';
import MarketplaceContract from '../contracts/Marketplace.json';

const Marketplace = () => {
    const [account, setAccount] = useState('');
    const [items, setItems] = useState([]);
    const [itemName, setItemName] = useState('');
    const [itemPrice, setItemPrice] = useState(0);
    const [contract, setContract] = useState(null);
    const web3 = new Web3(Web3.givenProvider || 'http://localhost:7545');

    useEffect(() => {
        const loadBlockchainData = async () => {
            const accounts = await web3.eth.getAccounts();
            setAccount(accounts[0]);
            const networkId = await web3.eth.net.getId();
            const deployedNetwork = MarketplaceContract.networks[networkId];
            const instance = new web3.eth.Contract(
                MarketplaceContract.abi,
                deployedNetwork && deployedNetwork.address,
            );
            setContract(instance);
            await loadItems(instance);
        };
        loadBlockchainData();
    }, []);

    const loadItems = async (instance) => {
        const itemCount = await instance.methods.itemCount().call();
        const itemsArray = [];
        for (let i = 1; i <= itemCount; i++) {
            const item = await instance.methods.items(i).call();
            itemsArray.push(item);
        }
        setItems(itemsArray);
    };

    const createItem = async () => {
        if (!itemName || itemPrice <= 0) {
            alert("Please enter valid item name and price.");
            return;
        }
        await contract.methods.createItem(itemName, web3.utils.toWei(itemPrice.toString(), 'ether')).send({ from: account });
        setItemName('');
        setItemPrice(0);
        await loadItems(contract); // Reload items after creating a new one
    };

    const purchaseItem = async (itemId) => {
        const item = await contract.methods.items(itemId).call();
        if (item.sold) {
            alert("Item already sold!");
            return;
        }
        await contract.methods.purchaseItem(itemId).send({ from: account, value: item.price });
        await loadItems(contract); // Reload items after purchase
    };

    return (
        <div>
            <h1>Decentralized Marketplace</h1>
            <h2>Your Account: {account}</h2>

            <h3>Create Item for Sale</h3>
            <input
                type="text"
                value={itemName}
                onChange={(e) => setItemName(e.target.value)}
                placeholder="Item Name"
            />
            <input
                type="number"
                value={itemPrice}
                onChange={(e) => setItemPrice(e.target.value)}
                placeholder="Item Price in ETH"
            />
            <button onClick={createItem}>Create Item</button>

            <h3>Available Items</h3>
            <ul>
                {items.map((item, index) => (
                    <li key={index}>
                        <p>Name: {item.name}</p>
                        <p>Price: {web3.utils.fromWei(item.price, 'ether')} ETH</p>
                        <p>Sold: {item.sold ? 'Yes' : 'No'}</p>
                        {!item.sold && (
                            <button onClick={() => purchaseItem(item.id)}>Purchase</button>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Marketplace;
