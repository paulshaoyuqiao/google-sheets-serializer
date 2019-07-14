import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="gserializer",
    version="1.0.6",
    description="Retrieve and serialize a google sheet into tabular data object for easier list and array manipulations",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/paulshaoyuqiao/google-sheets-serializer",
    author="Paul Shao",
    author_email="paulshaoyuqiao1@berkeley.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["google-api-python-client", "google-auth-httplib2", "google-auth-httplib2"]
)