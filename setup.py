# SPDX-License-Identifier: GPL-3.0-or-later
from setuptools import setup, find_packages

setup(
    name="plant_wn",
    version="1.0.0",
    long_description=__doc__,
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "bcrypt",
        "flask",
        "flask-jwt-extended",
        "flask-migrate",
        "flask-sqlalchemy",
        "requests",
    ],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={"console_scripts": ["plant-wn=plan_wn.web.manage:cli"]},
    license="GPLv3+",
    python_requires=">=3.6",
)
