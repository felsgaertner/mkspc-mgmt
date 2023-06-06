from setuptools import setup, find_packages

with open('README.md') as fp:
    longdesc = fp.read()

setup(
    name='mkspc-mgmt',
    version='0.9.0',
    author='OWBA',
    description='User management for makerspaces',
    long_description=longdesc,
    long_description_content_type="text/markdown",
    url='https://github.com/owba/mkspc-mgmt',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    packages=find_packages(),
    scripts=['manage.py'],
    install_requires=[],
)
