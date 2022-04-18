// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AucEngine {
    address public owner;
    uint256 constant DURATION = 2 days;
    uint256 constant FEE = 10;
    struct Auction {
        address payable seller;
        uint256 startingPrice;
        uint256 startAt;
        uint256 finalPrice;
        uint256 endsAt;
        uint256 discountRate;
        string item;
        bool stopped;
    }

    Auction[] public auctions;

    event AuctionCreated(
        string itemName,
        uint256 startingPrice,
        uint256 duration
    );
    event AuctionEded(uint256 index, uint256 finalPrice, address winner);

    constructor() {
        owner = msg.sender;
    }

    function createAuction(
        uint256 _startingPrice,
        uint256 _dicountRate,
        string calldata _item,
        uint256 _duration
    ) external {
        uint256 duration = _duration == 0 ? DURATION : _duration;
        require(
            _startingPrice >= _dicountRate * duration,
            "Incorrent starting price"
        );
        Auction memory newAuct = Auction({
            seller: payable(msg.sender),
            startingPrice: _startingPrice,
            finalPrice: _startingPrice,
            discountRate: _dicountRate,
            startAt: block.timestamp,
            endsAt: block.timestamp + duration,
            item: _item,
            stopped: false
        });
        auctions.push(newAuct);

        emit AuctionCreated(_item, _startingPrice, duration);
    }

    function getPriceFor(uint256 index) public view returns (uint256) {
        Auction memory cAuction = auctions[index];
        require(!cAuction.stopped, "stopped!");
        uint256 elapsed = block.timestamp - cAuction.startAt;
        uint256 discount = cAuction.discountRate * elapsed;
        return cAuction.startingPrice - discount;
    }

    function buy(uint256 index) external payable {
        Auction memory cAuction = auctions[index];
        require(!cAuction.stopped, "stopped!");
        require(block.timestamp < cAuction.endsAt, "ended!");
        uint256 cPrice = getPriceFor(index);
        require(msg.value >= cPrice, "not enough funds!");
        cAuction.stopped = true;
        cAuction.finalPrice = cPrice;
        uint256 refund = msg.value - cPrice;
        if (refund > 0) {
            payable(msg.sender).transfer(refund);
        }
        cAuction.seller.transfer(cPrice - ((cPrice * FEE) / 100));
        emit AuctionEded(index, cPrice, msg.sender);
    }
}
