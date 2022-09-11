from distutils.core import setup

setup(name='NE_Extracter',
      version='1.0.0',
      description='Python Economic and Financial Named Entity Extraction module',
      author='Wilawan Yathongkhum',
      author_email='wilawan_y@cmu.ac.th',
      license='gnu',
      url="https://github.com/Wilawan-Y/EconomicFinancial-NE-Extractor",
      install_requires=[
          'nltk',
          'marisa_trie',
          're',
          'pickle',
      ],
      )