from setuptools import setup

setup(
    name            = 'pybithumb',
    version         = '0.1.28',
    description     = 'python wrapper for Bithumb API',
    url             = 'https://github.com/sharebook-kr/pybithumb',
    author          = 'Lukas Yoo, Brayden Jo',
    author_email    = 'jonghun.yoo@outlook.com, pystock@outlook.com',
    install_requires=['requests'],
    license         = 'MIT',
    packages        = ['pybithumb'],
    zip_safe        = False
)