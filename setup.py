from setuptools import setup, find_packages

setup(
    name="html-image-scraper",
    version="1.0.0",
    description="A desktop application for extracting and downloading images from HTML content",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/html-image-scraper",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4>=4.9.0",
        "requests>=2.25.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "html-image-scraper=image_scraper:main",
        ],
    },
)