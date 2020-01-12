import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="calendrical_tools",
    version="0.0.1",
    author="Ray Nowell",
    author_email="ray.nowell@gmail.com",
    description="Minimal package for calendar calculations using code from Reingold & Dershowitz.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rn123/Calendrial-Tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
