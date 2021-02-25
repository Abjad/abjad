:orphan:

..  _appendix-virtualenv:

Virtual environments
====================

Managing different versions of Python on your system can be confusing. Your operating
system probably came with a version of Python preinstalled. And chances are good that you
will install a different version of Python sometime later, too.

This situation is not in itself a problem. But complexity arises in the management of the
different packages you install while you work. Use ``pip`` to install Python's ``roman``
package for Roman numerals. Is ``roman`` installed for Python 2.7.16 (which came bundled
with the most recent version of your operating system)?  Or for Python 3.6.0 (which you
installed by hand)? Which version of Python is ``pip`` working with? How can you check?
It usually works just to install a package and hope for the best. But what happens when
you upgrade Python? Or the packages you've installed?

Enter Python virtual environments. Python virtual environments allow you to isolate the
packages you install from packages preinstalled elsewhere on your computer. This can
clean up your development environment. Virtual environments also allow you to install
Python packages without using ``sudo``. We recommend all users of Abjad work in Python
virtual environments. Good summaries explaining how to work with Python virtual
environments are available on the Internet. We explain the outlines of process here, too.

The `virtualenv`_ package provides tools for working with Python virtual environments.
Almost everything you'll want to do with Python virtual environments can be done with the
`virtualenvwrapper`_ package:

..  code-block:: bash

    ~$ sudo pip install virtualenvwrapper

After installing ``virtualenvwrapper`` you have to decide where Python should store the
files you create when working in a virtual environment. Any directory will work. We
recommend ``~/.virtualenvs``. Decide which directory to use and then set the
``WORKON_HOME`` environment variable:

..  code-block:: bash

    ~$ export WORKON_HOME=~/.virtualenvs
    ~$ mkdir -p $WORKON_HOME

Source the ``virtualenvwrapper.sh`` script. This script teaches your shell how to create,
activate and delete virtual environments:

..  code-block:: bash

    ~$ source `which virtualenvwrapper.sh`

You can now create a virtual environment named ``abjad`` like this:

..  code-block:: bash

    ~$ mkvirtualenv abjad

The terminal prompt changes to show that you are now working in the ``abjad`` virtual
environment you just created. Now you can install Python packages in the ``abjad``
virtual environment and be safe in the knowledge that packages you install won't
interfere with Python packages installed anywhere else on your system. Here's how you
install the Abjad package in your ``abjad`` virtual environment:

..  code-block:: bash

    ~(abjad)$ pip install abjad

When you are done working in a virtual environment you can exit the virtual environment
to return to your default shell:

..  code-block:: bash

    ~(abjad)$ deactivate

Add these two lines to your profile if you decide to use Python virtual environments
every time you work in Abjad:

..  code-block:: bash

    export WORKON_HOME=$HOME/.virtualenvs
    source `which virtualenvwrapper.sh`

..  _virtualenv: https://readthedocs.org/projects/virtualenv/
..  _virtualenvwrapper: https://virtualenvwrapper.readthedocs.org/en/latest/
