Install
=======

Abjad is developed and tested on MacOS and Linux. Abjad is not tested on Windows.

(Interested in maintaining Abjad for Windows? We'd be happy to have you :ref:`join the
team. <appendix-community>`)

..  rubric:: Check your version of Python

Abjad requires Python 3.6 or later:

..  code-block:: bash

    ~$ python --version
    Python 3.9.0

..  rubric:: Install LilyPond

Make sure LilyPond is installed on your computer. If LilyPond is not callable from the
commandline, add the location of the LilyPond executable to your path:

..  code-block::

    ~$ lilypond --version
    GNU LilyPond 2.21.80

    Copyright (c) 1996--2020 by
    Han-Wen Nienhuys <hanwen@xs4all.nl>
    Jan Nieuwenhuizen <janneke@gnu.org>
    and others.

    This program is free software.  It is covered by the GNU General Public
    License and you are welcome to change it and/or distribute copies of it
    under certain conditions.  Invoke as `lilypond --warranty' for more
    information.

..  rubric:: Install Abjad

We recommend using :ref:`appendix-virtualenv` to install Abjad.

Create a virtual environment. Then install Abjad:

..  code-block:: bash

    ~$ pip install abjad

..  _CPython: http://www.python.org
..  _GitHub: https://github.com/Abjad/abjad
..  _Graphviz: http://graphviz.org/
..  _Homebrew: http://brew.sh/
..  _IPython notebook: http://ipython.org/notebook.html
..  _IPython: http://ipython.org/
..  _LaTeX: https://tug.org/
..  _LilyPond: http://lilypond.org/
..  _PyPI: https://pypi.python.org/pypi/Abjad
..  _Python: https://www.python.org/
..  _Sphinx: http://sphinx-doc.org/
..  _TeXLive: https://www.tug.org/texlive/
..  _timidity: http://timidity.sourceforge.net/
..  _pip: https://pip.pypa.io/en/stable/
..  _pytest: http://pytest.org/latest/
..  _virtualenv: https://readthedocs.org/projects/virtualenv/
..  _virtualenvwrapper: https://virtualenvwrapper.readthedocs.org/en/latest/
