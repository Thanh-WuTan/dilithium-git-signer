from setuptools import setup, find_packages

setup(
    packages=find_packages(where=".", include=["src*"]),
    package_data={
        "src": ["LICENSE"],
    },
)