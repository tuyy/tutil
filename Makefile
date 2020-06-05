.PHONY: html pip_install typehint test lint checklist autoformatting upload_py2 upload_py3 py2 py3 clean

TUTIL_VERSION := 0.0.6
PYENV_PYTHON2_VENV := functional2
PYENV_PYTHON3_VENV := functional3

html:
	make -C docs html

pip_install:
	pyenv local $(PYENV_PYTHON3_VENV)
	pip install -r requirements.txt

typehint:
	mypy tutil/ tests/

test:
	tox

lint:
	pycodestyle tutil/ tests/

autoformatting:
	black tutil/ tests/

py2:
	pyenv local $(PYENV_PYTHON2_VENV)

py3:
	pyenv local $(PYENV_PYTHON3_VENV)

clean:
	rm -rf dist

# pypi에 python2 버전으로 업로드
upload_py2: py2
	rm -rf dist
	python setup.py bdist_wheel
	twine upload dist/tutil-$(TUTIL_VERSION)-py2-none-any.whl

# pypi에 python3 버전으로 업로드
upload_py3: py3
	rm -rf dist
	python setup.py bdist_wheel
	twine upload dist/tutil-$(TUTIL_VERSION)-py3-none-any.whl

checklist: lint typehint test autoformatting
