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

contract = state.abi_contract(
    None,
    path=CONTRACT_UNDER_TEST,
    language='solidity'
)

print contract
