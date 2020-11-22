#!/usr/bin/env python3
#
# fast_bsdl_parser.py 
#
# Based on https://gist.github.com/raczben/88693d22600d743a5ccad797e7374260
#

import os
import sys
import re
import argparse
import glob
import logging

here = os.path.dirname(__file__)

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

def bsdl_attributes(args):
    file_set = set()
    
    if not args.recursive:
        file_set |= set([args.filename])
    else:
        if args.filename is None:
            args.filename = '.'
        for incl in args.include:
            glob_pattern = f'{args.filename}/**/{incl}'
            file_set |= set(filter(os.path.isfile, [f for f in glob.glob(glob_pattern, recursive=True)]))

    logging.info(f'Start procesing {len(file_set)} files.')

    attributes_dict = {}
    for f in file_set:
        logging.info(f'Processing {f} ...')
        attributes_dict[f] = get_bsdl_attributes(f)
        print(attributes_dict[f]['IDCODE_REGISTER'])


def get_bsdl_attributes(filename, verbose=False):

    # Match lines like:
    # attribute INSTRUCTION_LENGTH of corsica: entity is 3;
    pat_attribute = re.compile(r'attribute\s+(\w+)\s+OF\s+\w+\s*:\s+entity\s+is\s+([^;]+);', re.IGNORECASE)

    file_content = ''

    with open(filename) as f:
        file_content = f.read()

    # Remove comments
    file_content = re.sub('--.+$', '', file_content, flags=re.MULTILINE)

    m = re.finditer(pat_attribute, file_content)
    attributes ={}
    for attr in m:
        attr_name = attr.group(1)
        attr_val = attr.group(2)
        # Replace multiline attributes to single line:
        attr_val = re.sub(r'\s*\n\s*', ' ', attr_val)
        # Replace "XXXX" &  "0011100" style strings to "XXXX0011100" 
        attr_val = re.sub(r'"\s*&\s*"', '', attr_val)

        attributes[attr_name] = attr_val

    return attributes


def main():
    parser = argparse.ArgumentParser(
        description='Fast BSDL Parser: https://github.com/cyrozap/python-bsdl-parser is a fully '
        'featured BSDL parser, but it is slow. This Fast BSDL parser parses the attributes fast to '
        'fetch the IDCODE fast from dozen of BSDL files.'
        )
    parser.add_argument('filename', type=str, default=None, nargs="?",
        help='File to read to dump unused signals. Globbing expressions are accepted.',
        )
    parser.add_argument('--recursive', '-r', action='store_true',
        help='Read files recursively.',
        )
    parser.add_argument('--include', type=str, action='append', default=['*bsd', '*bsdl'],
        help='Search only files whose base name matches GLOB',
        )
    parser.add_argument('--verbose', '-v', action='store_true',
        help='Print more information',
        )
    args = parser.parse_args()
    
    
    # Validate arguments:
    if (args.filename is None) and (not args.recursive):
        print('A filename or the --recursive flag must given.')
        parser.print_help()
        sys.exit(-1)

    # Call the main:
    bsdl_attributes(args)

if __name__ == '__main__':
    main()
