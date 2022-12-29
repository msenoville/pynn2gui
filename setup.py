from distutils.core import setup

with open( "README.md", "r" ) as fh:
    long_description = fh.read()

setup(
  name = "pynn2gui",
  packages = [
      "pynn2gui"
      ],
  version = "0.1.0",
  license="",
  description = "Module to export any PyNN script to the PyNN GUI (wip).",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author = "Matthieu Sénoville",
  author_email = "matthieu.senoville@cnrs.fr",
  url = "https://github.com/msenoville/pynn2gui",
  keywords = ["PYNN","NEUROMORPHIC", "SPIKING", "NEURAL NETWORK", "SPINNAKER", "BRAINSCALES, NEST"],
  install_requires=[
         "pyNN>=0.8.0"
     ],
  classifiers=[
    "Development Status :: 3 - Alpha",      # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    "Intended Audience :: Developers",      # Define that your audience are developers
    "Topic :: Scientific/Engineering",
    # "License :: OSI Approved :: BSD License",
    'Natural Language :: English',
    'Operating System :: OS Independent',
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
  ],
  python_requires = ">=3.5",
)