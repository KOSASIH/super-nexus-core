const HDWalletProvider = require('@truffle/hdwallet-provider');
const Web3 = require('web3');
const WalletContract = require('./build/contracts/Wallet.json');
const { infuraKey, mnemonic } = require('./secrets.json'); // Store sensitive data in secrets.json

const provider = new HDWalletProvider(
    mnemonic,
    `https://rinkeby.infura.io/v3/${infuraKey}`
);

const web3 = new Web3(provider);

const deploy = async () => {
    const accounts = await web3.eth.getAccounts();
    console.log('Attempting to deploy from account', accounts[0]);

    const result = await new web3.eth.Contract(WalletContract.abi)
        .deploy({ data: WalletContract.evm.bytecode.object, arguments: [[accounts[0], accounts[1]], 2] }) // Example owners and required signatures
        .send({ gas: '1000000', from: accounts[0] });

    console.log('Contract deployed to', result.options.address);
    provider.engine.stop();
};

deploy();
