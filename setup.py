try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def parse_requirements(filename):
    with open(filename) as f:
        content = f.read()
    return filter(lambda x: x and not x.startswith('#'), content.splitlines())


setup(
    name='pystock-crawler',
    version='0.0.1',
    url='https://github.com/eliangcs/pystock-crawler',
    description='Crawl stock historical data.',
    long_description=open('README.rst').read(),
    author='Chang-Hung Liang',
    author_email='eliang.cs@gmail.com',
    license='MIT',
    packages=['pystock_crawler'],
    scripts=['bin/pystock-crawler'],
    install_requires=parse_requirements('requirements.txt'),
)
