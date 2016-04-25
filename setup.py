import setuptools

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

        errno = pytest.main(self.pytest_args)

        sys.exit(errno)

setuptools.setup(
        author="",
        author_email="",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: C",
            "Programming Language :: C++",
            "Programming Language :: Cython",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Topic :: Scientific/Engineering :: Bio-Informatics",
            "Topic :: Scientific/Engineering :: Image Recognition",
            "Topic :: Scientific/Engineering"
        ],
        cmdclass={
            "test": Test
        },
        description="",
        include_package_data=True,
        install_requires=[
            "matplotlib",
            "numpy",
            "scipy"
        ],
        keywords="",
        license="BSD",
        long_description="",
        name="CellStar",
        packages=setuptools.find_packages(exclude=[
            "tests"
        ]),
        setup_requires=[
            "pytest"
        ],
        url="https://github.com/CellProfiler/cellstar",
        version="1.0.0rc1"
)
