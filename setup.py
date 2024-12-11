from setuptools import setup, find_packages

setup(
    name="PipelineX",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple ETL pipeline tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pipelinex",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer",
        "questionary",
        "pandas",
        "boto3",
        "sqlalchemy",
        "pymongo",
        "pyyaml",
        "python-dotenv",
        "tqdm"
    ],
    entry_points={
        "console_scripts": [
            "pipelinex=pipelinex:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)