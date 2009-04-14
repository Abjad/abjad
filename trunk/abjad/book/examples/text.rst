This is **paragraph 1**.
Now comes some Abjad code

<abjad>
   abjad> v = Voice(construct.run(3))
   abjad> Beam(v)
   hide> write(v, 'example1')
   abjad> show(v)
</abjad>

Here is **paragraph 2**, and more Abjad code.
Notice that in the second block of abjad code I can reference objects and variables crated in previous blocks:

<abjad>
   abjad> pitchtools.diatonicize(v)
   abjad> Trill(v[4:])
   hide> write(v, 'example2')
   abjad> show(v)
</abjad>


And a final paragraph.

