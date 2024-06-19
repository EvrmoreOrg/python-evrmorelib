# Copyright (C) The python-bitcoinlib developers
# Copyright (C) 2018-2020 The python-ravencoinlib developers
#
# This file is part of python-ravencoinlib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-ravencoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.


from ravencoin.core.key import CPubKey
from ravencoin.core.serialize import ImmutableSerializable
from ravencoin.wallet import P2PKHRavencoinAddress
import ravencoin
import base64


def VerifyMessage(address, message, sig):
    sig = base64.b64decode(sig)
    hash = message.GetHash()

    pubkey = CPubKey.recover_compact(hash, sig)

    return str(P2PKHRavencoinAddress.from_pubkey(pubkey)) == str(address)


def SignMessage(key, message):
    sig, i = key.sign_compact(message.GetHash())

    meta = 27 + i
    if key.is_compressed:
        meta += 4

    return base64.b64encode(bytes([meta]) + sig)


class RavencoinMessage(ImmutableSerializable):
    __slots__ = ['magic', 'message']

    def __init__(self, message="", magic="Raven Signed Message:\n"):
        object.__setattr__(self, 'message', message.encode("utf-8"))
        object.__setattr__(self, 'magic', magic.encode("utf-8"))

    @classmethod
    def stream_deserialize(cls, f):
        magic = ravencoin.core.serialize.BytesSerializer.stream_deserialize(f)
        message = ravencoin.core.serialize.BytesSerializer.stream_deserialize(f)
        return cls(message, magic)

    def stream_serialize(self, f):
        ravencoin.core.serialize.BytesSerializer.stream_serialize(self.magic, f)
        ravencoin.core.serialize.BytesSerializer.stream_serialize(self.message, f)

    def __str__(self):
        return self.message.decode('ascii')

    def __repr__(self):
        return 'RavencoinMessage(%s, %s)' % (self.magic, self.message)
