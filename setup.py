"""
Installs local packages into local environment.
"""

from setuptools import find_packages, setup

setup(
    name = "mcq_project",
    version = "0.0.1",
    author = "Caner Karaoglu",
    author_email = "caner_karaoglu@hotmail.com",
    install_requires = ["openai", "langchain", "streamlit", "python-dotenv", "PyPDF2"],
    packages=find_packages()
)