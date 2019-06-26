from setuptools import setup, find_packages

setup(
    name='tbcs_rf_wrapper',
    version='0.11',
    packages=find_packages(exclude=['tests']),

    install_requires=[
        'requests',
        'tbcs-api-client',
        'robotframework'
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
