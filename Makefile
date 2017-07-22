readme:
	kamidana -a kamidana.additionals.reader misc/readme.j2 | sed 's@${HOME}@$$HOME@g' > README.rst
