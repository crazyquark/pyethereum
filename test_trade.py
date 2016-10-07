# -*- coding: utf8 -*-
from os import path

from ethereum import _solidity

from ethereum import tester
from ethereum import _solidity
from ethereum._solidity import get_solidity

SOLIDITY_AVAILABLE = get_solidity() is not None
CONTRACT_UNDER_TEST = path.join(path.dirname(path.abspath(__file__)), 'TradeFinanceContract.sol')

print CONTRACT_UNDER_TEST

state = tester.state()

buyer = 0x123456
seller = 0x654321
buyerDetails = 'NoBuyer'
sellerDetails = 'NoSeller'

print 'Testing constructor...'
contract = state.abi_contract(
    None,
    path=CONTRACT_UNDER_TEST,
    language='solidity',
    constructor_parameters=[buyer, seller, buyerDetails, sellerDetails]
)

parties = contract.getParties()
assert parties[0] == '0000000000000000000000000000000000123456'
assert parties[1] == 'NoBuyer'
assert parties[2] == '0000000000000000000000000000000000654321'
assert parties[3] == 'NoSeller'