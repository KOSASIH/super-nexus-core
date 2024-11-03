// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Marketplace {
    struct Item {
        uint id;
        string name;
        uint price;
        address payable owner;
        bool sold;
    }

    mapping(uint => Item) public items;
    uint public itemCount;

    event ItemCreated(uint id, string name, uint price, address owner);
    event ItemSold(uint id, address buyer);

    function createItem(string memory name, uint price) public {
        require(price > 0, "Price must be greater than 0");
        itemCount++;
        items[itemCount] = Item(itemCount, name, price, payable(msg.sender), false);
        emit ItemCreated(itemCount, name, price, msg.sender);
    }

    function buyItem(uint id) public payable {
        Item memory item = items[id];
        require(id > 0 && id <= itemCount, "Item does not exist");
        require(msg.value >= item.price, "Not enough Ether to purchase item");
        require(!item.sold, "Item already sold");
        
        item.owner.transfer(msg.value);
        item.sold = true;
        items[id] = item; // Update the item in the mapping
        emit ItemSold(id, msg.sender);
    }

    function getItem(uint id) public view returns (Item memory) {
        return items[id];
    }
}
