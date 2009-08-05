Duration interfaces compared
============================

=========== ====  ====  =========   =======  ======   =========   =========
\           core  leaf  container   measure  tuplet   fd tuplet   fm tuplet 
=========== ====  ====  =========   =======  ======   =========   =========
contents    –     –     ↵           ↵        ↵        ↵           ↵ 
multiplied  –     ↵     –           –        –        ↵           ↵
multiplier  –     √     –           ↵        ↵        ↵           √ 
preprolated ↵     ↵     ↵           ↵        ↵        ↵           ↵ 
prolated    ↵     ↵     ↵           ↵        ↵        ↵           ↵ 
prolation   ↵     ↵     ↵           ↵        ↵        ↵           ↵ 
target      –     –     –           –        –        √           – 
written     –     √     –           –        –        –           –
=========== ====  ====  =========   =======  ======   =========   =========


The table contains a total of only four settable duration attributes, divided among only three classes. Durated Abjad classes offer up many read-only duration attributes but very few read-write duration attributes.

All classes carry all three prolation-related attributes because all
classes can nest inside containers. It is possible, for example, to
nest an entire voice within a fixed-duration tuplet.


.. note::
   Leaf multipliers and tuplet multipliers differ.

.. note::
   :class:`_MeasureDurationInterface <abjad.measure.duration._MeasureDurationInterface>` implements `nonbinary` attributes not shown above.  


