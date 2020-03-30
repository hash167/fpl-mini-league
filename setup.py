from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()
setup(
    name='fpl',
    version='0.0.1',
    packages=find_packages(),
    description='A python tool for fpl mini leagues',
    long_description=long_description,
    author='hash167',
    author_email='hash167@gmail.com',
    url='https://github.com/hash167/fpl-mini-league',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='fpl mini league',
    install_requires=[
        'Click',
    ],
    include_package_data=False,
    entry_points='''
        [console-scripts]
        fpl-mini-league=src.main.cli
    ''',
)
