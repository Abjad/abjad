Jupyter notebooks
=================

Abjad can be used to embed music notation in `Jupyter`_ notebooks. Install Abjad with its
"ipython" extras:

..  code-block:: bash

    ~$ pip install abjad[ipython]

Then install `timidity`_. To install timidity on Debian or Ubuntu:

..  code-block:: bash

    ~$ apt-get install timidity

To install timidity on MacOS via Homebrew:

..  code-block:: bash

    ~$ brew install timidity

Run the following "magic" command in the cell of a Jupyter notebook to enable Abjad. Then
use ``abjad.show()`` and ``abjad.play()`` to embed music notation and MIDI files in your
notebook:

::

    %load_ext abjadext.ipython

..  _Jupyter: https://jupyter.org/
..  _timidity: http://timidity.sourceforge.net/
