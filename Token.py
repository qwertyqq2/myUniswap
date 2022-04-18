import solcx


class TokenContract:
    def __init__(self, address, pk_key, w3):
        nonce = w3.eth.getTransactionCount(address)
        res = solcx.compile_files(
            ["contracts/erc20.sol"],
            output_values=["abi", "bin"],
            solc_version="0.8.0"
        )
        abi = res['contracts/erc20.sol:ERC20']['abi']
        bytecode = res['contracts/erc20.sol:ERC20']['bin']
        token_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
        tx = token_contract.constructor("AltToken", "ALT", 0).buildTransaction(
            {
                "from": address,
                "nonce": nonce,
                "gasPrice": w3.eth.gas_price,
                "chainId": 1337,
            }
        )
        signed_txn = w3.eth.account.sign_transaction(tx, private_key=pk_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.sender = address
        self.abi = abi
        self.bytecode = bytecode
        self.tx_hash = tx_hash
        self.address = tx_receipt['contractAddress']
        self.contract = w3.eth.contract(abi=self.abi, address=self.address)

    def get_address(self):
        return self.address
