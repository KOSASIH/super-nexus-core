const HDWalletProvider = require('@truffle/hdwallet-provider');
const Web3 = require('web3');
const MarketplaceContract = require('./build/contracts/Marketplace.json');
const { infuraKey, mnemonic } = require('./secrets.json'); // Store sensitive data in secrets.json

const provider = new HDWalletProvider(
    mnemonic,
    `https://rinkeby.infura.io/v3/${infuraKey}`
);

const web3 = new Web3(provider);

const deploy = async () => {
    const accounts = await web3.eth.getAccounts();
    console.log('Attempting to deploy from account', accounts[0]);

    const result = await new web3.eth.Contract(MarketplaceContract.abi)
        .deploy({ data: MarketplaceContract.evm.bytecode.object })
        .send({ gas: '1000000', from: accounts[0] });

    console.log('Contract deployed to', result.options.address);
    provider.engine.stop();
};

deploy();
