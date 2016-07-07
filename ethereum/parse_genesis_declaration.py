from ethereum.state import State, STATE_DEFAULTS
from ethereum.block import Block, BlockHeader, FakeHeader
from ethereum.utils import decode_hex, big_endian_to_int, encode_hex, \
    parse_as_bin, parse_as_int
from ethereum.state_transition import initialize
from ethereum.config import Env
from ethereum.db import OverlayDB
import rlp

def state_from_genesis_declaration(genesis_data, env):
    h = BlockHeader(nonce=parse_as_bin(genesis_data["nonce"]),
                    difficulty=parse_as_int(genesis_data["difficulty"]),
                    mixhash=parse_as_bin(genesis_data["mixhash"]),
                    coinbase=parse_as_bin(genesis_data["coinbase"]),
                    timestamp=parse_as_int(genesis_data["timestamp"]),
                    prevhash=parse_as_bin(genesis_data["parentHash"]),
                    extra_data=parse_as_bin(genesis_data["extraData"]),
                    gas_limit=parse_as_int(genesis_data["gasLimit"]))
    blk = Block(h, [], [])
    state = State(env=env)
    for addr, data in genesis_data["alloc"].items():
        if len(addr) == 40:
            addr = decode_hex(addr)
        assert len(addr) == 20
        if 'wei' in data:
            state.set_balance(addr, parse_as_int(data['wei']))
        if 'balance' in data:
            state.set_balance(addr, parse_as_int(data['balance']))
        if 'code' in data:
            state.set_code(addr, parse_as_bin(data['code']))
        if 'nonce' in data:
            state.set_nonce(addr, parse_as_int(data['nonce']))
        if 'storage' in data:
            for k, v in data['storage'].items():
                state.set_storage_data(addr, parse_as_bin(k), parse_as_bin(v))
    initialize(state, blk)
    state.commit()
    blk.header.state_root = state.trie.root_hash
    state.prev_headers=[h]
    return state


def mk_basic_state(alloc, header, env):
    state = State(env=env)
    state["prev_headers"] = [FakeHeader(hash=parse_as_bin(header['hash']),
                                        number=parse_as_int(header['number']),
                                        timestamp=parse_as_int(header['timestamp']),
                                        difficulty=parse_as_int(header['difficulty']),
                                        gas_limit=parse_as_int(header['gas_limit']))]
    
    for addr, data in genesis_data["alloc"].items():
        if len(addr) == 40:
            addr = decode_hex(addr)
        assert len(addr) == 20
        if 'wei' in data:
            state.set_balance(addr, parse_as_int(data['wei']))
        if 'balance' in data:
            state.set_balance(addr, parse_as_int(data['balance']))
        if 'code' in data:
            state.set_code(addr, parse_as_bin(data['code']))
        if 'nonce' in data:
            state.set_nonce(addr, parse_as_int(data['nonce']))
        if 'storage' in data:
            for k, v in data['storage'].items():
                state.set_storage_data(addr, parse_as_bin(k), parse_as_bin(v))

    state.block_number = header["number"]
    state.gas_limit = header["gas_limit"]
    state.timestamp = header["timestamp"]
    state.block_difficulty = header["difficulty"]
    state.commit()
    return state


def mk_poststate_of_block(block, env):
    state = State(env=env)
    state.trie.root_hash = block.header.state_root
    initialize(state, block)
    state.gas_used = block.header.gas_used
    state.txindex = len(block.transactions)
    state.recent_uncles = {}
    state.prev_headers = []
    b = block
    for i in range(257):
        state.prev_headers.append(b.header)
        if i < 6:
            state.recent_uncles[state.block_number - i] = []
            for u in b.uncles:
                state.recent_uncles[state.block_number - i].append(u.hash)
        try:
            b = rlp.decode(state.db.get(b.header.prevhash), Block)
        except:
            break
    return state

