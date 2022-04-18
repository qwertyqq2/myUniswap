from re import S
import solcx
from Token import TokenContract


class Exchange:
    def __init__(self, address, pk_key, w3):
        token = TokenContract(address, pk_key, w3)
        nonce = w3.eth.getTransactionCount(address)
        res = solcx.compile_files(
            ["contracts/exchange.sol"],
            output_values=["abi", "bin"],
            solc_version="0.8.0"
        )
        abi = res['contracts/exchange.sol:Exchange']['abi']
        bytecode = res['contracts/exchange.sol:Exchange']['bin']
        contract = w3.eth.contract(abi=abi, bytecode=bytecode)
        token_address = token.get_address()
        tx = contract.constructor(token_address).buildTransaction(
            {
                "from": address,
                "nonce": nonce,
                "gasPrice": w3.eth.gas_price,
                "chainId": 1337,
                "gasPrice": 0,
            }
        )
        signed_txn = w3.eth.account.sign_transaction(tx, private_key=pk_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.address = tx_receipt['contractAddress']
        self.sender = address
        self.abi = abi
        self.bytecode = bytecode
        self.tx_hash = tx_hash
        self.token = token
        self.chain_id = 1337
        self.contract = w3.eth.contract(abi=self.abi, address=self.address)

    def addToken(self, address, nonce, pk_key, amount, w3):
        tx = self.contract.functions.addLiqToken(amount).buildTransaction(
            {
                "from": address,
                "nonce": nonce,
                "chainId": self.chain_id,
                "gasPrice": 0,
            }
        )
        signed_txn = w3.eth.account.sign_transaction(tx, private_key=pk_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash

    def addEth(self, address, nonce, pk_key, amount, w3):
        tx = self.contract.functions.addLiqEth().buildTransaction(
            {
                "from": address,
                "nonce": nonce,
                "chainId": self.chain_id,
                "value": amount,
                "gasPrice": 0,
            }
        )
        signed_txn = w3.eth.account.sign_transaction(tx, private_key=pk_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash

    def swapEthToToken(self, address, nonce, pk_key, amount, w3):
        tx = self.contract.functions.ethToTokenSwap().buildTransaction(
            {
                "from": address,
                "nonce": nonce,
                "chainId": self.chain_id,
                "value": amount,
                "gasPrice": 0,
            }
        )
        signed_txn = w3.eth.account.sign_transaction(tx, private_key=pk_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash

    def swapTokenToEth(self, address, nonce, pk_key, amount, w3):
        tx = self.contract.functions.tokenToEthSwap(amount).buildTransaction(
            {
                "from": address,
                "nonce": nonce,
                "chainId": self.chain_id,
                "gasPrice": 0,
            }
        )
        signed_txn = w3.eth.account.sign_transaction(tx, private_key=pk_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash

    def addTokenOnBalance(self, address, nonce, pk_key, amount, w3):
        tx = self.token.contract.functions.mint(address).buildTransaction(
            {
                "from": address,
                "nonce": nonce,
                "chainId": 1337,
                "value": amount,
                "gasPrice": 0,
            }
        )
        signed_txn = w3.eth.account.sign_transaction(tx, private_key=pk_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash

    def getTokenBalance(self, address):
        balance = self.contract.functions.getTokenBalanceOf(address).call()
        return balance

    def getLiqTokenBalance(self, address):
        balance = self.contract.functions.getLiqTokens(address).call()
        return balance

    def getLiqEthBalance(self, address):
        balance = self.contract.functions.getLiqEth(address).call()
        return balance

    def withdrawLiqToken(self, address, nonce, pk_key, amount, w3):
        tx = self.contract.functions.withdrawLiqToken(amount).buildTransaction(
            {
                "from": address,
                "nonce": nonce,
                "chainId": 1337,
                "gasPrice": 0,
            }
        )
        signed_txn = w3.eth.account.sign_transaction(tx, private_key=pk_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash

    def withdrawLiqEth(self, address, nonce, pk_key, amount, w3):
        tx = self.contract.functions.withdrawLiqEth(amount).buildTransaction(
            {
                "from": address,
                "nonce": nonce,
                "chainId": 1337,
                "gasPrice": 0,
            }
        )
        signed_txn = w3.eth.account.sign_transaction(tx, private_key=pk_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash

    def getPriceEth(self):
        price = self.contract.functions.getPriceEth().call()
        return price

    def getPriceToken(self):
        price = self.contract.functions.getPriceToken().call()
        return price

    def getEthReserve(self):
        return self.contract.functions.getEthReserve().call()

    def getTokenReserve(self):
        return self.contract.functions.getTokenReserve().call()

    def getAmount(self, in_am, in_res, out_res):
        return self.contract.functions.getAmount(in_am, in_res, out_res).call()

    def getEthStock(self):
        return self.contract.functions.getEthStock().call()

    def getTokenStock(self):
        return self.contract.functions.getTokenStock().call()
