from setuptools import setup, find_packages

setup(name='pyScripts',
      version='0.0.1',
      description='python functions for measurement analysis',
      url='https://github.com/julienbarrier/pyScripts',
      author='Julien Barrier',
      author_email='julien.barrier@manchester.ac.uk',
      classifiers=[
          'Intended Audience :: Science/Research',
          'Programming Language :: Python :: 3 :: Only',
          'License :: Apache License',
          'Topic :: Scientific/Engineering',
      ],
      license='Apache',
      packages=find_packages(),
      python_requires='>=3.9',
      zip_safe=False)
