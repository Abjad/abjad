Version history
===============


Release 1.1 
-----------
`Abjad 1.1.tar.gz <http://pypi.python.org/pypi/Abjad>`__

*  Many structure transform tools added. See the `abjad.tools.*`
   in the :doc:`Abjad API </chapters/api/index>` package.

*  Construction, transformation, manipulation and all other tools
   now grouped cleanly into packages.

*  New ``abjad-book`` application available. 
   Use ``abjad-book`` to interpret Abjad code blocks embedded in 
   HTML, LaTex and reST documents. 


Release 1.0.1055
----------------
`Abjad 1.0.1055dev.tar.gz
<http://128.59.116.55/~abjad/Abjad-1.0.1055dev.tar.gz>`__

Changes to the public interface:

*  Abjad now models ties exclusively with the Tie spanner. 
   The old ``_TieInterface._set`` attribute is now deprecated.

*  You can no longer say ``t.tie = True`` or ``t.tie = False``, 
   for leaf ``t``. You must structurally span ``t`` as ``Tie(t)`` 
   instead.

*  New public properties in ``_SpannerReceptor``: 
   ``chain, parented, count``.

*  New public helpers: 

   *  ``construct.notes_curve()``
   *  ``durtools.rationalize()``
   *  ``iterate.tie_chains()``
   *  ``list_helpers()``
   *  ``mathtools.interpolate_divide()``
   *  ``measuretools.concentrate()``
   *  ``measuretools.scale_and_remeter()``
   *  ``measuretools.spin()`` 
   *  ``play()``

*  Grace note ``append()`` and ``extend()`` no longer throw errors.


Release 1.0.1022
----------------

`Abjad 1.0.1012dev.tar.gz
<http://128.59.116.55/~abjad/Abjad-1.0.1012dev.tar.gz>`__

*  First public release of Abjad.


.. todo:: Add release dates.

