# Change the content according to your package.
import setuptools
import re

# Extract the version from the init file.
VERSION_FILE = "wantedposter/__init__.py"
getversion = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", open(VERSION_FILE, "rt").read(), re.M)
if getversion:
    new_version = getversion.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSION_FILE,))

# Configurations
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    install_requires=['Pillow', 'unidecode'],  # Dependencies
    python_requires='>=3',  # Minimum Python version
    name='one-piece-wanted-poster',  # Package name
    version=new_version,  # Version
    author="Nickelza",  # Author name
    author_email="nickjones7490@gmail.com",  # Author mail
    description="Python package generating One Piece Wanted Posters.",  # Short package description
    long_description=long_description,  # Long package description
    long_description_content_type="text/markdown",
    url="https://github.com/Nickelza/one-piece-wanted-poster",  # Url to your Git Repo
    download_url='https://github.com/Nickelza/one-piece-wanted-poster/archive/' + new_version + '.tar.gz',
    packages=setuptools.find_packages(),  # Searches throughout all dirs for files to include
    include_package_data=True,  # Must be true to include files depicted in MANIFEST.in
    license_files=["LICENSE"],  # License file
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
