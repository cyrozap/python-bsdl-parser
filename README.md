# python-bsdl-parser

This is a [Grako][Grako]-based parser for IEEE 1149.1 Boundary-Scan Description
Language (BSDL) files.

> [!CAUTION]
> This project is unmaintained. It worked in the past, but it now has [multiple
> unresolved issues][issues] and does not work with modern versions of Python.
> If you want to parse BSDL files with Python, you'll have to look elsewhere.

## Requirements

* Python 3
* [Grako 3.99.9][Grako]

## Usage

First, install the Grako command from [here][Grako]. Then you can run `make` to
generate the actual parser module (`bsdl.py`).

After generating the parser module, run
`./bsdl2json.py bsdl_file.bsd > json_file.json` to convert your BSDL file to
JSON.


[Grako]: https://pypi.python.org/pypi/grako
[issues]: https://github.com/cyrozap/python-bsdl-parser/issues?q=is%3Aissue%20state%3Aclosed%20reason%3Anot-planned
