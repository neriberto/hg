from setuptools import setup

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements


links = []
requires = []

req_file = 'requirements.txt'
requirements = parse_requirements(req_file, session=False)

for item in requirements:
    print(item)
    if getattr(item, 'url', None):
        links.append(str(item.url))
    if getattr(item, 'link', None):
        links.append(str(item.link))
    if item.req:
        requires.append(str(item.req))

print(requires)
print(links)
setup(
    name="hg",
    version='0.1',
    py_modules=['app'],
    install_requires=requires,
    entry_points='''
        [console_scripts]
        hg=app:cli
    ''',
    dependency_links=links,
    zip_safe=False,
)
