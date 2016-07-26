all: check_convention

check_convention:
	pep8 asset --max-line-length=109
