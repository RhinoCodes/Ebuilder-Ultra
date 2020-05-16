import pathlib
from setuptools import setup

README = ("/home/runner/README.md").read_text()

# This call to setup() does all the work
setup(
    name="Ebuilder-Ultra",
    version="0.8.0",
    description="A new web framework, there will be integration with the Ebuilder static site generator in version 1.0",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/RhinoCodes/Ebuilder-Ultra",
    author="Will Forbserg",
    author_email="forsbergw82@gmail.com",
    license="GNU GPLv3",
    classifiers=[
        "License :: GNU GPL v3",
        "Programming Language :: Python :: 3",
    ],
    packages=["ultra"],
    include_package_data=True,
    install_requires=["webob", "requests"],
)
