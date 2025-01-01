from setuptools import setup, find_packages

setup(
    name='mpesa_sdk',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    description='MPesa SDK for interacting with Safaricom APIs',
    author='Samuel Ephrem',
    author_email='samuelephrem2012@gmail.com',
)
