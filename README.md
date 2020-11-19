# python-bsdl-parser

This is a [Grako][Grako]-based parser for IEEE 1149.1 Boundary-Scan Description
Language (BSDL) files.

## Install

pip install bsdl-parser

## Usage

`bsdl2json bsdl_file.bsd > json_file.json` to convert your BSDL file to JSON.

Note: Installer will place the executable in `<python-folder>/bin/bsdl2json`

## Build

```sh
# Install build requirements
python -m pip install ".[build]"
# Build grako
cd bsdl_parser && make && cd ..
# Build wheel
python setup.py sdist bdist_wheel
# upload to Pypi
twine upload dist/*
```

[Grako]: https://pypi.python.org/pypi/grako