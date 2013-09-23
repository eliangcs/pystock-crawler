try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='stockcrawler',
    version='0.0.1',
    url = 'http://github.com/eliangcs/stockcrawler/',
    description='Crawl stock historical data.',
    long_description=open('README.rst').read(),
    author='Chang-Hung Liang',
    author_email='eliang.cs@gmail.com',
    license='MIT',
    packages=['stockcrawler'],
)
