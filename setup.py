from setuptools import setup, find_packages

setup(
    name="dilithium-git-signer",
    version="0.1.0",
    description="A CLI tool to sign and verify Git commits with Dilithium",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Thanh-WuTan",
    author_email="wt.vathanh@gmail.com",
    url="https://github.com/Thanh-WuTan/dilithium-git-signer",
    license="MIT",
    packages=find_packages(where=".", include=["src*"]),
    package_data={
        "src": ["LICENSE"],
    },
    install_requires=[
        "dilithium-py",
        "click",
        "pycryptodome",
    ],
    entry_points={
        "console_scripts": [
            "dilithium-signer=src.cli:cli",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)