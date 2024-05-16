from setuptools import setup, find_packages

setup(name='WVRENV',
      version='1.0.0',
      description='Environment for CC PHD',
      author='CHEN Can',
      author_email='3120205026@bit.edu.cn',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=['numpy', 'scipy']
)
