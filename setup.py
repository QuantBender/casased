from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()


setup_args = dict(
    name='casased',
    version='0.1.0',
    description='Python library to retrieve historical and intraday data from Casablanca Stock Exchange',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='ANDAM Amine',
    author_email='andamamine83@gmail.com',
    keywords=["Web scraping","financial data","casablanca"],
    url='https://github.com/QuantBender/casased',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

install_requires = ['requests','beautifulsoup4','pandas','lxml']

