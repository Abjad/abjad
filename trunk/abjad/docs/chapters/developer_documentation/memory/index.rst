Memory consumption
==================

You can examine memory consumption with tools included in the ``guppy`` module::

    from guppy import hpy
    hp = hpy()
    hp.setrelheap()
    notes = [Note(0, (1, 4)) for x in range(1000)]
    h = hp.heap()
    print h

::

    Partition of a set of 11024 objects. Total size = 586364 bytes.
     Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
         0   1000   9   124000  21    124000  21 abjad.tools.notetools.Note.Note.Note
         1   1004   9   116464  20    240464  41 __builtin__.set
         2   2003  18    76300  13    316764  54 list
         3   1000   9    52000   9    368764  63
                                                 abjad.tools.pitchtools.NamedChromaticPitch.NamedChromat
                                                 icPitch.NamedChromaticPitch
         4   1000   9    44000   8    412764  70
                                                 abjad.interfaces._OffsetInterface._OffsetInterface._Off
                                                 setInterface
         5   1000   9    44000   8    456764  78 abjad.tools.notetools.NoteHead.NoteHead.NoteHead
         6   1000   9    40000   7    496764  85 0x23add0
         7   1000   9    32000   5    528764  90
                                                 abjad.interfaces.ParentageInterface.ParentageInterface.
                                                 ParentageInterface
         8   1011   9    28568   5    557332  95 str
         9   1000   9    28000   5    585332 100
                                                 abjad.interfaces._NavigationInterface._NavigationInterf
                                                 ace._NavigationInterface
    <6 more rows. Type e.g. '_.more' to view.>


These results show 586K for 1000 notes.

You must download ``guppy`` from the public Internet because the module
is not included in the Python standard library.
