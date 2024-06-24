# Copyright (C) The python-bitcoinlib developers
# Copyright (C) 2018-2020 The python-ravencoinlib developers
#
# This file is part of python-evrmorelib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-evrmorelib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.


from evrmore.core.key import CPubKey
from evrmore.core.serialize import ImmutableSerializable
from evrmore.wallet import P2PKHEvrmoreAddress
import evrmore
import base64


def VerifyMessage(address, message, sig):
    sig = base64.b64decode(sig)
    hash = message.GetHash()

    pubkey = CPubKey.recover_compact(hash, sig)

    return str(P2PKHEvrmoreAddress.from_pubkey(pubkey)) == str(address)


def SignMessage(key, message):
    sig, i = key.sign_compact(message.GetHash())

    meta = 27 + i
    if key.is_compressed:
        meta += 4

    return base64.b64encode(bytes([meta]) + sig)


class EvrmoreMessage(ImmutableSerializable):
    __slots__ = ['magic', 'message']

    def __init__(self, message="", magic="Raven Signed Message:\n"):
        object.__setattr__(self, 'message', message.encode("utf-8"))
        object.__setattr__(self, 'magic', magic.encode("utf-8"))

    @classmethod
    def stream_deserialize(cls, f):
        magic = evrmore.core.serialize.BytesSerializer.stream_deserialize(f)
        message = evrmore.core.serialize.BytesSerializer.stream_deserialize(f)
        return cls(message, magic)

    def stream_serialize(self, f):
        evrmore.core.serialize.BytesSerializer.stream_serialize(self.magic, f)
        evrmore.core.serialize.BytesSerializer.stream_serialize(self.message, f)

    def __str__(self):
        return self.message.decode('ascii')

    def __repr__(self):
        return 'EvrmoreMessage(%s, %s)' % (self.magic, self.message)
