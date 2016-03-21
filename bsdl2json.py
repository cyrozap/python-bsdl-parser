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
import re
import sys


class BsdlFile:
    def __init__(self, bsdl_file):
        self.bsdl_file = bsdl_file
        self.entity = ""
        self.package = ""
        self.port_desc = {}
        self.pin_map = {}

    def parse(self):
        file_lines = open(self.bsdl_file, 'r').readlines()
        i = 0
        while i < len(file_lines):
            line = file_lines[i].strip('\n').strip('\r')
            compare_line = line.strip().lower()
            if compare_line.startswith("entity"):
                regex = re.compile('[a-zA-Z]+\s+(.*)\s+[a-zA-Z]+')
                self.entity = regex.search(line).group(1)
                i += 1
            elif compare_line.startswith("generic"):
                end = False
                while not end:
                    line = file_lines[i].strip('\n').strip('\r')
                    line = line.strip()
                    if "--" in line:
                        line = line.split("--")[0].strip()
                    if "PHYSICAL_PIN_MAP" in line:
                        regex = re.compile('\"(.*)\"')
                        self.package = regex.search(line).group(1)
                    if ");" in line:
                        end = True
                    i += 1
            elif compare_line.startswith("port"):
                end = False
                while not end:
                    line = file_lines[i].strip('\n').strip('\r')
                    line = line.strip()
                    if "--" in line:
                        line = line.split("--")[0].strip()
                    if ":" in line:
                        split_line = line.split(":")
                        pin_id = split_line[0]
                        pin_type = split_line[1].strip().rstrip(";")
                        if pin_id:
                            if pin_type.endswith("bit") and "linkage" not in pin_type:
                                self.port_desc[pin_id] = pin_type.split()[0]
                    if line.startswith(");"):
                        end = True
                    i += 1
            elif len(self.package) > 0 and compare_line.startswith("constant"):
                pin_map_string = ""
                end = False
                while not end:
                    line = file_lines[i].strip('\n').strip('\r')
                    line = line.strip()
                    if "--" in line:
                        line = line.split("--")[0].strip()
                    if "\"" in line:
                        pin_map_string += line.rstrip("&").strip().replace("\"","")
                    if line.endswith(";"):
                        pin_map_list = pin_map_string.split(",")
                        current_signal = None
                        for item in pin_map_list:
                            if ":" in item:
                                split_item = item.split(":")
                                signal = split_item[0].strip()
                                pin_name = split_item[1].strip()
                                if "(" in pin_name:
                                    current_signal = signal
                                    pin_name = pin_name.lstrip("(")
                                self.pin_map[pin_name] = signal
                            else:
                                if ")" in item:
                                    item = item.rstrip(")")
                                self.pin_map[item] = current_signal
                        end = True
                    i += 1
            else:
                i += 1

    def __str__(self):
        dictionary = {
            "entity": self.entity,
            "package": self.package,
            "port_desc": self.port_desc,
            "pin_map": self.pin_map,
        }
        return json.dumps(dictionary)


if __name__ == "__main__":
    bsdl = BsdlFile(sys.argv[1])
    bsdl.parse()
    print(bsdl)
