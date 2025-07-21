#!/usr/bin/env python3
"""
Setup script for Aha! MCP Server
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="aha-mcp-server",
    version="1.0.0",
    author="MCP Server Generator",
    description="A Model Context Protocol server for Aha! product management platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/aha-mcp-server",
    py_modules=["aha_mcp_server"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "aha-mcp-server=aha_mcp_server:main",
        ],
    },
)

