from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hiws",
    version="0.2.1",
    author="Tomas Santana",
    author_email="tomas@cervant.chat",
    description="A simple Python wrapper for WhatsApp's Cloud API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cervant-ai/hiws",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pydantic>=2.11.7",
        "httpx>=0.28.1",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.23",
            "black>=21.0",
            "flake8>=3.8.0",
            "mypy>=0.800",
        ],
    },
)
