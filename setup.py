from ricky import __appname__, __version__
from setuptools import setup


long_description = ""

with open('requirements.txt') as f:
    install_requires = [l for l in f.read().splitlines()
                        if not l.startswith('#')]

setup(
    name=__appname__,
    version=__version__,
    scripts=[],
    packages=[
        'ricky',
    ],
    install_requires=install_requires,
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
