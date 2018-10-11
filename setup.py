from setuptools import setup

PACKAGE = 'pytest_ast_transformer'

requirements = [
    'pytest',
    'astunparse'
]

setup(
    name=PACKAGE,
    version='1.0.0',
    packages=[PACKAGE],
    entry_points={
        "pytest11": ["pytest_ast_transformer = pytest_ast_transformer.plugin"],
    },
    install_requires=requirements,
    author='okorolev',
    author_email='johnnyprobel@gmail.com',
    keywords=['pytest', 'ast', 'transformer', 'refactoring', 'testing', 'debug'],
    classifiers=[
        "Framework :: Pytest",
    ],
)
