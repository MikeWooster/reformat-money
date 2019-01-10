#!/usr/bin/env python

import setuptools


application_dependencies = []
prod_dependencies = []
test_dependencies = [
    'pytest',
    'pytest-cov',
    'pytest-env',
    'ipdb',
]
lint_dependencies = [
    'flake8',
    'flake8-docstrings',
    'black',
]
deploy_dependenies = [
    'setuptools',
    'wheel',
    'twine',
]
docs_dependencies = []
dev_dependencies = test_dependencies + lint_dependencies + docs_dependencies + deploy_dependenies + []


with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='reformat-money',
    version='0.0.1',
    author='Mike Wooster',
    author_email='',
    description='A script to fix money references within a codebase.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MikeWooster/reformat-money',
    python_requires='>=3.6',
    packages=[
        'reformat_money',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
    ],
    install_requires=application_dependencies,
    extras_require={
        'production': prod_dependencies,
        'test': test_dependencies,
        'lint': lint_dependencies,
        'docs': dev_dependencies,
        'dev': dev_dependencies,
    },
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'reformat-money=reformat_money.__main__:main',
        ]
    },
)
