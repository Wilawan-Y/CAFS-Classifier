from setuptools import setup
import subprocess

# List of additional packages to check and install if needed
ADDITIONAL_PACKAGES = [
    'nltk==3.8.1',
    'marisa_trie==0.8.0',
    'pandas==1.5.3',
    'regex',
	'operator',
	'scikit-learn==1.2.2'
]

# Check if the package is installed
def package_installed(package_name):
    try:
        __import__(package_name)
    except ImportError:
        return False
    return True

# Install additional packages if they are not already installed
def install_additional_packages():
    missing_packages = [pkg for pkg in ADDITIONAL_PACKAGES if not package_installed(pkg)]
    if missing_packages:
        print(f"Installing additional packages: {', '.join(missing_packages)}")
        subprocess.call(['pip', 'install'] + missing_packages)

# Run the installation
if __name__ == '__main__':
    install_additional_packages()

    setup(name='CAFS_Classier',
      version='1.0.0',
      description='Python package for Economic and Financial News Categorization.',
      author='Wilawan Yathongkhum',
      author_email='wilawan_y@cmu.ac.th',
      license='gnu',
      url="https://github.com/Wilawan-Y/CAFS-Classifier",
      install_requires=[
          'nltk==3.8.1',
          'marisa_trie==0.8.0',
		  'pandas==1.5.3',
		  'regex',
		  'operator',
	      'scikit-learn==1.2.2'
      ]
      )
