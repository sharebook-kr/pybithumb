from setuptools import setup

setup(
    name            = 'pybithumb',
    version         = '1.0.19',
    description     = 'python wrapper for Bithumb API',
    url             = 'https://github.com/sharebook-kr/pybithumb',
    author          = 'Lukas Yoo, Brayden Jo',
    author_email    = 'jonghun.yoo@outlook.com, pystock@outlook.com',
    install_requires=['requests', 'pandas', 'bs4', 'html5lib', 'datetime', 'websockets'],
    license         = 'MIT',
    packages        = ['pybithumb'],
    zip_safe        = False
)