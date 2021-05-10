import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="transferwise-python-sdk",
    version="0.0.2",
    author="David Vartanian",
    author_email="davidvartanian@posteo.de",
    description="A light TransferWise SDK for Python",
    license="gpl-3.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davidvartanian/transferwise-python-sdk",
    download_url="https://github.com/davidvartanian/transferwise-python-sdk/archive/v0.0.2.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=open("requirements.txt", "r").read().splitlines(),
    python_requires=">=3.6",
)
