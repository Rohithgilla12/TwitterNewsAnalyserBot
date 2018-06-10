import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="News_Comparer",
    version="0.0.1",
    author="Rohith Gilla",
    author_email="gillarohith1@gmail.com",
    description="News comparison bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rohithgilla12/TwitterNewsAnalyserBot",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)