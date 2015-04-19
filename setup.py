__author__ = 'moshebasanchig'

from setuptools import setup, find_packages
from pip.req import parse_requirements


VERSION = '0.1.1'

requirements = [str(ir.req) for ir in parse_requirements('requirements.txt')]

setup(
    name='Hydro',
    version=VERSION,
    packages=find_packages(where='src', exclude=('sample', 'test')),
    description='On-the-fly data manipulation framework',
    author='Convertro',
    author_email='moshe.basanchig@convertro.com',
    url='https://github.com/Convertro/Hydro',
    download_url='https://github.com/Convertro/Hydro/tarball/0.1',
    package_dir={'': 'src'},
    install_requires=requirements,
    test_suite="nose.collector",
    tests_require="nose",
    entry_points={
        'console_scripts': [
            'hydro_cli = hydro.hydro_cli:main'
        ]
    },
    package_data={
        '': ['hydro/template/*.template']
    },
    include_package_data=True
)
