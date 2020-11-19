#!/usr/bin/env python3
#
# python-bsdl-parser
#
# Copyright (c) 2016, Forest Crossman <cyrozap@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#


import json
import sys
import os
import argparse
import glob

import bsdl_parser.bsdl as bsdl


class BsdlSemantics:
    def map_string(self, ast):
        parser = bsdl.bsdlParser()
        ast = parser.parse(''.join(ast), "port_map")
        return ast

    def grouped_port_identification(self, ast):
        parser = bsdl.bsdlParser()
        ast = parser.parse(''.join(ast), "group_table")
        return ast

def bsdl2json(filename, outfilename=None):
    with open(filename) as f:
        text = f.read()
        parser = bsdl.bsdlParser()
        ast = parser.parse(text, "bsdl_description", semantics=BsdlSemantics(), parseinfo=False)
        if outfilename is None:
            print(json.dumps(ast.asjson()))
        else:
            with open(outfilename, 'w') as outfile:
                json.dump(ast.asjson(), outfile)

def main():
    # Based on: https://gist.github.com/89465127/5273149
    parser = argparse.ArgumentParser(description='Parse bsdl files to json format.')
    parser.add_argument('path', nargs='+', help='Path of a file or a folder of BSDL files.')
    parser.add_argument('-e', '--extension', default='bsd',
        help='File extension to filter by. (default=bsd)')
    parser.add_argument('-o', '--out-path', default=None,
        help='''Path of the parsed files. bsdl2json will print the parsed content to stdout if
        out-path is not spectified.''')
    args = parser.parse_args()
    
    # Parse paths
    full_paths = [os.path.join(os.getcwd(), path) for path in args.path]
    files = set()
    for path in full_paths:
        if os.path.isfile(path):
            files.add(path)
        else:
            files |= set(glob.glob(path + '/*' + args.extension))

    outpath = args.out_path

    if outpath is None:
        # Do not print information, it will disturb the printed, parsed data
        verbose = False
    else:
        verbose = True

    # Check if there is any valid input file
    if not files:
        print(f'ERROR: No BSDL files found at {args.path}')
        sys.exit(-1)

    # If we want to store the parsed content into a file...
    if outpath is not None:
        if len(files)>1:
            # If there are multiple input files, we need the output path as directory
            if not os.path.isdir(outpath):
                print(f'ERROR: Please give a directory as output-path.')
                sys.exit(-1)


    for f in files:
        outname = outpath
        if outpath is not None:
            bname = os.path.basename(f)
            if os.path.isdir(outpath):
                outname = os.path.join(outpath, f'{bname}.json')
        if verbose:
            print(f'Processing {f} -> {outname} ...')
        bsdl2json(f, outname)

if __name__ == "__main__":
    main()
