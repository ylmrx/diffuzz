from setuptools import setup

setup(
    name='DifFuzz',
    version='0.0.1',
    py_modules=['diffuzz'],
    install_requires=[
        'deepdiff',
        'click',
        'termcolor'
    ],
    entry_points='''
        [console_scripts]
        diffuzz=diffuzz:main
    ''',
    author='Yoann Lamouroux',
    author_email='yla@nbs-system.com'
)
