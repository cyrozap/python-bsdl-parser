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

import std_1149_1_2013


class BsdlSemantics:
    def map_string(self, ast):
        parser = std_1149_1_2013.std_1149_1_2013Parser()
        ast = parser.parse(''.join(ast), "port_map")
        return ast

def main(filename):
    with open(filename) as f:
        text = f.read()
        parser = std_1149_1_2013.std_1149_1_2013Parser()
        ast = parser.parse(text, "bsdl_description", semantics=BsdlSemantics())
        print(json.dumps(ast, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
