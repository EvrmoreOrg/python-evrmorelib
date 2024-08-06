# Copyright (C) The python-bitcoinlib developers
#
# This file is part of python-evrmorelib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-evrmorelib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.


import unittest

from evrmore.core import *
from evrmore.core.serialize import EvrHash

class Test_str_value(unittest.TestCase):
    def test(self):
        def T(value, expected):
            actual = str_money_value(value)
            self.assertEqual(actual, expected)

        T(         0,  '0.0')
        T(         1,  '0.00000001')
        T(        10,  '0.0000001')
        T(  12345678,  '0.12345678')
        T(  10000000,  '0.1')
        T( 100000000,  '1.0')
        T(1000000000, '10.0')
        T(1010000000, '10.1')
        T(1001000000, '10.01')
        T(1012345678, '10.12345678')

class Test_Money(unittest.TestCase):
    def test_MoneyRange(self):
        self.assertFalse(MoneyRange(-1))
        self.assertTrue(MoneyRange(0))
        self.assertTrue(MoneyRange(100000))
        self.assertTrue(MoneyRange(21000000 * 1000 * COIN)) # Maximum money on Evrmore network
        self.assertFalse(MoneyRange(21000001 * 1000 * COIN))

    def test_MoneyRangeCustomParams(self):
        highMaxParamsType = type(str('CoreHighMainParams'), (CoreMainParams,object), {'MAX_MONEY': 22000000 * COIN })
        highMaxParams = highMaxParamsType()
        self.assertTrue(MoneyRange(21000001 * COIN, highMaxParams))
        self.assertTrue(MoneyRange(22000000 * COIN, highMaxParams))
        self.assertFalse(MoneyRange(22000001 * COIN, highMaxParams))

class Test_CBlockHeader(unittest.TestCase):
    def test_serialization(self):
        genesis = CBlockHeader(nVersion=4,
                hashPrevBlock=lx('0000000000000000000000000000000000000000000000000000000000000000'),
                hashMerkleRoot=lx('c191c775b10d2af1fcccb4121095b2a018f1bee84fa5efb568fcddd383969262'),
                nTime=1667072172,
                nBits=0x1e00ffff,
                nHeight=0,
                nonce64=1777396,
                mix_hash=lx('0000000000000000000000000000000000000000000000000000000000000000'),
                nNonce=0)
        serialized = genesis.serialize()
        self.assertEqual(EvrHash(serialized),
                      lx('00000061fea06b985451647b6c4b111c0883017a80c4cce29a4277d7cc9c3d69'))

        genesis2 = CBlockHeader.deserialize(serialized)
        self.assertEqual(genesis, genesis2)

    def test_GetHash(self):
        genesis = CBlockHeader(nVersion=4,
                hashPrevBlock=lx('0000000000000000000000000000000000000000000000000000000000000000'),
                hashMerkleRoot=lx('28ff00a867739a352523808d301f504bc4547699398d70faf2266a8bae5f3516'),
                nTime=1514999494,
                nBits=0x1e00ffff,
                nNonce=25023712)
        self.assertEqual(genesis.GetHash(), lx('0000006b444bc2f2ffe627be9d9e7e7a0730000870ef6eb6da46c8eae389df90'))

    def test_calc_difficulty(self):
        def T(nbits, expected):
            actual = CBlockHeader.calc_difficulty(nbits)
            actual = round(actual, 3)
            self.assertEqual(actual, expected)

        T(486604799,        1.000) # block 0
        T(486594666,        1.183) # block 33333
        T(469809688,      352.161) # block 74000
        T(453179945,    22012.381) # block 105000
        T(436527338,  3438908.960) # block 210000
        T(426957810, 37392766.136) # block 250000

