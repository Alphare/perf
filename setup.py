from pathlib import Path
from setuptools import setup

current_dir = Path(__file__).parent.resolve()

with open(current_dir / "README.md", encoding="utf-8") as f:
    long_description = f.read()
    
setup(
    name="perf",
    description="Time your functions and expressions with a great interface",
    version="0.1.1",
    author="btaskaya",
    author_email="batuhanosmantaskaya@gmail.com",
    packages=["perf"],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url="https://github.com/isidentical/perf"
)
