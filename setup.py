from setuptools import setup, find_packages

setup(
    name='tbcs_rf_wrapper',
    version='0.16',
    packages=find_packages(exclude=['tests']),

    python_requires='>=3.6',
    install_requires=[
        'requests>=2.22',
        'tbcs-api-client>=0.17',
        'robotframework==3.2.1'
    ],

    entry_points={
        'console_scripts': [
            'robot-parser=test_case_import.__main__:main'
        ]
    },

    description="Wrapper to be used in Robot Framework in order to integrate your tests with "
                "TestBench CS through the REST API.",
    license="PSF",
    keywords="testbench tbcs testautomation robot robotframework",
    url="https://testbench.com"
)
