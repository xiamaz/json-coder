.PHONY: build
build:
	python3 setup.py sdist bdist_wheel

clean:
	rm -r build
	rm -r dist

upload:
	twine upload dist/*
