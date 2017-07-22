from setuptools import setup

setup(
    name='CHDiff',
    version='0.0.1',
    py_modules=['chdiff'],
    install_requires=[
        'deepdiff',
        'click',
        'termcolor'
    ],
    entry_points='''
        [console_scripts]
        chdiff=chdiff:main
    ''',
    author='Yoann Lamouroux',
    author_email='yla@nbs-system.com'
)
