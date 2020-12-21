Developer installation
======================

What if you want to run Abjad's test suite? Or build Abjad's docs locally?

Clone Abjad's Github repository. Then use pip to install Abjad in edit mode with Abjad's
"test" extras. Abjad's "test" extras install `pytest`_ and `Sphinx`_. If your machine
does not have a C compiler, you may see Sphinx error messages while pip runs.
These warnings are harmless and will not prevent Sphinx's installation:

..  code-block:: bash

    ~$ git clone https://github.com/Abjad/abjad.git
    ~$ cd abjad
    abjad$ pip install -e .[test]

To build Abjad's docs, you also need to install `TeXLive`_ and `Graphviz`_. Abjad uses
Graphviz to create graphs of rhythm-trees and class hierarchies. To install Graphviz on
Debian and Ubuntu:

..  code-block:: bash

    ~$ sudo apt-get install graphviz

To install Graphviz on MacOS via Homebrew:

..  code-block:: bash

    ~$ brew install graphviz

Then make sure Graphviz is callable from the commandline:

..  code-block:: bash

    ~$ dot -V
    dot - graphviz version 2.40.1 (20161225.0304)

..  _Graphviz: http://graphviz.org/
..  _Sphinx: http://sphinx-doc.org/
..  _TeXLive: https://www.tug.org/texlive/
..  _pytest: http://pytest.org/latest/
