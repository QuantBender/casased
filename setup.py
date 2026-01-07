from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()


setup_args = dict(
    name='casased',
    version='0.1.5',
    description='Python library to retrieve historical and intraday data from Casablanca Stock Exchange via Medias24 API with Cloudflare bypass',
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

# Optional dependencies for bypassing Cloudflare protection
extras_require = {
    'cloudflare': ['nodriver>=0.30', 'seleniumbase>=4.0.0'],
    'browser': ['nodriver>=0.30', 'seleniumbase>=4.0.0'],
}

if __name__ == "__main__":
    # Execute setup when running setup.py directly (support legacy builds)
    setup(**setup_args, install_requires=install_requires, extras_require=extras_require)

