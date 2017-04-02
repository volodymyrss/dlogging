from distutils.core import setup

setup(
        name='dlogging',
        version='1.0',
        py_modules= ['dlogging'],
        package_data     = {
            "": [
                "*.txt",
                "*.md",
                "*.rst",
                "*.py"
                ]
            },
        install_requires=[
        'zmq',
        ],
        license='Creative Commons Attribution-Noncommercial-Share Alike license',
        long_description=open('README.md').read(),
        )
