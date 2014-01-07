:tocdepth: 2

Change log
==========


Changes from 2.13 to 2.14
-------------------------

Reduced the number of public functions from 465 to 438.

Reduced the number of public classes from 485 to 429.

Cleaned up many packages in the API such that they now contain only classes and
no functions.

Added top-level ``attach()``, ``detach()``, ``override()``,
``set_()``, ``graph()``, ``iterate()``, ``new()`` and ``persist()``
functions.

Replaced ``marktools`` and ``contexttools`` packages with ``indicatortools``
package.

Removed ``chordtools``, ``containertools``, ``measuretools``, ``notetools``,
``resttools``, ``skiptools``, ``stafftools``, ``tuplettools`` and
``voicetools`` packages. Moved all classes and functions to ``scoretools``
package.

Added most frequently used indicator classes to the global namespace:
``Articulation``, ``Clef``, ``Dynamic``, ``KeySignature``, ``Markup``,
``Tempo``, ``TimeSignature``.

Added most frequently used spanner classes to the global namespace: ``Beam``,
``Crescendo``, ``Decrescendo``, ``Glissando``, ``Hairpin``, ``Slur``, ``Tie``.

Removed ``attach()`` and ``detach()`` methods from indicator classes; use
top-level ``attach()`` and ``detach()`` functions instead.

Removed ``attach()`` and ``detach()`` methods from spanner classes; use
top-level ``attach()`` and ``detach()`` functions instead.

Removed ``iotools`` package. Use ``persist()`` function instead.

Removed ``iterationtools`` package. Use ``iterate()`` function instead.

Added ``IsAtSoundingPitch`` and ``IsUnpitched`` indicator classes.

Removed ``mathtools.cumulative_sums_zero()`` and
``mathtools.cumulative_products_zero()``; use ``mathtools.cumulative_sums()``
and ``mathtools.cumulative_products()`` instead.

Removed ``timerelationtools`` package. Merged package contents into
``timespantools`` package.

Removed ``timesignaturetools`` package. Renamed ``MetricalHierarhcy`` class to
``Meter`` and moved related contents to new ``metertools`` package.

Renamed ``lilypondproxytools`` package. The new name is ``lilypondnametools``.
Reduced the number of classes in the package from seven to three.

Replaced ``updatetools`` package with ``systemtools.UpdateManager``. Replaced
``wellformednesstools`` package with ``systemtools.WellformednessManager``.
Replaced ``testtools`` package with ``systemtools.TestManager``. Replaced
``formattools`` package with ``systemtools.LilyPondFormatManager``. Replaced
``importtools`` package with ``systemtools.ImportManager``. Replaced
``iotools`` package with ``systemtools.IOManager``.

Removed another dozen custom exception classes.

Added first set of parameterized tests in ``tools/test/`` directory.

Documented instrument classes.


Older Versions
--------------

..  toctree::
    :maxdepth: 1
   
    change_log_2_13
    change_log_2_11
    change_log_2_10
