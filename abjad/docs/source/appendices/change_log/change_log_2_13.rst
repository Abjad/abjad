:orphan:

Changes from 2.12 to 2.13
-------------------------

Updated system requirements from Python 2.7.2 to 2.7.5.

Reduced the number of public functions from 1045 to 465.

Reduced the number of public classes from 559 to 485.

Added top-level ``inspect_()``, ``mutate()`` and ``select()`` functions.

Removed the terms `prolated` and `preprolated` from the system.
Use ``note.duration`` and ``inspect_(note).get_duration()`` to work with
duration attributes.

Changed all occurrences of `klass` to `class` in the functions of the API.

Removed the terms `melodic` and `harmonic` from the system in reference to the
directedness of intervals.

Removed the terms `chromatic` and `diatonic` from the system in reference to
pitches and pitch classes.
