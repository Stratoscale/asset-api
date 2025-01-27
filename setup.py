from setuptools import setup, find_packages
from setuptools_plugins.version import get_version

setup(
    name="asset_client",
    author="Zadara",
    description="Zadara rack server assets ",
    keywords=["asset"],
    author_email="Engineering-DevOps+asset_api@zadarastorage.com ",
    long_description="""API client for Zadara asset management""",
    url="https://github.com/Stratoscale/asset-api",
    package_dir={"": "py"},
    packages=find_packages(where="py"),
    version=get_version(),
    include_package_data=False,
)

