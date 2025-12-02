from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="itchamps",
    version="0.0.1",
    author="ITChamps",
    author_email="info@itchamps.com",
    description="ITChamps HR Management with AI Chatbot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nusrath02/itchamps",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
    install_requires=[
        "frappe",
    ],
    include_package_data=True,
    zip_safe=False,
)
