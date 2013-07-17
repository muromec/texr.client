from setuptools import setup

setup(
    name='texr.client',
    version='0.6.0',
    url='https://github.com/muromec/texr.client',
    license="BSD",
    author='Ilya Petrov',
    author_email='ilya.muromec@gmail.com',
    install_requires=[
        'msgpack-python',
    ],
    packages=[
        'texr', 'texr.client',
    ],
    platforms='any',
    entry_points={
        'console_scripts': [
            'texr-daemon = texr.client.command:main',
        ],
    },
)
