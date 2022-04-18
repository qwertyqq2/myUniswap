// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./safeMath.sol";

interface IERC20 {
    function balanceOf(address account) external view returns (uint256);

    function transfer(address to, uint256 amount) external returns (bool);

    function approve(address spender, uint256 amount) external;

    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) external;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(
        address indexed owner,
        address indexed spender,
        uint256 value
    );
}

contract ERC20 {
    using SafeMath for uint256;
    uint256 public totalSupply;
    string public name;
    string public symbol;

    constructor(
        string memory _name,
        string memory _symbol,
        uint256 _initialSupply
    ) {
        name = _name;
        symbol = _symbol;
        totalSupply = _initialSupply;
    }

    uint8 public constant decimal = 18;

    mapping(address => uint256) balances;

    mapping(address => mapping(address => uint256)) allowed;

    function mint(address to) public payable {
        balances[to] = balances[to].add(msg.value);
        totalSupply = totalSupply.add(msg.value);
    }

    function balanceOf(address owner) public view returns (uint256) {
        return balances[owner];
    }

    function transfer(address _to, uint256 _value) public {
        require(balances[msg.sender] >= _value, "Not Enouth wei");
        balances[msg.sender] = balances[msg.sender].sub(_value);
        balances[_to] = balances[_to].add(_value);
    }

    function transferFrom(
        address _from,
        address _to,
        uint256 _value
    ) public {
        require(balances[_from] >= _value, "Err balance");
        balances[_from] = balances[_from].sub(_value);
        balances[_to] = balances[_to].add(_value);
    }

    function approve(address _spender, uint256 _value) public {
        allowed[msg.sender][_spender] = _value;
    }
}
