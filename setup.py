from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name="hg",
    version='0.2.0',
    description='',
    long_description=readme,
    packages=['hg'],
    url='https://github.com/neriberto/hg',
    license='BSD 3-Clause License',
    author='Neriberto C. Prado',
    author_email='neriberto@gmail.com',
    dependency_links=[
        'git+https://github.com/neriberto/malwarefeeds.git@develop#egg=malwarefeeds'
    ],
    install_requires=[
        "click==7.0",
        "requests==2.22.0",
        'malwarefeeds',
    ],
    entry_points={
        "console_scripts": [
            "hg=hg:cli"
        ],
    },
    zip_safe=False,
)
