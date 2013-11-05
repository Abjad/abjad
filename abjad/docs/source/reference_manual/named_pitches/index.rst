Named pitches
=============

Named pitches are the everyday pitches attached to notes and chords:

::

   >>> note = Note("cs''8")
   >>> show(note)

.. image:: images/index-1.png


::

   >>> note.written_pitch
   NamedPitch("cs''")



Creating named pitches
----------------------

Create named pitches like this:

::

   >>> named_pitch = NamedPitch("cs''")


::

   >>> named_pitch
   NamedPitch("cs''")



Inspecting the name of a named pitch
------------------------------------

Use ``str()`` to get the name of named pitches:

::

   >>> str(named_pitch)
   "cs''"



Inspecting the octave of a named pitch
--------------------------------------

Get the octave number of named pitches with ``octave_number``:

::

   >>> named_pitch.octave_number
   5



Sorting named pitches
---------------------

Named pitches sort by octave, diatonic pitch-class and accidental:

::

   >>> pitchtools.NamedPitch('es') < pitchtools.NamedPitch('ff')
   True



Comparing named pitches
-----------------------

You can compare named pitches to each other:

::

   >>> named_pitch_1 = pitchtools.NamedPitch("c''")
   >>> named_pitch_2 = pitchtools.NamedPitch("d''")


::

   >>> named_pitch_1 == named_pitch_2
   False


::

   >>> named_pitch_1 != named_pitch_2
   True


::

   >>> named_pitch_1 > named_pitch_2
   False


::

   >>> named_pitch_1 < named_pitch_2
   True


::

   >>> named_pitch_1 >= named_pitch_2
   False


::

   >>> named_pitch_1 <= named_pitch_2
   True



Converting a named pitch to a numbered pitch
--------------------------------------------

Convert a named pitch to a numbered pitch like this:

::

   >>> named_pitch.numbered_pitch
   NumberedPitch(13)


Or like this:

::

   >>> pitchtools.NumberedPitch(named_pitch)
   NumberedPitch(13)



Converting a named pitch to a named pitch-class
-----------------------------------------------

Convert a named pitch to a named pitch-class like this:

::

   >>> named_pitch.named_pitch_class
   NamedPitchClass('cs')


Or like this:

::

   >>> pitchtools.NamedPitchClass(named_pitch)
   NamedPitchClass('cs')



Converting a named pitch to a numbered pitch-class
--------------------------------------------------

Convert a named pitch to a numbered pitch-class like this:

::

   >>> named_pitch.numbered_pitch_class
   NumberedPitchClass(1)


Or like this:

::

   >>> pitchtools.NumberedPitchClass(named_pitch)
   NumberedPitchClass(1)



Copying named pitches
---------------------

Use ``copy.copy()`` to copy named pitches:

::

   >>> import copy


::

   >>> copy.copy(named_pitch)
   NamedPitch("cs''")


Or use ``copy.deepcopy()`` to do the same thing.
