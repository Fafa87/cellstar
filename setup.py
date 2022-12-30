import sys
import setuptools

if sys.version_info[0] == 2:
    numpy_version = "numpy>=1.16"
    scipy_version = "scipy>=1.2.3"
else:
    numpy_version = "numpy>=1.17"
    scipy_version = "scipy>=1.5.3"

with open("README.rst") as f:
    long_description = f.read()


class Test(setuptools.Command):
    user_options = [
        ("pytest-args=", "a", "arguments to pass to py.test")
    ]

    def initialize_options(self):
        self.pytest_args = []

    def finalize_options(self):
        pass

    def run(self):
        import pytest
        errno = pytest.main(self.pytest_args + ['--ignore', 'utils/'])
        sys.exit(errno)


setuptools.setup(
    author="Filip Mroz",
    author_email="fafafft@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering"
    ],
    cmdclass={
        "test": Test
    },
    include_package_data=True,
    install_requires=[
        numpy_version,
        scipy_version,
        "pillow<=6.2.2",
        "matplotlib<=2.2.5",
        "imageio<=2.6.1",
        "pathlib"
    ],
    keywords=["brightfield", "yeast", "segmentation", "adapting"],
    license="BSD",
    long_description=long_description,
    name="CellStar",
    description="Algorithm for round cells identification in the brightfield microscopy images.",
    packages=setuptools.find_packages(exclude=[
        "tests", "utils"
    ]),
    setup_requires=[
        "pytest"
    ],
    url="https://github.com/Fafa87/cellstar",
    version="2.0.1"
)
