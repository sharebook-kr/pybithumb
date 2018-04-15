from setuptools import setup

setup(
    name            = 'pybithumb',
    version         = '0.0.1',
    description     = 'python wrapper for Bithumb API',
    url             = 'https://github.com/sharebook/pybithumb',
    author          = 'Lukas Yoo, Brayden Jo',
    author_email    = 'mmyjh86@gmail.com, pystock@outlook.com',
    install_requires=['requests', 'pandas'],
    license         = 'MIT',
    packages        = ['pybithumb'],
    zip_safe        = False
)