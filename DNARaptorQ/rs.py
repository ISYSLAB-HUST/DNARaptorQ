'''
Reed Solomon encoder/decoder
'''

from reedsolo import RSCodec
import warnings


class InnerRScode(object):
    def __init__(self, nsym=2):
        """

        Args:
            nsym: default:2, the number of bytes in the error correction code, can correct up to `nsym/2` of the errors in the message
        """
        if nsym > 0:
            self._nsym = nsym
        else:
            warnings.warn("nysm should be greater than 0, restore defaults(nysm=2)", Warning)
            self._nsym = 2
        self.RSCodec = RSCodec(self._nsym)

    def encode(self, data):
        """

        Args:
            data: str OR byte

        Returns:
            data_enc: bytearray
        """
        data_enc = self.RSCodec.encode(data)
        return data_enc

    def decode(self, data_enc):
        """

        Args:
            data_enc: str OR byte

        Returns:
            data_dec: bytearray
        """
        data_dec = self.RSCodec.decode(data_enc)
        return data_enc


if __name__ == '__main__':
    rs = InnerRScode(2)
    bit_enc = rs.encode([1,2,3,3,])
    print(bit_enc)
    bit_dec = rs.decode(bit_enc)[-2:]
    print([ord(item) for item in bit_dec.decode()])
