from setuptools import find_packages, setup

setup(
    name="dissect.thumbcache",
    packages=list(map(lambda v: "dissect." + v, find_packages("dissect"))),
    install_requires=[
        "dissect.cstruct>=3.0.dev,<4.0.dev",
        "dissect.util>=3.0.dev,<4.0.dev",
    ],
    entry_points={
        "console_scripts": [
            "thumbcache-extract=dissect.thumbcache.tools.extract_images:main",
            "thumbcache-extract-indexed=dissect.thumbcache.tools.extract_with_index:main",
        ]
    },
)
