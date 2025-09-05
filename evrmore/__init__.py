# Copyright (C) 2012-2018 The python-bitcoinlib developers
# Copyright (C) 2018-2020 The python-evrmorelib developers
#
# This file is part of python-evrmorelib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-evrmorelib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

from __future__ import absolute_import, division, print_function, unicode_literals

import evrmore.core

from version import __version__


class MainParams(evrmore.core.CoreMainParams):
    MESSAGE_START = b'\x45\x56\x52\x4d'
    DEFAULT_PORT = 8820
    RPC_PORT = 8819
    DNS_SEEDS = (('seed-mainnet-evr.evrmorecoin.org', 'seed-evrmore.evrmore.com'))
    BASE58_PREFIXES = {'PUBKEY_ADDR': 33,
                       'SCRIPT_ADDR': 92,
                       'SECRET_KEY': 128}
    BECH32_HRP = 'evr'


class TestNetParams(evrmore.core.CoreTestNetParams):
    MESSAGE_START = b'\x45\x56\x52\x54'
    DEFAULT_PORT = 18820
    RPC_PORT = 18819
    DNS_SEEDS = (('seed-testnet-evr.evrmorecoin.org', 'seed-testnet-evrmore.evrmore.com'))
    BASE58_PREFIXES = {'PUBKEY_ADDR': 111,
                       'SCRIPT_ADDR': 196,
                       'SECRET_KEY': 239}
    BECH32_HRP = 'evrt'


class RegTestParams(evrmore.core.CoreRegTestParams):
    MESSAGE_START = b'\xfa\xbf\xb5\xda'
    DEFAULT_PORT = 18444
    RPC_PORT = 18443
    DNS_SEEDS = ()
    BASE58_PREFIXES = {'PUBKEY_ADDR': 111,
                       'SCRIPT_ADDR': 196,
                       'SECRET_KEY': 239}
    BECH32_HRP = 'evrr'


"""Master global setting for what chain params we're using.

However, don't set this directly, use SelectParams() instead so as to set the
evrmore.core.params correctly too.
"""
# params = evrmore.core.coreparams = MainParams()
params = MainParams()


def SelectParams(name):
    """Select the chain parameters to use

    name is one of 'mainnet', 'testnet', or 'regtest'

    Default chain is 'mainnet'
    """
    global params
    evrmore.core._SelectCoreParams(name)
    if name == 'mainnet':
        params = evrmore.core.coreparams = MainParams()
    elif name == 'testnet':
        params = evrmore.core.coreparams = TestNetParams()
    elif name == 'regtest':
        params = evrmore.core.coreparams = RegTestParams()
    else:
        raise ValueError('Unknown chain %r' % name)
