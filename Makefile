.PHONY: test

test:
	pytest

README.rst: README.md
	pandoc --from=markdown --to=rst $< > $@
