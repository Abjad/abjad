Duration types
==============

Abjad publishes duration information about notes, rests, chords and
skips, and also about tuplets, measures, voices, staves and the other
containers. Abjad groups duration information about notes, rests,
chords and skips into the :class:`abjad.leaf.duration._LeafDurationInterface` class; duration
information about tuplets, measures, voices, staves and other
containers groups together inside some type of container duration
interface. For information on the duration of notes, rests, chords and
skips, see :doc:`the chapter on working with leaf durations
<../leaf/index>`; for information on the
duration of tuplets, measures, voices, staves and other containers,
see :doc:`the chapter on working with container durations
<../container/index>`. This chapter
lists all duration attributes, belonging to leaves, containers or
both.



Written duration
----------------

Abjad notes, rests, chords and skips all make written duration
available as `duraiton.written`. Written duration is a user-assignable
rational number. Users can assign and reassign the written duration of
notes, rests, chords and skips at initialization and at any time
during the life of the note, rest, chord or skip. Notes, rests, chords
and skips admit a degree of input flexibility; Abjad `Rational`
instances, rational tokens, and integers are all allowed; see the
chapter on :doc:`duration initialzation <../initialization/index>` for details. 
Written durations must always be notehead-assignable; see the chapter on
:doc:`assignability <../assignability/index>` for
details. The written duration of notes, rests, chords and skips
corresponds more closely to our usual understanding of musical
duration than do any of the other Abjad duration attributes. Abjad
containers do not carry written duration.

.. sourcecode:: python

    
    abjad> note = Note(0, (1, 4))
    abjad> note.duration.written
    Rational(1, 4)




Prolated duration
-----------------

:doc:`Prolation <../prolation/index>` refers to the duration-scaling
effects of tuplets and special types of time signature. Prolation is a
way of thinking about the contribution that musical structure makes to
the duration of score objects. All durated Abjad objects carry a
prolated duration as `duration.prolated`. Prolated duration is an
emergent property of notes, tuplets and other durated objects. The
prolated duration of notes, rests, chords and skips equals the product
of the written duration and prolation of those objects. The prolated
duration of tuplets, measures and other containers equals the product
of the container duration interface itself and the prolation of the
container in question.



.. todo::

   Prolated leaf duration makes perfect sense: written * prolation. But
   prolated container duration is a mess: self * prolation, where self is
   whatever magic value the container duration interface itself carries.
   Clean this in the one remaining duration rewrite. We want duration
   interface comparison of the form `leaf1.duration == leaf2.duration`
   and `container1.duration == container2.duration`. But we do not want
   duration interface assignment of the form `container1.duration = (1,
   8)`. Right now, unfortunately, fixed-duration tuplets demand interface
   assignment when, for example, you want to change the "container size"
   (or whatever it is) of the tuplet in question.

