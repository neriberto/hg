from setuptools import setup

setup(
    name="hg",
    version='0.1',
    py_modules=['app'],
    install_requires=[
        "asyncio==3.4.3",
        "requests==2.19.1",
        ],
    entry_points='''
        [console_scripts]
        hg=app:cli
    ''',
    dependency_links=[
        "git+https://github.com/neriberto/malwarefeeds"
        ],
)
