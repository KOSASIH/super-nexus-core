// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./ERC20Token.sol";

contract MintableToken is ERC20Token {
    event Mint(address indexed to, uint256 amount);

    constructor(
        string memory _name,
        string memory _symbol,
        uint8 _decimals,
        uint256 _initialSupply,
        uint256 _maxTransferAmount
    ) ERC20Token(_name, _symbol, _decimals, _initialSupply, _maxTransferAmount) {}

    /**
     * @dev Mints new tokens and assigns them to the specified address.
     * Can only be called by the owner.
     * @param to The address to which the minted tokens will be assigned.
     * @param amount The amount of tokens to mint.
     */
    function mint(address to, uint256 amount) public onlyOwner returns (bool) {
        require(to != address(0), "MintableToken: mint to the zero address");
        require(amount > 0, "MintableToken: amount must be greater than zero");

        totalSupply = totalSupply.add(amount);
        balances[to] = balances[to].add(amount);
        emit Transfer(address(0), to, amount);
        emit Mint(to, amount);
        return true;
    }
}
