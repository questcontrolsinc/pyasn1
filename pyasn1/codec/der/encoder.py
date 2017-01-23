#
# This file is part of pyasn1 software.
#
# Copyright (c) 2005-2017, Ilya Etingof <etingof@gmail.com>
# License: http://pyasn1.sf.net/license.html
#
from pyasn1.type import univ
from pyasn1.codec.cer import encoder
from pyasn1 import error


class SetOfEncoder(encoder.SetOfEncoder):
    @staticmethod
    def _cmpSetComponents(c1, c2):
        tagSet1 = isinstance(c1, univ.Choice) and c1.getEffectiveTagSet() or c1.getTagSet()
        tagSet2 = isinstance(c2, univ.Choice) and c2.getEffectiveTagSet() or c2.getTagSet()
        return cmp(tagSet1, tagSet2)


tagMap = encoder.tagMap.copy()
tagMap.update({
    # Overload CER encoders with BER ones (a bit hackerish XXX)
    univ.BitString.tagSet: encoder.encoder.BitStringEncoder(),
    univ.OctetString.tagSet: encoder.encoder.OctetStringEncoder(),
    # Set & SetOf have same tags
    univ.SetOf().tagSet: SetOfEncoder()
})

typeMap = encoder.typeMap


class Encoder(encoder.Encoder):
    supportIndefLength = False

    def __call__(self, client, defMode=True, maxChunkSize=0):
        if not defMode:
            raise error.PyAsn1Error('DER forbids indefinite length mode')
        return encoder.Encoder.__call__(self, client, defMode, maxChunkSize)

#: Turns ASN.1 object into DER octet stream.
#:
#: Takes any ASN.1 object (e.g. :py:class:`~pyasn1.type.base.PyAsn1Item` derivative)
#: walks all its components recursively and produces a DER octet stream.
#:
#: Parameters
#: ----------
#  value: any pyasn1 type object (e.g. :py:class:`~pyasn1.type.base.PyAsn1Item` derivative)
#:     A pyasn1 type object to encode
#:
#: defMode: :py:class:`bool`
#:     If `False`, produces indefinite length encoding
#:
#: maxChunkSize: :py:class:`int`
#:     Maximum chunk size in chunked encoding mode (0 denotes unlimited chunk size)
encode = Encoder(tagMap, typeMap)
