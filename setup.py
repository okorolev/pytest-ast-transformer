from setuptools import setup

PACKAGE = 'pytest-ast-transformer'

requirements = [
    'pytest',
    'astor'
]

setup(
    name=PACKAGE,
    version='1.0.0',
    packages=['pytest_ast_transformer'],
    entry_points={
        "pytest11": ["pytest_ast_transformer = pytest_ast_transformer.plugin"],
    },
    install_requires=requirements,
    author='okorolev',
    url='https://github.com/okorolev/pytest-ast-transformer',
    author_email='johnnyprobel@gmail.com',
    keywords=['pytest', 'ast', 'transformer', 'refactoring', 'testing', 'debug'],
    classifiers=[
        'Framework :: Pytest',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
    ],
)
