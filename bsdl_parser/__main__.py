import os
import sys
import argparse

import bsdl_parser.bsdl2json
import bsdl_parser.bsdl_attributes

sub_prog = sys.argv[1] 
del sys.argv[1] 
if sub_prog == 'bsdl2json':
    bsdl_parser.bsdl2json.main()
if sub_prog == 'bsdl_attributes':
    bsdl_parser.bsdl_attributes.main()
