import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='transferwise-python-sdk',
    version='0.0.1',
    author="David Vartanian",
    author_email="davidvartanian@posteo.de",
    description="A light TransferWise SDK for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davidvartanian/transferwise-python-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Crypto",
        "pycrypto",
        "requests",
    ],
    python_requires='>=3.7',
)
