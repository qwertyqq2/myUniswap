// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "./safeMath.sol";
import "./erc20.sol";

contract Exchange is ERC20 {
    using SafeMath for uint256;

    address public tokenAddress;

    mapping(address => uint256) liqTokensOnAccount;
    mapping(address => uint256) liqEthOnAccount;

    uint256 private ethTotal;
    uint256 private tokenTotal;
    uint256 private tokenStock;
    uint256 private ethStock;
    uint256 private ethSupply;

    uint256 private minTokens;
    uint256 private minEth;
    uint256 private commission_procent = 1;

    constructor(address _token) ERC20("Uniswap", "UniToken", 0) {
        require(_token != address(0), "invalid token address");
        tokenAddress = _token;
        minTokens = 0;
        minEth = 0;
    }

    function addLiqToken(uint256 _tokenAmount) public {
        if (getReserveToken() == 0) {
            uint256 liqTokens = _tokenAmount;
            IERC20 token = IERC20(tokenAddress);
            token.transferFrom(msg.sender, address(this), _tokenAmount);
            liqTokensOnAccount[msg.sender] += liqTokens;
            totalSupply += liqTokens;
            tokenTotal += _tokenAmount;
        } else {
            uint256 liqTokens = (100 * _tokenAmount) / totalSupply;
            IERC20 token = IERC20(tokenAddress);
            token.transferFrom(msg.sender, address(this), _tokenAmount);
            liqTokensOnAccount[msg.sender] += liqTokens;
            totalSupply += liqTokens;
            tokenTotal += _tokenAmount;
        }
    }

    function addLiqEth() public payable {
        if (address(this).balance - msg.value == 0) {
            uint256 liqEth = msg.value;
            liqEthOnAccount[msg.sender] += liqEth;
            ethTotal += msg.value;
            ethSupply += msg.value;
        } else {
            uint256 ethReserve = address(this).balance - msg.value;
            uint256 liqEth = (100 * msg.value) / ethReserve;
            liqEthOnAccount[msg.sender] += liqEth;
            ethTotal += msg.value;
            ethSupply += msg.value;
        }
    }

    function getLiqEth(address addr) public view returns (uint256) {
        return liqEthOnAccount[addr];
    }

    function getLiqTokens(address addr) public view returns (uint256) {
        return liqTokensOnAccount[addr];
    }

    function getReserveEth() public view returns (uint256) {
        return address(this).balance;
    }

    function getReserveToken() public view returns (uint256) {
        return IERC20(tokenAddress).balanceOf(address(this));
    }

    function getPrice(uint256 inputReserve, uint256 outputReserve)
        public
        pure
        returns (uint256)
    {
        require(inputReserve > 0 && outputReserve > 0, "invalid reserves");
        return SafeMath.div(inputReserve, outputReserve);
    }

    function getPriceEth() public view returns (uint256) {
        return
            getPrice(
                address(this).balance,
                IERC20(tokenAddress).balanceOf(address(this))
            );
    }

    function getPriceToken() public view returns (uint256) {
        return
            getPrice(
                IERC20(tokenAddress).balanceOf(address(this)),
                address(this).balance
            );
    }

    function getEthReserve() public view returns (uint256) {
        return ethTotal;
    }

    function getTokenReserve() public view returns (uint256) {
        return tokenTotal;
    }

    function getAmount(
        uint256 inputAmount,
        uint256 inputReserve,
        uint256 outputReserve
    ) public pure returns (uint256) {
        require(inputReserve > 0 && outputReserve > 0, "invalid reserves");
        uint256 denomenator = inputAmount + inputReserve;
        uint256 numenator = inputAmount * outputReserve;
        return numenator / denomenator;
    }

    function ethToTokenSwap() public payable {
        uint256 tokenReserve = getReserveToken();
        uint256 remain = (msg.value * commission_procent) / 100;
        ethStock += remain;
        ethTotal += msg.value - remain;
        uint256 tokenBounds = getAmount(
            msg.value - remain,
            address(this).balance,
            tokenReserve
        );
        require(minTokens <= tokenBounds, "tokenBounds too small");
        tokenTotal -= tokenBounds;
        IERC20(tokenAddress).transferFrom(
            address(this),
            msg.sender,
            tokenBounds
        );
    }

    function tokenToEthSwap(uint256 _tokenSold) public {
        uint256 tokenReserve = getReserveToken();
        uint256 remain = (_tokenSold * commission_procent) / 100;
        uint256 tokenSold = _tokenSold - remain;
        tokenStock += remain;
        tokenTotal += tokenSold;
        uint256 ethBounds = getAmount(
            tokenSold,
            tokenReserve,
            address(this).balance
        );
        require(minEth <= ethBounds || ethBounds <= 0, "ethBounds too small");
        IERC20(tokenAddress).transferFrom(
            msg.sender,
            address(this),
            _tokenSold
        );
        ethTotal -= ethBounds;
        payable(msg.sender).transfer(ethBounds);
    }

    function getTokenBalanceOf(address _addr) public view returns (uint256) {
        IERC20 token = IERC20(tokenAddress);
        uint256 balance = token.balanceOf(_addr);
        return balance;
    }

    function withdrawLiqToken(uint256 amount) public {
        require(liqTokensOnAccount[msg.sender] >= amount, "Not enouth tokens");
        uint256 procent = (amount * 10000) / totalSupply;
        uint256 res = (tokenStock * procent) / 10000;
        liqTokensOnAccount[msg.sender] -= amount;
        IERC20(tokenAddress).transferFrom(address(this), msg.sender, res);
    }

    function withdrawLiqEth(uint256 amount) public {
        require(liqEthOnAccount[msg.sender] >= amount, "Not enouth eth");
        uint256 procent = (amount * 10000) / ethSupply;
        uint256 res = (ethStock * procent) / 10000;
        liqEthOnAccount[msg.sender] -= amount;
        payable(msg.sender).transfer(res);
    }

    function getCommission() public view returns (uint256) {
        return commission_procent;
    }

    function getEthStock() public view returns (uint256) {
        return ethStock;
    }

    function getTokenStock() public view returns (uint256) {
        return tokenStock;
    }
}
