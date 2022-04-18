from brownie import accounts
from hexbytes import HexBytes
from User import User
from web3 import Web3
from eth_account import Account
from eth_keys import keys
import random
import matplotlib.pyplot as plt
import numpy as np


def createUsers(password, count_acc, accpath, w3):
    users = []
    for idx in range(count_acc):
        acct = Account.from_mnemonic(password, account_path=accpath+str(idx))
        pk = acct.key
        pk_key = str(keys.PrivateKey(pk))
        addr = acct._address
        user = User(addr, pk_key, w3)
        users.append(user)
    return users


def swap(users, exchange):
    counter = 0
    points = []
    l = []
    print("start reserve : ", exchange.getTokenReserve(), exchange.getEthReserve())
    for user in users:
        if counter == 0:
            amount = random.randint(1, 100000)
            print("swap token ", amount)
            user.swapTokenOnEth(exchange, amount)
            points.append((exchange.getEthReserve(),
                          exchange.getTokenReserve()))
            l.append((exchange.getTokenStock(), exchange.getEthStock()))

            counter = 1
        elif counter == 1:
            amount = random.randint(1, 100000)
            print("swap eth ", amount)
            user.swapEthToToken(exchange, amount)
            points.append((exchange.getEthReserve(),
                          exchange.getTokenReserve()))
            l.append((exchange.getTokenStock(), exchange.getEthStock()))
            counter = 0
    return points, l


def main():
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
    count_acc = 100
    password = "soft intact make super filter ritual sing govern attitude flight best into"
    accpath = "m/44'/60'/0'/0/"
    print("Creation users...")
    users = createUsers(password, count_acc, accpath, w3)
    me = users[0]
    exchange = users[0].createExchange()
    x = []
    y = []
    le = []
    lt = []
    print("Start liquidity...")
    for user in users:
        user.addToken(exchange, 1000000000)
        user.addLiqToken(exchange, 100000)
        user.addLiqEth(exchange, 100000)
    print(exchange.getTokenStock())
    print(exchange.getEthStock())

    for i in range(1):
        points, liq = swap(users, exchange)

        for p in points:
            x.append(p[0])
            y.append(p[1])

        for l in liq:
            le.append(l[0])
            lt.append(l[1])

    plt.plot(x, y)
    plt.show()

    plt.plot(np.arange(0, len(le)), le, 'r')
    plt.plot(np.arange(0, len(lt)), lt, 'b')
    plt.show()

    plt.plot(np.arange(0, len(x)), x, 'r')
    plt.plot(np.arange(0, len(y)), y, 'b')
    plt.show()

    print(me.getTokenBalance(exchange))
    print(me.getLiqTokenBalance(exchange))
    me.withdrawLiqToken(exchange, 100000)
    print(me.getTokenBalance(exchange))
    print(me.getLiqTokenBalance(exchange))


main()
