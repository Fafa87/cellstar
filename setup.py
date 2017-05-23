import setuptools

setuptools.setup(
        author="Filip Mroz",
        author_email="fafafft@gmail.com",
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
        description="",
        include_package_data=True,
        install_requires=[
            "numpy==1.12.0",
            "scipy==0.19.0",
            "Pillow==4.0.0"
        ],
        keywords="",
        license="BSD",
        long_description="",
        name="CellStar",
        packages=setuptools.find_packages(exclude=[
            "tests", "utils"
        ]),
        setup_requires=[
            "pytest"
        ],
        url="https://github.com/CellProfiler/cellstar",
        version="1.3.0"
)
