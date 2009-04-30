Download
========

Release 1.1
----------------

`Abjad 1.1.tar.gz <http://pypi.python.org/pypi/Abjad>`__

**Many** changes and improvements!

Highlights:

* Many composer and structure transformation tools added. See the `abjad.tools.*` in the :doc:`Abjad API </chapters/api/index>` package.
* All tools (construction, transformation, manipulation) are now very cleanly grouped and categorized in various packages.
* New ``abjad-book`` application available. Use ``abjad-book`` to interpret Abjad code blocks embedded in HTML, LaTex and reST documents. 


Release 1.0.1055
----------------
`Abjad 1.0.1055dev.tar.gz
<http://128.59.116.55/~abjad/Abjad-1.0.1055dev.tar.gz>`__

Changes to the public interface:

+ Abjad now models ties exclusively with the Tie spanner. The old
  *_TieInterface._set* attribute is now deprecated.
+ You can no longer say t.tie = True or t.tie = False, for leaf t. You
  must str ucturally span t as Tie(t) instead.
+ New public properties in _SpannerReceptor: chain, parented, count.



New public helpers:

+ iterate.tie_chains( ), list_helpers( ), measuretools.concentrate( ),
  measuretools.spin( ), measuretools.scale_and_remeter( ), play( ),
  durtools.rationalize( )



New tools:

+ construct.notes_curve( ), mathtools.interpolate_divide( )


Bug fixes:

+ Grace note appending and extending no longer throw error.




Release 1.0.1022
----------------

`Abjad 1.0.1012dev.tar.gz
<http://128.59.116.55/~abjad/Abjad-1.0.1012dev.tar.gz>`__

This is the first public release of Abjad!

