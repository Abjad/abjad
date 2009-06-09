def sign(n):
   '''Return ``-1``, ``0``, ``1`` for 
   negative, zero, positive numbers, respectively.

   ::
   
      abjad> mathtools.sign(-96.2)
      -1

   ::

      abjad> mathtools.sign(0)
      0

   ::

      abjad> mathtools.sign(Rational(9, 8))
      1
  
   .. note:: ``mathtools.sign(n)`` aliases built-in ``cmp(n, 0)``.'''

   return cmp(n, 0)
