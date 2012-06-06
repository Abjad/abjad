This is **paragraph 1**.
Now comes some Abjad code

<abjad>
   >>> v = Voice("c'8 d'8 e'8")
   >>> Beam(v)
   hide> write(v, 'example1')
   >>> show(v)
</abjad>

Here is **paragraph 2**, and more Abjad code.
Notice that in the second block of abjad code I can reference objects and variables created in previous blocks:

<abjad>
   >>> Trill(v[4:])
   hide> write(v, 'example2')
   >>> show(v)
</abjad>


And a final paragraph.