class Test_CBlock(unittest.TestCase):
    def test_serialization(self):
        initial_serialized = x('00000030053b69358576bc50a27eee295bab545d7776ef56c6a720241b48d0117b000000f1bc5bdb7415af47aacbd840c5c77a2ff7f8c42ab34c8eaa2b1adc02ea152f95cce35f63ffff001e0100000080dd2a4801c58ea5272d8df4076c2864e34fb9cce7c9e83bdbc1b9a4c8334bfec28163530b2fac0f01020000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025100ffffffff0300715a363a0000001976a9146288284ff8bc5dab99577dad295912666b909d1488ac0029d1770600000017a914a78f72cdb3a7ee5f09d5259ae7eb64231858bdc2870000000000000000266a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf90120000000000000000000000000000000000000000000000000000000000000000000000000')
        genesis = CBlock.deserialize(initial_serialized)
        serialized = genesis.serialize()
        self.assertEqual(EvrHash(serialized[0:120]),
                      lx('00000061fea06b985451647b6c4b111c0883017a80c4cce29a4277d7cc9c3d69'))
        self.assertEqual(serialized, initial_serialized)

    def test_GetHash(self):
        genesis = CBlock.deserialize(x('00000030053b69358576bc50a27eee295bab545d7776ef56c6a720241b48d0117b000000f1bc5bdb7415af47aacbd840c5c77a2ff7f8c42ab34c8eaa2b1adc02ea152f95cce35f63ffff001e0100000080dd2a4801c58ea5272d8df4076c2864e34fb9cce7c9e83bdbc1b9a4c8334bfec28163530b2fac0f01020000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025100ffffffff0300715a363a0000001976a9146288284ff8bc5dab99577dad295912666b909d1488ac0029d1770600000017a914a78f72cdb3a7ee5f09d5259ae7eb64231858bdc2870000000000000000266a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf90120000000000000000000000000000000000000000000000000000000000000000000000000'))
        self.assertEqual(genesis.GetHash(), lx('00000061fea06b985451647b6c4b111c0883017a80c4cce29a4277d7cc9c3d69'))

    def test_calc_merkle_root_of_empty_block(self):
        """CBlock.calc_merkle_root() fails if vtx empty"""
        block = CBlock()
        with self.assertRaises(ValueError):
            block.calc_merkle_root()

    def test_calc_merkle_root(self):
        # block 1
        block = CBlock.deserialize(x('00000030053b69358576bc50a27eee295bab545d7776ef56c6a720241b48d0117b000000f1bc5bdb7415af47aacbd840c5c77a2ff7f8c42ab34c8eaa2b1adc02ea152f95cce35f63ffff001e0100000080dd2a4801c58ea5272d8df4076c2864e34fb9cce7c9e83bdbc1b9a4c8334bfec28163530b2fac0f01020000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025100ffffffff0300715a363a0000001976a9146288284ff8bc5dab99577dad295912666b909d1488ac0029d1770600000017a914a78f72cdb3a7ee5f09d5259ae7eb64231858bdc2870000000000000000266a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf90120000000000000000000000000000000000000000000000000000000000000000000000000'))
        self.assertEqual(block.calc_merkle_root(), lx('952f15ea02dc1a2baa8e4cb32ac4f8f72f7ac7c540d8cbaa47af1574db5bbcf1'))
        self.assertEqual(block.vMerkleTree, (lx('952f15ea02dc1a2baa8e4cb32ac4f8f72f7ac7c540d8cbaa47af1574db5bbcf1'),))

        # 1000
        block = CBlock.deserialize(x('00000030060bec4ef4e9872107cb0ce914cf7c96485929662ae0976ee96f3f0200000000443a09069d4f6513fcbbef6134bee93f61ef24c107754a371b0759acc0946e488eed5f637522061ce8030000107867090040616917e0d25d520e59add7330a58a749653ce612f5ddbe16758a1887f9491848774601010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff0b02e803048eed5f630269610000000004c06a54a1390000001976a914221c04a580fbcd01454409e692e4566965185d9f88ac0029d1770600000017a914a78f72cdb3a7ee5f09d5259ae7eb64231858bdc28740060695000000001976a914d81d2dc77f527e3d30d4abe7a9948e70807c579688ac0000000000000000266a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf90120000000000000000000000000000000000000000000000000000000000000000000000000'))
        self.assertEqual(block.calc_merkle_root(), lx('486e94c0ac59071b374a7507c124ef613fe9be3461efbbfc13654f9d06093a44'))
