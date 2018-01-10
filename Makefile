all: build

build:
	python setup.py sdist bdist_wheel --universal

check_convention:
	pep8 py --max-line-length=109

.PHONY: build all
