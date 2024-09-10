# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('.'))   # Default path
sys.path.insert(0, os.path.abspath('..'))  


project = 'Sketch Image Classification'
copyright = '2024, Park Dong Jun'
author = 'Park Dong Jun'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.githubpages'
             ]
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = []

language = 'ko'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_favicon = 'favicon.ico'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_baseurl = 'https://poodlee.github.io/Boostcamp_7th_CV-01-Sketch_Classification/'
##############################################################################
