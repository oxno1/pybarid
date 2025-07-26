from setuptools import setup, find_packages

setup(
    name='pybarid',
    version='0.1.0',
    author='oxno1',
    description='Temporary email client in Python.',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/oxno1/pybarid',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'httpx',
        'requests'
    ],
)
