"""
LFSR module by Zhanghang
"""


def lfsr(state, mask):
    # Galois lfsr:
    result = state
    nbits = mask.bit_length() - 1
    while True:
        result = (result << 1)
        xor = result >> nbits
        if xor != 0:
            result ^= mask
        yield result


def lfsr16mask():
    # this function returns a hard coded polynomial (0b10000000000101101).
    # The polynomial corresponds to 1 + x^11 + x^13 + x^14 + x^16, which is known
    # to repeat only after 16^2-1 tries. Don't change this number!
    return 0b10000000000101101


def pseudo_random(seed, len_payload):
    # 32 Byte pseudo-random number generator
    pr_block = int(len_payload / 2)
    lf = lfsr(seed, lfsr16mask())
    s = ''
    for i in range(pr_block):
        s += '{:016b}'.format(next(lf))
    pseudo_sequence = []
    for a in range(0, len(s), 8):
        pseudo_sequence.append(int(s[a:a+8], 2))
    return pseudo_sequence


if __name__ == '__main__':
    ps = pseudo_random(111, 32)
    print(ps)
