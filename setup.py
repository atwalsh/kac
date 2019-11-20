import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='kac',
    version='0.1.3',
    author="Adam Walsh",
    author_email="adam@grid.sh",
    description="Automatic version bumping for Keep-a-Changelog style Changelog files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atwalsh/kac",
    packages=setuptools.find_packages(),
    install_requires=[
        'click==7.0',
        'questionary==1.3.0'
    ],
    entry_points='''
        [console_scripts]
        kac=kac.kac:main
    ''',
    python_requires='>=3.6',
)
