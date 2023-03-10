from setuptools import setup, find_packages

setup(
    name='myproject',
    version='0.1.0',
    description='My tool for searching unsigned first good issue',
    author='Evgenii',
    author_email='ev.ustinov03@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'myproject=issueMonitoringTool.cli:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)