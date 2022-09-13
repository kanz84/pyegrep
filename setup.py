from distutils.core import setup


from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="pyegrep",
    version="1.0.11",
    packages=["pyegrep"],
    url="https://github.com/kanz84/pyegrep",
    license="MIT",
    author="kanz84",
    author_email="kanz1384@gmail.com",
    description="A tool for grep",
    download_url="https://github.com/kanz84/pyegrep/archive/refs/tags/v1.0.11.tar.gz",
    keywords=["grep", "egrep"],
    install_requires=[],
    # long_description_content_type="",
    # long_description_content_type="text/x-rst",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
