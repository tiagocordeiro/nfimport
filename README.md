# NFI

[![Build Status](https://travis-ci.org/tiagocordeiro/nfimport.svg?branch=master)](https://travis-ci.org/tiagocordeiro/nfimport)
[![Updates](https://pyup.io/repos/github/tiagocordeiro/nfimport/shield.svg)](https://pyup.io/repos/github/tiagocordeiro/nfimport/)
[![Python 3](https://pyup.io/repos/github/tiagocordeiro/nfimport/python-3-shield.svg)](https://pyup.io/repos/github/tiagocordeiro/nfimport/)
[![codecov](https://codecov.io/gh/tiagocordeiro/nfimport/branch/master/graph/badge.svg)](https://codecov.io/gh/tiagocordeiro/nfimport)

## Como rodar o projeto:

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://github.com/tiagocordeiro/nfimport.git
cd nfimport
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
```

## Como rodar os testes:

```
pycodestyle .
flake8 .
python manage.py test -v 2
```

### Cobertura de testes:

```
coverage run --source='.' manage.py test -v 2
coverage report -m
```
