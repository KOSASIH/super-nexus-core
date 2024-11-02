// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./SafeMath.sol";
import "./Ownable.sol";

contract ERC20Token is Ownable {
    using SafeMath for uint256;

    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;
    uint256 public maxTransferAmount; // Anti-whale mechanism

    mapping(address => uint256) private balances;
    mapping(address => mapping(address => uint256)) private allowances;
    mapping(address => bool) private isExcludedFromAntiWhale;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Burn(address indexed burner, uint256 value);
    event Paused();
    event Unpaused();

    bool public paused = false;

    modifier whenNotPaused() {
        require(!paused, "ERC20Token: token transfer while paused");
        _;
    }

    constructor(string memory _name, string memory _symbol, uint8 _decimals, uint256 _initialSupply, uint256 _maxTransferAmount) {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        totalSupply = _initialSupply * (10 ** uint256(decimals));
        maxTransferAmount = _maxTransferAmount * (10 ** uint256(decimals));
        balances[msg.sender] = totalSupply;
        emit Transfer(address(0), msg.sender, totalSupply);
    }

    function balanceOf(address account) public view returns (uint256) {
        return balances[account];
    }

    function transfer(address to, uint256 amount) public whenNotPaused returns (bool) {
        require(to != address(0), "ERC20Token: transfer to the zero address");
        require(balances[msg.sender] >= amount, "ERC20Token: transfer amount exceeds balance");
        require(isExcludedFromAntiWhale[msg.sender] || amount <= maxTransferAmount, "ERC20Token: transfer amount exceeds the maxTransferAmount");

        balances[msg.sender] = balances[msg.sender].sub(amount);
        balances[to] = balances[to].add(amount);
        emit Transfer(msg.sender, to, amount);
        return true;
    }

    function approve(address spender, uint256 amount) public whenNotPaused returns (bool) {
        allowances[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) public whenNotPaused returns (bool) {
        require(from != address(0), "ERC20Token: transfer from the zero address");
        require(to != address(0), "ERC20Token: transfer to the zero address");
        require(balances[from] >= amount, "ERC20Token: transfer amount exceeds balance");
        require(allowances[from][msg.sender] >= amount, "ERC20Token: transfer amount exceeds allowance");
        require(isExcludedFromAntiWhale[from] || amount <= maxTransferAmount, "ERC20Token: transfer amount exceeds the maxTransferAmount");

        balances[from] = balances[from].sub(amount);
        balances[to] = balances[to].add(amount);
        allowances[from][msg.sender] = allowances[from][msg.sender].sub(amount);
        emit Transfer(from, to, amount);
        return true;
    }

    function allowance(address owner, address spender) public view returns (uint256) {
        return allowances[owner][spender];
    }

    function burn(uint256 amount) public returns (bool) {
        require(balances[msg.sender] >= amount, "ERC20Token: burn amount exceeds balance");
        balances[msg.sender] = balances[msg.sender].sub(amount);
        totalSupply = totalSupply.sub(amount);
        emit Burn(msg.sender, amount);
        return true;
    }

    function mint(address to, uint256 amount) public onlyOwner returns (bool) {
        require(to != address(0), "ERC20Token: mint to the zero address");
        totalSupply = totalSupply.add(amount);
        balances[to] = balances[to].add(amount);
        emit Transfer(address(0), to, amount);
        return true;
    }

    function setMaxTransferAmount(uint256 _maxTransferAmount) public onlyOwner {
        maxTransferAmount = _maxTransferAmount * (10 ** uint256(decimals));
    }

    function excludeFromAntiWhale(address account) public onlyOwner {
        isExcludedFromAntiWhale[account] = true;
    }

    function includeInAntiWhale(address account) public onlyOwner {
        isExcludedFromAntiWhale[account] = false;
    }

    function pause() public onlyOwner {
        paused = true;
        emit Paused();
    }

    function unpause() public onlyOwner {
        paused = false;
        emit Unpaused();
    }

    function recoverTokens(address tokenAddress, uint256 amount) public onlyOwner {
        require(tokenAddress != address(this), "ERC20Token: cannot recover this token");
        IERC20(tokenAddress).transfer(owner(), amount);
    }
}

// Interface for ERC20 token recovery
interface IERC20 {
    function transfer(address recipient, uint256 amount) external returns (bool);
}
