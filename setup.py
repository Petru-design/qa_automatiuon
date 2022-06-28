from setuptools import setup

setup(
    name='mypkg-tests',
    version='0.1',
    install_requires=[
        "imageio==2.19.2",
        "jarowinkler==1.0.2",
        "networkx==2.8.2",
        "numpy==1.22.4",
        "opencv-python==4.5.5.64",
        "openpyxl==3.0.10",
        "packaging==21.3",
        "Pillow==9.1.1",
        "PyPDF2==1.28.2",
        "pyparsing==3.0.9",
        "python-docx==0.8.11",
        "python-pptx==0.6.21",
        "PyWavelets==1.3.0",
        "rapidfuzz==2.0.11",
        "scikit-image==0.19.2",
        "scipy==1.8.1",
        "tifffile==2022.5.4",
        "toml==0.10.2",
    ],
    packages=['stiEF_tests'],
    package_data={'stiEF_tests': ['tests/*', 'tests/**/*']},
)