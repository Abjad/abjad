Memory consumption
==================

You can examine memory consumption with tools included in the ``guppy`` module::

   from guppy import hpy
   hp = hpy( )
   hp.setrelheap( )
   notes = [Note(0, (1, 4)) for x in range(1000)]
   h = hp.heap( )
   print h

::

   Partition of a set of 544106 objects. Total size = 62090200 bytes.
    Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
        0  79000  15 11060000  18  11060000  18 dict (no owner)
        1   2000   0  3352000   5  14412000  23 dict of abjad.components.Grace.Grace.Grace
        2  49001   9  2376132   4  16788132  27 list
        3   1000   0  1676000   3  18464132  30 dict of abjad.components.Note.Note.Note
        4  51004   9  1644200   3  20108332  32 tuple
        5   3000   1  1572000   3  21680332  35 dict of
                                                abjad.interfaces.BeamInterface.BeamInterface.BeamInterf
                                                ace
        6   3000   1  1572000   3  23252332  37 dict of
                                                abjad.interfaces.BreaksInterface.BreaksInterface.Breaks
                                                Interface
        7   3000   1  1572000   3  24824332  40 dict of
                                                abjad.interfaces.ClefInterface.ClefInterface.ClefInterf
                                                ace
        8   3000   1  1572000   3  26396332  43 dict of
                                                abjad.interfaces.DirectivesInterface.DirectivesInterfac
                                                e.DirectivesInterface
        9   3000   1  1572000   3  27968332  45 dict of
                                                abjad.interfaces.InstrumentInterface.InstrumentInterfac
                                                e.InstrumentInterface
   <138 more rows. Type e.g. '_.more' to view.>

These results show 62.1M for 1000 notes.

You must download ``guppy`` from the public Internet because the module
is not included in the Python standard library.
