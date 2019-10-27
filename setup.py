from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'pyhacks',
  packages = ['pyhacks'],
  version = '1.0.8',
  license='MIT',
  description = 'Ease developers to use queue/threads functions to handle big amount of data',
  long_description_content_type="text/markdown",
  long_description=long_description,
  author = 'Barak Tawily',
  author_email = 'barak.tawily@gmail.com',
  url = 'https://github.com/Quitten/pyhacks',
  download_url = 'https://github.com/Quitten/pyhacks/releases/v_01.tar.gz',
  keywords = ['threads','queue'],
  install_requires=[
          'uuid',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
