from setuptools import setup

setup(
    name='stiEF_tests',
    version='0.1',
    install_requires=[
        "pytest==7.1.2",
        "numpy==1.22.4",
        "opencv-python==4.5.5.64",
        "openpyxl==3.0.10",
        "PyPDF2==1.28.2",
        "python-docx==0.8.11",
        "python-pptx==0.6.21",
        "rapidfuzz==2.0.11",
        "scikit-image==0.19.2",
        "toml==0.10.2",
        "yargs==0.8.1",
    ],
    packages=['stiEF_tests'],
    package_data={'stiEF_tests': ['tests/*', 'tests/pyfiles/*', 'tests/utils/*']},
    console=['run_stiEF_test.py']
    # py_modules=['conftest']
)