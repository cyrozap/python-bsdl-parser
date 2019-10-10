bsdl.py: bsdl.ebnf
	grako --name bsdl -o $@ $^

package:
	touch __init__.py

clean:
	rm bsdl.py __init__.py
