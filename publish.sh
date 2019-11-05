rm -R dist/*
python setup.py sdist
twine upload dist/*