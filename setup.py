"""
Gaming Workforce Observatory - Setup Configuration
Enterprise-grade workforce analytics for the gaming industry
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "docs" / "README.md").read_text(encoding='utf-8')

# Read requirements
def read_requirements(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

requirements = read_requirements('requirements.txt')
dev_requirements = read_requirements('requirements-dev.txt')

setup(
    name="gaming-workforce-observatory",
    version="1.0.0",
    author="Rémi Chenouri",
    author_email="remi.chenouri@example.com",
    description="Enterprise-grade workforce analytics dashboard for the gaming industry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/remichenouri/gaming-workforce-observatory",
    project_urls={
        "Bug Tracker": "https://github.com/remichenouri/gaming-workforce-observatory/issues",
        "Documentation": "https://github.com/remichenouri/gaming-workforce-observatory/blob/main/docs/README.md",
        "Live Demo": "https://gaming-workforce-observatory.streamlit.app",
        "Source Code": "https://github.com/remichenouri/gaming-workforce-observatory",
    },
    packages=find_packages(include=['src', 'src.*']),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Office/Business :: Financial :: Spreadsheet",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Framework :: Streamlit",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "test": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.1",
            "pytest-asyncio>=0.21.1",
        ],
        "docs": [
            "sphinx>=7.1.2",
            "sphinx-rtd-theme>=1.3.0",
            "myst-parser>=2.0.0",
        ],
        "ml": [
            "scikit-learn>=1.3.0",
            "xgboost>=1.7.0",
            "lightgbm>=4.0.0",
        ],
        "cloud": [
            "boto3>=1.28.0",
            "google-cloud-storage>=2.10.0",
            "azure-storage-blob>=12.17.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "gaming-workforce=src.cli:main",
            "gwo-backup=scripts.backup_scripts:main",
            "gwo-health=monitoring.health_check:main",
        ],
    },
    include_package_data=True,
    package_data={
        "src": [
            "data/*.csv",
            "data/*.json",
            "utils/*.css",
            "utils/*.js",
        ],
        "": [
            "config/*.json",
            "config/*.yml",
            "config/*.yaml",
            ".streamlit/*.toml",
        ],
    },
    zip_safe=False,
    keywords=[
        "streamlit",
        "dashboard",
        "analytics",
        "gaming",
        "workforce",
        "hr-analytics",
        "data-visualization",
        "machine-learning",
        "kpi",
        "gaming-industry",
        "people-analytics",
        "performance-metrics",
        "team-analytics",
        "enterprise-dashboard"
    ],
    platforms=["any"],
    license="MIT",
    maintainer="Rémi Chenouri",
    maintainer_email="remi.chenouri@example.com",
)
