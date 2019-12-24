"""
libraptorQ encoder/decoder
"""

import hashlib
import logging
import sys
import time
import types

from DNARaptorQ import RQEncoder, RQDecoder, RQError

logging.basicConfig(
    format='%(asctime)s :: %(levelname)s :: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG if opts.debug else logging.WARNING)
log = logging.getLogger()

p = lambda fmt, *a, **k: \
    print(*([fmt.format(*a, **k)]
            if isinstance(fmt, types.StringTypes) and (a or k)
            else [[fmt] + list(a), k]), file=sys.stderr)

num_fmt = lambda n: '{:,}'.format(n)  # number format


def _timer_iter():
    ts0 = time.time()
    while True:
        ts = time.time()
        ts_diff, ts0 = ts - ts0, ts
        yield ts_diff


def timer_iter():
    timer = _timer_iter()
    next(timer)
    return timer


class EncDecFailure(Exception):
    pass


def encode(opts, data):
    """
    RaptorQ encoder
    Args:
        opts: args
        data: bytes

    Returns:
        dict: {data_len:int, oti_scheme:int, oti_common:int
                symbols:[int, [int]], checksums:str
                }
    """
    data_len, data_md5 = len(data), hashlib.md5(data).hexdigest()  # bytes length, bytes md5
    if data_len % 4 != 0:
        data += bytes((4 - data_len % 4))  # padding NULL for bytes
    timer = timer_iter()

    # Encoder
    with RQEncoder(data, opts['subsymbol_size'], opts['symbol_size'], opts['max_memory']) as enc:
        log.debug('Initialized RQEncoder (%.3fs)...', next(timer))
        oti_scheme, oti_common = enc.oti_scheme, enc.oti_common  # OTI value
        # Precomputed
        if not opts['no_precompute']:
            enc.precompute(opts['threads'], background=False)
            log.debug('Precomputed blocks (%.3fs)...', next(timer))

        symbols, enc_k, n_drop = list(), 0, 0
        for block in enc:
            enc_k += block.symbols  # not including repair ones
            block_syms = list(block.encode_iter(repair_rate=opts['repair_symbols_rate']))
            if opts['drop_rate'] > 0:
                import random
                n_drop_block = int(round(len(block_syms) * opts['drop_rate'], 0))
                for n in range(n_drop_block):
                    block_syms[int(random.random() * len(block_syms))] = None
                n_drop += n_drop_block
            symbols.extend(block_syms)
        log.debug('Finished encoding symbols (%s blocks, %.3fs)...', enc.blocks, next(timer))
    log.debug('Closed RQEncoder (%.3fs)...', next(timer))

    symbols = filter(None, symbols)
    if log.isEnabledFor(logging.DEBUG):
        log.debug(
            'Encoded %s B into %s symbols (needed: >%s, repair rate:'
            ' %d%%), %s dropped (%d%%), %s left in output (%s B without ids)',
            num_fmt(data_len), num_fmt(len(symbols) + n_drop),
            num_fmt(enc_k), opts['repair_symbols_rate'] * 100,
            num_fmt(n_drop), opts['drop_rate'] * 100, num_fmt(len(symbols)),
            num_fmt(sum(len(s[1]) for s in symbols)))

    return dict(data_bytes=data_len,
                oti_scheme=oti_scheme, oti_common=oti_common,
                symbols=list((s[0], list(s[1])) for s in symbols),
                checksums=dict(md5=data_md5))


def decode(config, symbols):
    """
    RaptorQ decoder
    Args:
        config: dict
        symbols:
    Returns:
        bytes
    """
    data_dec = _decode(config, symbols)
    if config['data_bytes'] != len(data_dec):
        raise EncDecFailure('Data length mismatch - {} B encoded vs {} B decoded'
                            .format(num_fmt(config['data_bytes']), num_fmt(len(data_dec))))

    data_md5 = config.get('checksums')
    for k, v in data_md5.viewitems():
        if getattr(hashlib, k)(data_dec).hexdigest() != v:
            raise EncDecFailure('Data checksum ({}) mismatch'.format(k))
    return data_dec


def _decode(config, symbols):
    """

    Args:
        config: dict
        symbols:

    Returns:
            bytes
    """
    n_syms, n_syms_total, n_sym_bytes = 0, len(symbols), 0
    if not symbols and config['oti_common'] == config['oti_scheme'] == 0:
        return ''  # zero-input/zero-output case
    timer = timer_iter()

    # Decoder
    with RQDecoder(config['oti_common'], config['oti_scheme']) as dec:
        log.debug('Initialized RQDecoder (%.3fs)...', next(timer))
        err = 'no symbols available'
        for sym_id, sym in symbols:
            sym_id, sym = int(sym_id), bytes(sym)
            try:
                dec.add_symbol(sym, sym_id)
            except RQError as err:
                continue
            n_syms, n_sym_bytes = n_syms + 1, n_sym_bytes + len(sym)
            try:
                data = dec.decode()[:config['data_bytes']]  # strips \0 padding to rq block size
            except RQError as err:
                pass
            else:
                log.debug('Decoded enough symbols to recover data (%.3fs)...', next(timer))
                break
        else:
            raise EncDecFailure(('Faled to decode data from {}'
                                 ' total symbols (processed: {}) - {}').format(n_syms_total, n_syms, err))
    log.debug('Closed RQDecoder (%.3fs)...', next(timer))
    if log.isEnabledFor(logging.DEBUG):
        log.debug(
            'Decoded %s B of data from %s processed'
            ' symbols (%s B without ids, symbols total: %s)',
            num_fmt(len(data)), num_fmt(n_syms),
            num_fmt(n_sym_bytes), num_fmt(n_syms_total))
    return data
