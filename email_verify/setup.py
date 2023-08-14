from setuptools import setup, find_packages

setup(
    name='email_verify',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'itsdangerous>=2.1.2',
    ],
)