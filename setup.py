from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='hospitaler',
    packages=find_packages(),
    install_requires=required,
    use_scm_version=True,
    setup_requires=[
        "setuptools_scm>=1.10.1,<2.0.0",
    ],
)