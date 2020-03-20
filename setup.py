import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='kac',
    version='0.2.3',
    author="Adam Walsh",
    author_email="adam@grid.sh",
    description="A command line tool for CHANGELOG files that follow the Keep-a-Changelog standard.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atwalsh/kac",
    packages=setuptools.find_packages(),
    install_requires=[
        'click==7.0',
        'pyperclip==1.7.0',
        'questionary==1.4.0'
    ],
    entry_points='''
        [console_scripts]
        kac=kac.kac:cli
    ''',
    python_requires='>=3.6',
)
