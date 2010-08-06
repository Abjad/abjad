Pitch conventions
=================

Abjad follows the following pitch conventions.


Names
-----

Abjad names pitches according to the LilyPond ``english.ly`` module.

Abjad names accidentals according to the table below.

   ======================       ========
   accidental                    symbol
   ======================       ========
   quarter sharp                 'qs'
   quarter flat                  'qf' 
   sharp                         's' 
   flat                          'f' 
   three-quarters sharp          'tqs' 
   three-quarters flat           'tqf' 
   double sharp                  'ss' 
   double flat                   'ff'
   ======================       ========


Numbers
-------

Abjad sets middle C equal to 0. This follows the presentation of
American pitch-class theory in, for example, [Morris1987]_ .

IRCAM / MIDI pitch numbers equal Abjad pitch numbers plus 60.


Octaves
-------

Abjad represents octaves with both numbers and ticks.

   ===============      =============
   Octave notation      Tick notation
   ===============      =============
         C7                   c'''' 
         C6                   c''' 
         C5                   c'' 
         C4                   c' 
         C3                   c 
         C2                   c, 
         C1                   c,,
   ===============      =============

Abjad follows American usage and sets the octave of middle C equal to 4.
usage.

Abjad uses ticks in LilyPond output only.


Accidental spelling
-------------------

Abjad chooses between enharmonic spellings at pitch-initialization
time according to the following table.

   ===============      ================
   PC number            Default spelling
   ===============      ================
      0                    C 
      1                    C♯ 
      2                    D 
      3                    E♭ 
      4                    E 
      5                    F 
      6                    F♯ 
      7                    G 
      8                    G♭ 
      9                    A 
      10                   B♭ 
      11                   B
   ===============      ================

For example::

   abjad> t = Staff([Note(n, (1, 8)) for n in range(12)])
   abjad> print t.format
   \new Staff {
           c'8
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
           af'8
           a'8
           bf'8
           b'8
   }

You can use :func:`pitchtools.make_sharp() 
<abjad.tools.pitchtools.make_sharp.make_sharp>` and 
:func:`pitchtools.make_flat() 
<abjad.tools.pitchtools.make_flat.make_flat>` to respell accidentals
after initialization::

   abjad> pitchtools.make_sharp(t)
   abjad> print t.format
   \new Staff {
           c'8
           cs'8
           d'8
           ds'8
           e'8
           f'8
           fs'8
           g'8
           gs'8
           a'8
           as'8
           b'8
   }
