import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="izmon-class",
    version="1.00",
    author="akita-yohei",
    author_email="akita.yohei0724@gmail.com",
    license='MIT',
    description="You can play 'izmon' with this class",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akita0724/izmon",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
)
