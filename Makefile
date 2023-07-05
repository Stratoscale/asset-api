all: check_convention

check_convention:
	python2 -m pep8 py --max-line-length=109

generated-requirements.txt: *.py
	python2 -m pigar -n -p $@ 

