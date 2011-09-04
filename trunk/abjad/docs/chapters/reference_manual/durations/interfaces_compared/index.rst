Duration interfaces compared
============================

=========== ====  ====  =========   =======  ======   =========   =========
type        core  leaf  container   measure  tuplet   fd tuplet   fm tuplet 
=========== ====  ====  =========   =======  ======   =========   =========
contents    –     –     R           R        R        R           R
multiplied  –     R     –           –        –        R           R
multiplier  –     RW    –           R        R        R           RW 
preprolated R     R     R           R        R        R           R 
prolated    R     R     R           R        R        R           R
prolation   R     R     R           R        R        R           R
target      –     –     –           –        –        RW          – 
written     –     RW    –           –        –        –           –
=========== ====  ====  =========   =======  ======   =========   =========


The table contains a total of only four settable duration attributes, divided among only three classes. Durated Abjad classes offer up many read-only duration attributes but very few read-write duration attributes.

All classes carry all three prolation-related attributes because all
classes can nest inside containers. It is possible, for example, to
nest an entire voice within a fixed-duration tuplet.


.. note::
   Leaf multipliers and tuplet multipliers differ.
