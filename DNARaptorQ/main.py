"""
main module
"""
import argparse
from DNARaptorQ.RaptorQ import *


def main(args=None, error_func=None):
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

    global log
    logging.basicConfig(
        format='%(asctime)s :: %(levelname)s :: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG if opts.debug else logging.WARNING)
    log = logging.getLogger()

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
                data = encode(opts, data)
            except RQError as err:
                raise EncDecFailure(str(err))
            data = json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))
        elif opts.cmd == 'decode':
            data = decode(opts, json.loads(data))
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
