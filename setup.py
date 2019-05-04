from setuptools import setup, find_packages

requirements = [
    'pytest',
    'astor',
]

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='pytest-ast-transformer',
    version='1.0.3',
    packages=find_packages(exclude=['examples', 'tests']),
    entry_points={
        "pytest11": ["pytest_ast_transformer = pytest_ast_transformer.plugin"],
    },
    install_requires=requirements,
    long_description=readme,
    author='okorolev',
    author_email='johnnyprobel@gmail.com',
    url='https://github.com/okorolev/pytest-ast-transformer',
    keywords=['pytest', 'ast', 'transformer', 'refactoring', 'testing', 'debug'],
    classifiers=[
        'Framework :: Pytest',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
    ],
    tests_require=['pytest-mock'],
    setup_requires=['pytest-runner'],
)
