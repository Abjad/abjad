:tocdepth: 2

Version history
===============


Abjad 2.15
----------

Released 2014-05-22. Implements 440 public classes and 391 functions totaling
170,677 lines of code.


Python 3.4+ compatibility
^^^^^^^^^^^^^^^^^^^^^^^^^

Abjad 2.15 is the first version of Abjad to be compatible with both Python 2
and 3. Our py.test and doctest suites pass under both 2.7.5 and 3.4.0

We'll continue to work over the next year to improve documentation support
under Python 3.


IPython notebook extension
^^^^^^^^^^^^^^^^^^^^^^^^^^

Abjad 2.15 features an IPython notebook extension for capturing the output of
`show()` as PNGs. To activate the extension in a notebook include the following
two lines:

::
    
    from abjad import *
    %load_ext abjad.ext.ipython


Parameterized test suite
^^^^^^^^^^^^^^^^^^^^^^^^

We've implemented a suite of parameterized tests in our regression battery
which test *every* function and class in Abjad's toolkit for a variety of
common functionalities such as copyability, documentation coverage, hashability
and pickling.


Improved tools package APIs
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Abjad 2.15 features a simpler lilypondfiletools API:

    lilypondfiletools.BookBlock
    lilypondfiletools.BookpartBlock
    lilypondfiletools.ContextBlock
    lilypondfiletools.HeaderBlock
    lilypondfiletools.LayoutBlock
    lilypondfiletools.MIDIBlock
    lilypondfiletools.PaperBlock

    lilypondfiletools.ContextBlock
    lilypondfiletools.Block

Abjad 2.15 features a simpler and more powerful rhythm-maker API.

Simplified scoretools API:

    scoretools.Score
    scoretools.StaffGroup
    scoretools.Staff
    scoretools.Voice


Mutation improvements
^^^^^^^^^^^^^^^^^^^^^

Added `transpose()` method to MutationAgent.

You can now say:

::

    >>> staff = Staff("<c' e' g'>4 d'4 <e' g' c''>4")
    >>> mutate(staff).transpose(+6)
    >>> print format(staff)
    \new Staff {
            <gf' bf' df''>4
            af'4
            <bf' df'' gf''>4
    }

Made mutate(expr).rewrite_meter() more robust


New `indicatortools` classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Arpeggio
    KeyCluster
    LaissezVibrer


New `datastructuretools` classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    ContextMap


Thanks
^^^^^^

Special thanks to:

    George K. Thiruvathukal <thiruvathukal@gmail.com>
    Tiago Antão <tiagoantao@gmail.com>

for their help and with our Python 3 conversion and IPython integration.


Older versions
--------------

..  toctree::
    :maxdepth: 1

    version_2_14
    version_2_13
    version_2_12
    version_2_11
    version_2_10
    version_2_9
    version_2_8
    version_2_7
    version_2_6
    version_2_5
    version_2_4
    version_2_3
    version_2_2
    version_2_1
    version_2_0
