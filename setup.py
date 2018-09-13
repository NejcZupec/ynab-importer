from setuptools import setup

setup(
    name='ynab-importer',
    description='Importer for YNAB budgeting software',
    author='Nejc Zupec',
    author_email='zupec.nejc@gmail.com',
    url='https://github.com/NejcZupec/ynab-importer',
    version='0.1',
    py_modules=[],
    install_requires=[
        'click',
        'n26',
        'pyyaml',
    ],
    packages=[],
    scripts=[],
    entry_points="""
    [console_scripts]
    ynab_importer=cli:cli
    """,
    python_requires='~=3.5',
)
