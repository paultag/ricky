from ricky import __appname__, __version__
from setuptools import setup


long_description = ""

setup(
    name=__appname__,
    version=__version__,
    scripts=[],
    packages=[
        'ricky',
    ],
    author="Paul Tagliamonte",
    author_email="tag@pault.ag",
    long_description=long_description,
    description='You got some \'splainin to do!',
    license="Expat",
    url="http://deb.io/",
    platforms=['any'],
    entry_points={
        'console_scripts': [
            'ricky-forge-changes = ricky.cli:forge_changes',
            'ricky-upload = ricky.cli:upload_package',
        ],
    }
)
