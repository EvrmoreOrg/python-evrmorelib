# Copyright (C) The python-bitcoinlib developers
#
# This file is part of python-evrmorelib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-ravencoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.


import unittest

from evrmore.wallet import CEvrmoreSecret
from evrmore.signmessage import EvrmoreMessage, VerifyMessage, SignMessage
import sys
import os
import json

def load_test_vectors(name):
    with open(os.path.dirname(__file__) + '/data/' + name, 'r') as fd:
        return json.load(fd)


class Test_SignVerifyMessage(unittest.TestCase):
    def test_verify_message_simple(self):
        address = "EcUicWyyb5EBrsiPB1fdQqEarQuVZmjyT5"
        message = address
        signature = "IBHayJqbHKckXN8iDMm7PVL7f+y9ZfsuODgnPXwXln9rTh4Q1C03Jsj+jO6xDxcFalGgY8yr0Rihhbg1wX5LnyA="

        message = EvrmoreMessage(message)

        self.assertTrue(VerifyMessage(address, message, signature))

    def test_verify_message_vectors(self):
        for vector in load_test_vectors('signmessage.json'):
            message = EvrmoreMessage(vector['address'])
            self.assertTrue(VerifyMessage(vector['address'], message, vector['signature']))

    def test_sign_message_simple(self):
        key = CEvrmoreSecret("KywSNadPCm5bjGFomCT5xB57Xbiqj1LtAKeziz7z9tofSLuFKqrL")
        address = "EcUicWyyb5EBrsiPB1fdQqEarQuVZmjyT5"
        message = address

        message = EvrmoreMessage(message)
        signature = SignMessage(key, message)

        self.assertTrue(signature)
        self.assertTrue(VerifyMessage(address, message, signature))

    def test_sign_message_vectors(self):
        for vector in load_test_vectors('signmessage.json'):
            key = CEvrmoreSecret(vector['wif'])
            message = EvrmoreMessage(vector['address'])

            signature = SignMessage(key, message)

            self.assertTrue(signature, "Failed to sign for [%s]" % vector['address'])
            self.assertTrue(VerifyMessage(vector['address'], message, vector['signature']), "Failed to verify signature for [%s]" % vector['address'])


if __name__ == "__main__":
    unittest.main()
