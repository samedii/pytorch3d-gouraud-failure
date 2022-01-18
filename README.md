# pytorch3d reproducing gouraud shader failure

## Install

### Frozen requirements if you don't use poetry

See requirements.txt

### Install with poetry

You should have nvcc version 11.1 installed. Other versions should work but
they need to match the version you are using with pytorch.
```
nvcc --version
```

Install pyenv and use python 3.8.8
```
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
pyenv install 3.8.8
```

Install poetry
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

Install requirements
```
poetry install
```

Override pytorch requirements to use corrent CUDA version (11.1):
```
poetry run python -m pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
```
_Note that every time you add a dependency in pytorch then you need to reinstall the torch packages._

NVIDIA CUB requirement for CUDA 11.1
```
curl -LO https://github.com/NVIDIA/cub/archive/1.9.10-1.tar.gz
tar -xvzf 1.9.10-1.tar.gz
export CUB_HOME=$PWD/cub-1.9.10-1
```
_See https://github.com/NVIDIA/cub for what version to use with what CUDA version._

Install from git
```
poetry run python -m pip install git+https://github.com/facebookresearch/pytorch3d.git@v0.6.1
```
