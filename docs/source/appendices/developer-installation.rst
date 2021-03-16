Developer installation
======================

What's the difference between "packaged" and "cloned" installation? How can a local build
of Abjad's docs be made for viewing offline? How can Abjad be used with Jupyter
notebooks?

"Packaged" versus "cloned" installs of Abjad
--------------------------------------------

The majority of users install Abjad from the Python Package Index:

https://abjad.github.io/first_steps/macos.html

https://abjad.github.io/first_steps/linux.html

"Packaged" installation of Abjad is recommended for most users. Python installs the
current release of Abjad into the site-packages directory of the Python virtual
environment active at the time of installation. Installing Abjad from package means that
a user intends to compose with Abjad, but not develop Abjad.

Abjad can be installed another way, too. Clone Abjad from GitHub and then use pip to
install the clone in "editable" mode:

..  code-block:: bash

    ~$ git clone https://github.com/Abjad/abjad.git
    ~$ cd abjad
    abjad$ python -m pip install --editable .

"Cloned" installation of Abjad is necessary for users who want to develop Abjad. Cloned
installation is also required for users who want to build Abjad's docs locally.

Building Abjad's docs locally
-----------------------------

The most recent version of Abjad's docs is hosted here:

https://abjad.github.io/

This means that most users do not need to build Abjad's docs locally. Users who do want
to build Abjad's docs locally should clone and install Abjad as shown above. Then make
sure `TeXLive`_ and `Graphviz`_ are installed.

To install Graphviz on macOS via Homebrew:

..  code-block:: bash

    ~$ brew install graphviz

To install Graphviz on Debian and Ubuntu:

..  code-block:: bash

    ~$ sudo apt-get install graphviz

To check that Graphviz is callable from the commandline after install:

..  code-block:: bash

    ~$ dot -V
    dot - graphviz version 2.40.1 (20161225.0304)

Make a local version of the docs like this:

..  code-block:: bash

    ~$ cd path/to/abjad/docs
    ~$ make html

The build process takes a long time the first time it runs. Finished output is available
here:

..  code-block:: bash

    ~$ ls path/to/abjad/docs/build/html
    _images           _static           gallery-2010.html objects.inv       sidebar.html
    _modules          api               gallery-2015.html overview          welcome
    _mothballed       appendices        gallery-2020.html py-modindex.html
    _pending          examples          genindex.html     search.html
    _sources          first_steps       index.html        searchindex.js

Browse ``file:///path/to//abjad/docs/build/html/index.html`` to naviagate the build.

Jupyter notebooks
-----------------

Abjad can be used to embed music notation in `Jupyter`_ notebooks. Install Abjad with its
"ipython" extras:

..  code-block:: bash

    ~$ python -m pip install abjad[ipython]

Then install `timidity`_. To install timidity on Debian or Ubuntu:

..  code-block:: bash

    ~$ apt-get install timidity

To install timidity on macOS via Homebrew:

..  code-block:: bash

    ~$ brew install timidity

Run the following "magic" command in the cell of a Jupyter notebook to enable Abjad. Then
use ``abjad.show()`` and ``abjad.play()`` to embed music notation and MIDI files in your
notebook:

::

    %load_ext abjadext.ipython

..  _Jupyter: https://jupyter.org/
..  _Graphviz: http://graphviz.org/
..  _Sphinx: http://sphinx-doc.org/
..  _TeXLive: https://www.tug.org/texlive/
..  _timidity: http://timidity.sourceforge.net/
