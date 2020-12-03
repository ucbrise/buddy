import setuptools

with open('requirements.txt', 'r') as f:
    requirements = f.read().split('\n')

setuptools.setup(
        name='buddy',
        version='0.0.1',
        description='CALM Programming with Python and SQL',
        url='https://github.com/ucbrise/buddy',
        packages=setuptools.find_packages(),
        install_requires=requirements,
        python_requires='>=3.6',
        )
