from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT = "-e."

def get_requirements(file_path: str)->List[str]:
    requirements = []
    with open(file_path,"r") as f:
        requirements = f.readlines()
        requiremnts = [i.replace("\n","") for i in requirements]
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    





setup(
    name = "Agriculture Project",
    version = "0.1",
    packages = find_packages(),
    author = "Soham",
    author_email = "sohamsawankhanna@gmail.com",
    install_requires = get_requirements('requirements.txt')
)