"""
main module
"""
import argparse
import json

from .RaptorQ import *
from .lfsr import *
from .rs import InnerRScode
from .utils import *


def EncoderToDNA(data, len_payload, nsym):
    """

    Args:
        data:
        len_payload:
        nsym:

    Returns:

    """
    dna_str = []
    for item in data["symbols"]:
        symbol_id = item[0]
        symbol = item[1]
        pseudo_sequence = pseudo_random(symbol_id, len_payload)
        _symbol = Randomization(symbol, pseudo_sequence)
        _rs = InnerRScode(nsym)
        rs_enc = list(_rs.encode(pseudo_sequence.insert(0, symbol_id)))
        item_dna_str = sixteen_to_dna(int_to_sixteen(symbol_id)) + BinToDNA(rs_enc[1:])
        dna_str.append(item_dna_str)
    return dna_str


def DNAToDecoder(dna_str, dna_len, nsym, len_payload):
    """

    Args:
        dna_str: str
        dna_len: int
        nsym: int
        len_payload: int
    """
    symbols = []
    for item in dna_str:
        if len(item) == dna_len:  # DNA length check
            dna_symbol_id = item[0:12]
            dna_symbol_rs = item[12:]
            symbol_id = dna_to_symbol_id_half(dna_symbol_id)
            symbol_rs = DNAToBin(dna_symbol_rs + dna_symbol_rs)
            symbol, rs = symbol_rs[:-nsym], symbol_rs[-nsym:]
            _rs = InnerRScode(nsym)
            symbol_correct = _rs.decode(list(symbol_id) + symbol_rs)[:-nsym]
            if np.count_nonzero(symbol != symbol_correct) == 0:
                pseudo_sequence = pseudo_random(symbol_id, len_payload)
                _symbol = UnRandomization(symbol, pseudo_sequence)
                symbols.append([symbol_id, _symbol])
    return symbols


def main():
    parser = argparse.ArgumentParser(
        description="Encode/decode data using RaptorQ rateless "
                    "erasure encoding (\"fountain code\") algorithm, using libRaptorQ through CFFI.")
    parser.add_argument('--debug', action='store_true', help='Verbose operation mode.')
    cmds = parser.add_subparsers(dest='cmd',
                                 title='Supported operations (have their own suboptions as well)')

    cmd = cmds.add_parser('encode',
                          help='Encode file into chunks and dump these along with OTI parameters as a JSON structure.')
    cmd.add_argument('path_src', nargs='?',
                     help='Path to a file which contents should be encoded. Stdin will be used, if not specified.')
    cmd.add_argument('path_dst', nargs='?',
                     help='Path to write resulting JSON to. Will be dumped to stdout, if not specified.')

    cmd.add_argument('--no-precompute', action='store_true',
                     help='Do not run precompute() synchronously before encoding symbols.'
                          ' Should be much slower, so probably only useful for benchmarking or debugging.')
    cmd.add_argument('-j', '--threads',
                     type=int, metavar='n',
                     help='Number of encoder threads to use. 0 to scale to all cpus (default).')
    cmd.add_argument('-k', '--subsymbol-size',
                     type=int, metavar='bytes',
                     help='Should almost always be equal to symbol size.'
                          ' See RFC6330 for details. Set to value of symbols size if not specified.')
    cmd.add_argument('-s', '--symbol-size',
                     required=True, type=int, metavar='bytes',
                     help='Size of each indivisible (must either be'
                          ' present intact or lost entirely when decoding) symbol in the output.'
                          ' Using wrong value here (for data size) can result in undecodable output.'
                          ' See RFC6330 or libRaptorQ code/docs for more information.'
                          ' Must be specified manually.')
    cmd.add_argument('-n', '--nysm',
                     required=True, type=int, default=2, help="RS code")
    cmd.add_argument('-m', '--max-memory',
                     required=True, type=int, metavar='int',
                     help='Value for working memory of the decoder,'
                          ' see RFC6330 or libRaptorQ code/docs for more information.'
                          ' Raise it if encoding fails to produce valid (decodable) data.'
                          ' Must be specified manually.')

    cmd.add_argument('-n', '--repair-symbols-rate',
                     required=True, type=float, metavar='float',
                     help='Fraction of extra symbols to generate above what is required'
                          ' to reassemble to file as a fraction of that "required" count.'
                          ' For example, if 100 symbols are required, "-n 0.5" will generate 150 symbols.'
                          ' Must be specified manually.')

    cmd.add_argument('-d', '--drop-rate',
                     default=0, type=float, metavar='0-1.0',
                     help='Drop specified randomly-picked fraction'
                          ' of symbols encoded for each block (incl. ones for repair).'
                          ' I.e. just discard these right after encoding. Mainly useful for testing.')

    cmd = cmds.add_parser('decode', help='Decode lines of base64 into a file.')
    cmd.add_argument('path_src', nargs='?',
                     help='Path to a file with JSON structure, such as produced by "encode" operation.'
                          ' Stdin will be used, if not specified.')
    cmd.add_argument('path_dst', nargs='?',
                     help='Path to write assembled file to. Will be dumped to stdout, if not specified.')

    opts = parser.parse_args(sys.argv[1:] if args is None else args)

    src = sys.stdin if not opts.path_src else open(opts.path_src, 'rb')
    try:
        data = src.read()
    finally:
        src.close()

    try:
        if opts.cmd == 'encode':
            if not opts.subsymbol_size:
                opts.subsymbol_size = opts.symbol_size
            try:
                _opts = {"subsymbol_size": opts.subsymbol_size, "symbol_size": opts.symbol_size,
                         "max_memory": opts.max_memory, "no_precompute": opts.no_precompute, "threads": opts.threads,
                         "repair_symbols_rate": opts.repair_symbols_rate, "drop_rate": opts.drop_rate}
                data = encode(_opts, data)
                dna_str = EncoderToDNA(data, opts.symbol_size, opts.nysm)
                data["symbols"] = dna_str
                data["rs"] = opts.nysm
                data = json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))
            except RQError as err:
                raise EncDecFailure(str(err))

        elif opts.cmd == 'decode':
            data = json.loads(data)
            dna_length = data["symbol_size"] + data[
                "rs"] + 12  # here, 12 is hard-coded when file is small, otherwise, 24 will be OK
            _symbol = DNAToDecoder(data["symbols"], dna_length, data["rs"], data["symbol_size"])
            data["symbols"] = _symbol
            data = decode(opts, data)
        else:
            raise NotImplementedError(opts.cmd)
    except EncDecFailure as err:
        log.error('Operation failed - %s', err)
        return 1

    if data is not None:
        dst = sys.stdout if not opts.path_dst else open(opts.path_dst, 'wb')
        try:
            dst.write(data)
        finally:
            dst.close()
