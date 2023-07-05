import os
import subprocess
from setuptools import find_packages, setup


def get_git_revision():
    """Return the git revision."""
    if os.path.exists('PKG-INFO'):
        with open('PKG-INFO') as package_info:
            for key, value in (line.split(':', 1) for line in package_info):
                if key.startswith('Version'):
                    return value.strip()

    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()


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
    version=get_git_revision(),
    include_package_data=False
)