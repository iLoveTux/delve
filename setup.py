import sys
from setuptools import setup

tests_require = ["nose>=1.0"]
if sys.version_info < (3,0):
    tests_require = ["nose>=1.0", "mock"]

setup(
    name="delve",
    version="0.1.0",
    author="iLoveTux",
    author_email="cliffordbressette@gmail.com",
    description="delve into your data, Now!",
    license="GPLv3",
    keywords="utility tools data pandas pony",
    url="http://github.com/ilovetux/delve",
    packages=['delve'],
    install_requires=["colorama"],
    entry_points={
        "console_scripts": [
            "delve=delve.__main__:cli",
        ]
    },
    test_suite="nose.collector",
    tests_require=tests_require,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
