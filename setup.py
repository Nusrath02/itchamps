from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# Filter out comments and empty lines
install_requires = [r.strip() for r in install_requires if r.strip() and not r.startswith("#")]

setup(
    name="itchamps",
    version="0.0.1",
    description="ITChamps HR Management with AI Chatbot",
    author="ITChamps",
    author_email="info@itchamps.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
