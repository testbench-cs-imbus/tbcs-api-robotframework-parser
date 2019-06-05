from setuptools import setup, find_packages

setup(
    name='tbcs_rf_wrapper',
    version='0.1',
    packages=find_packages(),

    install_requires=[],

    description="Wrapper to be used in Robot Framework in order to integrate your tests with "
                "TestBench CS through the REST API.",
    license="PSF",
    keywords="testbench tbcs testautomation robot robotframework",
    url="https://testbench.com"
)
