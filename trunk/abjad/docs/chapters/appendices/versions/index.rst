Version history
===============


Abjad 1.1.1
-----------

`Abjad 1.1.1.tar.gz <http://pypi.python.org/pypi/Abjad>`__ 

*   More complete documentation.

*   The configuration file ``config`` changed to pure Python ``config.py``. 
    The file now supports more settings previously read as environment 
    variables. All user setings are now found in this file. 
    Users no longer need to set environment variables. 

*   Some new classes

    *   ``_HistoryInterface``. Use the _HistoryInterface to apply attributes to 
        any component in score that will be completely ignored by Abjad. 
        Think of the _HistoryInterface as a private user namespace.
    *   ``_NoteColumnInterface`` to handle the LilyPond NoteColumn grob. 
    *   ``_SpanBarInterface``. See API for details.
    *   ``InvisibleStaff( )`` staff.
    *   ``Moment`` utility class to model the Abjad representation of the LilyPond moment.

*   New Spanners

    *   ``TempoProportional`` spanner.

*   More than a dozen new tools added. 


Abjad 1.1.0
-----------

*   Many structure transform tools added. See the `abjad.tools.*`
    in the :doc:`Abjad API </chapters/api/index>` package.

*   Construction, transformation, manipulation and all other tools
    now grouped cleanly into packages.

*   New ``abjad-book`` application available. 
    Use ``abjad-book`` to interpret Abjad code blocks embedded in 
    HTML, LaTex and reST documents. 



Abjad 1.0.1055
----------------

Changes to the public interface:

*   Abjad now models ties exclusively with the Tie spanner. 
    The old ``_TieInterface._set`` attribute is now deprecated.

*   You can no longer say ``t.tie = True`` or ``t.tie = False``, 
    for leaf ``t``. You must structurally span ``t`` as ``Tie(t)`` 
    instead.

*   New public properties in ``_SpannerReceptor``: ``chain, parented, count``.

*   New public helpers: 

    *  ``construct.notes_curve()``
    *  ``durtools.rationalize()``
    *  ``iterate.tie_chains()``
    *  ``list_helpers()``
    *  ``mathtools.interpolate_divide()``
    *  ``measuretools.concentrate()``
    *  ``measuretools.scale_and_remeter()``
    *  ``measuretools.spin()`` 
    *  ``play()``

*   Grace note ``append()`` and ``extend()`` no longer throw errors.


Abjad 1.0.1022
----------------

*   First public release of Abjad.
