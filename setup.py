import json

from setuptools import find_packages, setup

manifest = json.load(open("caption/manifest.json", "r"))
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
setup(
    name=manifest["name"],
    version=manifest["version"],
    author=manifest["author"],
    description=manifest["description"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=manifest["url"],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": [
            "manifest.json",
        ]
    },
    install_requires=[
        "transformers>=4.39.2",
        "torch>=2.2.2",
        "pyexiv2",
        "tqdm",
        "termcolor",
        "Pillow",
    ],
    entry_points={
        "console_scripts": [
            "caption = caption.cli_main:main",
        ],
    },
    python_requires=">=3.9",
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Environment :: GPU :: NVIDIA CUDA",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Graphics",
    ],
)
