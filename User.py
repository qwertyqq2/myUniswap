from Exchange import Exchange
import time


class User:
    def __init__(self, address, pk_key, w3) -> None:
        ###### Тут должна быть проверка pk_key #######
        ##############################################
        self.w3 = w3
        self.address = address
        self.pk_key = pk_key
        self.nonce = self.w3.eth.getTransactionCount(address)

    def __repr__(self) -> str:
        return str(self.address) + " " + str(self.pk_key)

    def createExchange(self) -> Exchange:
        return Exchange(self.address, self.pk_key, self.w3)

    def addTokenAsync(self, exchange, amount):
        self.nonce = self.w3.eth.getTransactionCount(self.address)
        exchange.addTokenOnBalance(
            self.address, self.nonce, self.pk_key, amount, self.w3)

    def addToken(self, exchange, amount):
        self.nonce = self.w3.eth.getTransactionCount(self.address)
        exchange.addTokenOnBalance(
            self.address, self.nonce, self.pk_key, amount, self.w3)

    def getTokenBalance(self, exchange):
        return exchange.getTokenBalance(self.address)

    def getLiqTokenBalance(self, exchange):
        return exchange.getLiqTokenBalance(self.address)

    def getLiqEthBalance(self, exchange):
        return exchange.getLiqEthBalance(self.address)

    def addLiqTokenAsync(self, exchange, amount):
        self.nonce = self.w3.eth.getTransactionCount(self.address)
        exchange.addToken(self.address, self.nonce,
                          self.pk_key, amount, self.w3)

    def addLiqToken(self, exchange, amount):
        self.nonce = self.w3.eth.getTransactionCount(self.address)
        exchange.addToken(self.address, self.nonce,
                          self.pk_key, amount, self.w3)

    def addLiqEthAsync(self, exchange, amount):
        self.nonce = self.w3.eth.getTransactionCount(self.address)
        exchange.addEth(self.address, self.nonce, self.pk_key, amount, self.w3)

    def addLiqEth(self, exchange, amount):
        self.nonce = self.w3.eth.getTransactionCount(self.address)
        exchange.addEth(self.address, self.nonce, self.pk_key, amount, self.w3)

    def swapTokenOnEth(self, exchange, amount):
        self.nonce = self.w3.eth.getTransactionCount(self.address)
        exchange.swapTokenToEth(self.address, self.nonce,
                                self.pk_key, amount, self.w3)

    def swapEthToToken(self, exchange, amount):

        self.nonce = self.w3.eth.getTransactionCount(self.address)
        exchange.swapEthToToken(self.address, self.nonce,
                                self.pk_key, amount, self.w3)

    def withdrawLiqToken(self, exchange, amount):
        self.nonce = self.w3.eth.getTransactionCount(self.address)
        exchange.withdrawLiqToken(
            self.address, self.nonce, self.pk_key, amount, self.w3)

    def withdrawLiqEth(self, exchange, amount):
        self.nonce = self.w3.eth.withdrawLiqEth(self.address)
        exchange.withdrawLiqToken(
            self.address, self.nonce, self.pk_key, amount, self.w3)

    #######################################################


class Process():
    def __init__(self, user, exhange):
        self.user = user
        self.time_created = time.time()
        self.exchange = exhange
        self.is_work = True
        self.past_data = []

    def state(self):
        return self.is_work
