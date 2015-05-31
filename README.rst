****************************
Sphinx changelist extentsion
****************************

Installation
============


::

    pip install sphinx-changelist

Usage
=====


#. Add extension into conf.y::

    # Add any Sphinx extension module names here, as strings. They can be
    # extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
    # ones.
    extensions = ['sphinx_changelist']

#. Place the directive **changelist** any where in your rst file::

    .. chnagelist::

        0.1.0 2015-05-05

#. Make it::

    make html

