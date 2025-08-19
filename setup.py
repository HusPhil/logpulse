from setuptools import setup, find_packages

setup(
    name="logtracker",
    version="1.0.0",
    packages=find_packages(),
    package_data={
        "": ["*.ico", "*.md"],
    },
    include_package_data=True,
    install_requires=[
        "Pillow",
        "pystray",
    ],
    entry_points={
        "console_scripts": [
            "logtracker=logtracker.main:main",
        ],
    },
    author="Your Name",
    description="A simple activity logging application",
    python_requires=">=3.7",
)