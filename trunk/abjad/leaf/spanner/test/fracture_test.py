from abjad import *


def test_fracture_01( ):
   '''
   Fracture left of t[0].

   Start with spanner spanning the four components in t.
   The spanner aggregator of component t[i] in t knows that 
   p and only p references t[i].

   Call fracture('left') on the zeroth component t[0] in t.
   Three-element receipt returns. 
   Source spanner returns unaltered and continues to hold references
   to all four components in t.
   'left' part of receipt returns empty spanner and holds no references
   to any components in t.
   'right' part of receipt returns new spanner and holds references
   to all four components in t.
   '''

   t = Voice(scale(4))
   p = Spanner(t[ : ])

   "Spanner(c'8, d'8, e'8, f'8)"

   assert len(p.components) == 4
   assert p.components[0] is t[0]
   assert p.components[1] is t[1]
   assert p.components[2] is t[2]
   assert p.components[3] is t[3]

   assert len(t[0].spanners.mine( )) == 1
   assert len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.mine( )) == 1

   assert t[0].spanners.mine( )[0] is p
   assert t[1].spanners.mine( )[0] is p
   assert t[2].spanners.mine( )[0] is p
   assert t[3].spanners.mine( )[0] is p

   assert check(t)

   receipt = t[0].spanners.fracture('left')[0]
   source, left, right = receipt

   "(Spanner(c'8, d'8, e'8, f'8), Spanner( ), Spanner(c'8, d'8, e'8, f'8))"

   assert source is p
   assert len(source.components) == 4

   assert source.components[0] is t[0]
   assert source.components[1] is t[1]
   assert source.components[2] is t[2]
   assert source.components[3] is t[3]

   assert left is not p
   assert len(left.components) == 0

   assert right is not p
   assert len(right.components) == 4
   assert right.components[0] is t[0]
   assert right.components[1] is t[1]
   assert right.components[2] is t[2]
   assert right.components[3] is t[3]
   
   assert len(t[0].spanners.mine( )) == 1
   assert len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.mine( )) == 1

   assert t[0].spanners.mine( )[0] is right
   assert t[1].spanners.mine( )[0] is right
   assert t[2].spanners.mine( )[0] is right
   assert t[3].spanners.mine( )[0] is right

   assert check(t)


def test_fracture_02( ):
   '''
   Fracture left of t[1].
   
   Fracture left of positive index. 
   Three-element receipt.
   Source spanner returns unaltered.
   'left' and 'right' parts return new spanners.
   'left' and 'right' parts partition components in t.
   '''

   t = Voice(scale(4))
   p = Spanner(t[ : ])

   "Spanner(c'8, d'8, e'8, f'8)"

   assert len(p.components) == 4
   assert p.components[0] is t[0]
   assert p.components[1] is t[1]
   assert p.components[2] is t[2]
   assert p.components[3] is t[3]

   assert len(t[0].spanners.mine( )) == 1
   assert len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.mine( )) == 1

   assert t[0].spanners.mine( )[0] is p
   assert t[1].spanners.mine( )[0] is p
   assert t[2].spanners.mine( )[0] is p
   assert t[3].spanners.mine( )[0] is p

   assert check(t)

   receipt = t[1].spanners.fracture('left')[0]
   source, left, right = receipt

   "(Spanner(c'8, d'8, e'8, f'8), Spanner(c'8), Spanner(d'8, e'8, f'8))"

   assert source is p
   assert left is not p

   assert len(left.components) == 1
   assert left.components[0] is t[0]
   assert len(t[0].spanners.mine( )) == 1
   assert t[0].spanners.mine( )[0] is left

   assert right is not p
   assert len(right.components) == 3
   assert right.components[0] is t[1]
   assert right.components[1] is t[2]
   assert right.components[2] is t[3]
   assert len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.mine( )) == 1
   assert t[1].spanners.mine( )[0] is right
   assert t[2].spanners.mine( )[0] is right
   assert t[3].spanners.mine( )[0] is right
   assert check(t)


def test_fracture_03( ):
   '''
   Fracture left of t[-1].

   Three-element receipt.
   Source spanner returns unaltered.
   'left' and 'right' parts return new spanners.
   'left' and 'right' parts partition components in t.
   '''

   t = Voice(scale(4))
   p = Spanner(t[ : ])

   "Spanner(c'8, d'8, e'8, f'8)"

   assert len(p.components) == 4

   assert p.components[0] is t[0]
   assert p.components[1] is t[1]
   assert p.components[2] is t[2]
   assert p.components[3] is t[3]

   assert len(t[0].spanners.mine( )) == 1
   assert len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.mine( )) == 1

   assert t[0].spanners.mine( )[0] is p
   assert t[1].spanners.mine( )[0] is p
   assert t[2].spanners.mine( )[0] is p
   assert t[3].spanners.mine( )[0] is p

   assert check(t)

   receipt = t[-1].spanners.fracture('left')[0]
   source, left, right = receipt

   "(Spanner(c'8, d'8, e'8, f'8), Spanner(c'8, d'8, e'8), Spanner(f'8))"

   assert source is p

   assert source.components[0] is t[0]
   assert source.components[1] is t[1]
   assert source.components[2] is t[2]
   assert source.components[3] is t[3]

   assert left is not p

   assert len(left.components) == 3
   assert left.components[0] is t[0]
   assert left.components[1] is t[1]
   assert left.components[2] is t[2]

   assert right is not p
   assert len(right.components) == 1
   assert right.components[0] is t[3]

   assert len(t[0].spanners.mine( )) == 1
   assert len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.mine( )) == 1

   assert t[0].spanners.mine( )[0] is left
   assert t[1].spanners.mine( )[0] is left
   assert t[2].spanners.mine( )[0] is left
   assert t[3].spanners.mine( )[0] is right

   assert check(t)


def test_fracture_04( ):
   '''
   Fracture right of t[0].
   '''

   t = Voice(scale(4))
   p = Spanner(t[ : ])

   "Spanner(c'8, d'8, e'8, f'8)"

   assert len(p.components) == 4
   assert p.components[0] is t[0]
   assert p.components[1] is t[1]
   assert p.components[2] is t[2]
   assert p.components[3] is t[3]

   assert len(t[0].spanners.mine( )) == 1
   assert len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.mine( )) == 1

   assert t[0].spanners.mine( )[0] is p
   assert t[1].spanners.mine( )[0] is p
   assert t[2].spanners.mine( )[0] is p
   assert t[3].spanners.mine( )[0] is p

   assert check(t)

   receipt = t[0].spanners.fracture('right')[0]
   source, left, right = receipt

   "(Spanner(c'8, d'8, e'8, f'8), Spanner(c'8), Spanner(d'8, e'8, f'8))"

   assert source is p
   assert len(source.components) == 4

   assert source.components[0] is t[0]
   assert source.components[1] is t[1]
   assert source.components[2] is t[2]
   assert source.components[3] is t[3]

   assert left is not p
   assert len(left.components) == 1

   assert left.components[0] is t[0]

   assert right is not p
   assert len(right.components) == 3

   assert right.components[0] is t[1]
   assert right.components[1] is t[2]
   assert right.components[2] is t[3]
   
   assert len(t[0].spanners.mine( )) == 1
   assert len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.mine( )) == 1

   assert t[0].spanners.mine( )[0] is left
   assert t[1].spanners.mine( )[0] is right
   assert t[2].spanners.mine( )[0] is right
   assert t[3].spanners.mine( )[0] is right

   assert check(t)


def test_fracture_05( ):
   '''
   Fracture right of t[1].
   '''

   t = Voice(scale(4))
   p = Spanner(t[ : ])

   "Spanner(c'8, d'8, e'8, f'8)"

   assert len(p.components) == 4

   assert p.components[0] is t[0]
   assert p.components[1] is t[1]
   assert p.components[2] is t[2]
   assert p.components[3] is t[3]

   assert len(t[0].spanners.mine( )) == 1
   assert len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.mine( )) == 1

   assert t[0].spanners.mine( )[0] is p
   assert t[1].spanners.mine( )[0] is p
   assert t[2].spanners.mine( )[0] is p
   assert t[3].spanners.mine( )[0] is p

   assert check(t)

   receipt = t[1].spanners.fracture('right')[0]
   source, left, right = receipt

   "(Spanner(c'8, d'8, e'8, f'8), Spanner(c'8, d'8), Spanner(e'8, f'8))"

   assert source is p
   assert len(source.components) == 4

   assert source.components[0] is t[0]
   assert source.components[1] is t[1]
   assert source.components[2] is t[2]
   assert source.components[3] is t[3]

   assert left is not p
   assert len(left.components) == 2

   assert left.components[0] is t[0]
   assert left.components[1] is t[1]

   assert right is not p
   assert len(right.components) == 2

   assert right.components[0] is t[2]
   assert right.components[1] is t[3]

   assert len(t[0].spanners.mine( )) == 1
   assert len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.mine( )) == 1

   assert t[0].spanners.mine( )[0] is left
   assert t[1].spanners.mine( )[0] is left
   assert t[2].spanners.mine( )[0] is right
   assert t[3].spanners.mine( )[0] is right

   assert check(t)


def test_fracture_06( ):
   '''
   Fracture right of t[-1].
   '''

   t = Voice(scale(4))
   p = Spanner(t[ : ])

   "Spanner(c'8, d'8, e'8, f'8)"

   assert len(p.components) == 4

   assert p.components[0] is t[0]
   assert p.components[1] is t[1]
   assert p.components[2] is t[2]
   assert p.components[3] is t[3]

   assert len(t[0].spanners.mine( )) == 1
   assert len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.mine( )) == 1

   assert t[0].spanners.mine( )[0] is p
   assert t[1].spanners.mine( )[0] is p
   assert t[2].spanners.mine( )[0] is p
   assert t[3].spanners.mine( )[0] is p

   assert check(t)

   receipt = t[-1].spanners.fracture('right')[0]
   source, left, right = receipt

   "(Spanner(c'8, d'8, e'8, f'8), Spanner(c'8, d'8, e'8, f'8), Spanner( ))"

   assert source is p

   assert source.components[0] is t[0]
   assert source.components[1] is t[1]
   assert source.components[2] is t[2]
   assert source.components[3] is t[3]

   assert left is not p
   assert len(left.components) == 4

   assert left.components[0] is t[0]
   assert left.components[1] is t[1]
   assert left.components[2] is t[2]
   assert left.components[3] is t[3]

   assert right is not p
   assert len(right.components) == 0

   assert len(t[0].spanners.mine( )) == 1
   assert len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.mine( )) == 1

   assert t[0].spanners.mine( )[0] is left
   assert t[1].spanners.mine( )[0] is left
   assert t[2].spanners.mine( )[0] is left
   assert t[3].spanners.mine( )[0] is left

   assert check(t)


def test_fracture_07( ):
   '''
   Fracture both sides of t[0].
   '''

   t = Voice(scale(4))
   p = Spanner(t[ : ])

   "Spanner(c'8, d'8, e'8, f'8)"

   assert len(p.components) == 4
   assert p.components[0] is t[0]
   assert p.components[1] is t[1]
   assert p.components[2] is t[2]
   assert p.components[3] is t[3]

   assert len(t[0].spanners.mine( )) == 1
   assert len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.mine( )) == 1

   assert t[0].spanners.mine( )[0] is p
   assert t[1].spanners.mine( )[0] is p
   assert t[2].spanners.mine( )[0] is p
   assert t[3].spanners.mine( )[0] is p

   assert check(t)

   receipt = t[0].spanners.fracture( )[0]
   source, left, center, right = receipt

   "(Spanner(c'8, d'8, e'8, f'8), Spanner( ), Spanner(c'8), Spanner(d'8, e'8, f'8))"

   assert source is p
   assert len(source.components) == 4

   assert source.components[0] is t[0]
   assert source.components[1] is t[1]
   assert source.components[2] is t[2]
   assert source.components[3] is t[3]

   assert left is not p
   assert len(left.components) == 0

   assert center is not p
   assert len(center.components) == 1

   assert center.components[0] is t[0]

   assert right is not p
   assert len(right.components) == 3

   assert right.components[0] is t[1]
   assert right.components[1] is t[2]
   assert right.components[2] is t[3]
   
   assert len(t[0].spanners.mine( )) == 1
   assert len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.mine( )) == 1

   assert t[0].spanners.mine( )[0] is center
   assert t[1].spanners.mine( )[0] is right
   assert t[2].spanners.mine( )[0] is right
   assert t[3].spanners.mine( )[0] is right

   assert check(t)


def test_fracture_08( ):
   '''
   Fracture both sides of t[1].
   '''

   t = Voice(scale(4))
   p = Spanner(t[ : ])

   "Spanner(c'8, d'8, e'8, f'8)"

   assert len(p.components) == 4

   assert p.components[0] is t[0]
   assert p.components[1] is t[1]
   assert p.components[2] is t[2]
   assert p.components[3] is t[3]

   assert len(t[0].spanners.mine( )) == 1
   assert len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.mine( )) == 1

   assert t[0].spanners.mine( )[0] is p
   assert t[1].spanners.mine( )[0] is p
   assert t[2].spanners.mine( )[0] is p
   assert t[3].spanners.mine( )[0] is p

   assert check(t)

   receipt = t[1].spanners.fracture( )[0]
   source, left, center, right = receipt

   "(Spanner(c'8, d'8, e'8, f'8), Spanner(c'8), Spanner(d'8), Spanner(e'8, f'8))"

   assert source is p
   assert len(source.components) == 4

   assert source.components[0] is t[0]
   assert source.components[1] is t[1]
   assert source.components[2] is t[2]
   assert source.components[3] is t[3]

   assert left is not p
   assert len(left.components) == 1

   assert left.components[0] is t[0]

   assert center is not p
   assert len(center.components) == 1
   
   assert center.components[0] is t[1]

   assert right is not p
   assert len(right.components) == 2

   assert right.components[0] is t[2]
   assert right.components[1] is t[3]

   assert len(t[0].spanners.mine( )) == 1
   assert len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.mine( )) == 1

   assert t[0].spanners.mine( )[0] is left
   assert t[1].spanners.mine( )[0] is center
   assert t[2].spanners.mine( )[0] is right
   assert t[3].spanners.mine( )[0] is right

   assert check(t)


def test_fracture_09( ):
   '''
   Fracture both sides of t[-1].
   '''

   t = Voice(scale(4))
   p = Spanner(t[ : ])

   "Spanner(c'8, d'8, e'8, f'8)"

   assert len(p.components) == 4

   assert p.components[0] is t[0]
   assert p.components[1] is t[1]
   assert p.components[2] is t[2]
   assert p.components[3] is t[3]

   assert len(t[0].spanners.mine( )) == 1
   assert len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.mine( )) == 1

   assert t[0].spanners.mine( )[0] is p
   assert t[1].spanners.mine( )[0] is p
   assert t[2].spanners.mine( )[0] is p
   assert t[3].spanners.mine( )[0] is p

   assert check(t)

   receipt = t[-1].spanners.fracture( )[0]
   source, left, center, right = receipt

   "(Spanner(c'8, d'8, e'8, f'8), Spanner(c'8, d'8, e'8), Spanner(f'8), Spanner( ))"

   assert source is p

   assert source.components[0] is t[0]
   assert source.components[1] is t[1]
   assert source.components[2] is t[2]
   assert source.components[3] is t[3]

   assert left is not p
   assert len(left.components) == 3

   assert left.components[0] is t[0]
   assert left.components[1] is t[1]
   assert left.components[2] is t[2]

   assert center is not p
   assert len(center.components) == 1

   assert center.components[0] is t[3]

   assert right is not p
   assert len(right.components) == 0

   assert len(t[0].spanners.mine( )) == 1
   assert len(t[1].spanners.mine( )) == 1
   assert len(t[2].spanners.mine( )) == 1
   assert len(t[3].spanners.mine( )) == 1

   assert t[0].spanners.mine( )[0] is left
   assert t[1].spanners.mine( )[0] is left
   assert t[2].spanners.mine( )[0] is left
   assert t[3].spanners.mine( )[0] is center

   assert check(t)


def test_fracture_10( ):
   '''
   Fracture multiple spanners to either side of some component.
   '''

   t = Voice(scale(4))
   p1 = Spanner(t[ : ])
   p2 = Spanner(t[ : ])

   "Spanner(c'8, d'8, e'8, f'8)"
   "Spanner(c'8, d'8, e'8, f'8)"

   assert p1 is not p2

   assert len(p1.components) == 4
   
   assert p1.components[0] is t[0]
   assert p1.components[1] is t[1]
   assert p1.components[2] is t[2]
   assert p1.components[3] is t[3]

   assert len(p2.components) == 4
   
   assert p2.components[0] is t[0]
   assert p2.components[1] is t[1]
   assert p2.components[2] is t[2]
   assert p2.components[3] is t[3]

   assert len(t[0].spanners.mine( )) == 2
   assert len(t[1].spanners.mine( )) == 2
   assert len(t[2].spanners.mine( )) == 2
   assert len(t[3].spanners.mine( )) == 2

   assert p1 in t[0].spanners.mine( )
   assert p1 in t[1].spanners.mine( )
   assert p1 in t[2].spanners.mine( )
   assert p1 in t[3].spanners.mine( )

   assert p2 in t[0].spanners.mine( )
   assert p2 in t[1].spanners.mine( )
   assert p2 in t[2].spanners.mine( )
   assert p2 in t[3].spanners.mine( )

   receipts = t[1].spanners.fracture( )

   '''
   [(Spanner(c'8, d'8, e'8, f'8), 
      Spanner(c'8), 
      Spanner(d'8), 
      Spanner(e'8, f'8)), 
   (Spanner(c'8, d'8, e'8, f'8), 
      Spanner(c'8), 
      Spanner(d'8), 
      Spanner(e'8, f'8))]
   '''

   first, second = receipts

   source, left, center, right = first

   assert source is p1
   assert len(source.components) == 4

   assert source.components[0] is t[0]
   assert source.components[1] is t[1]
   assert source.components[2] is t[2]
   assert source.components[3] is t[3]

   assert left is not p1
   assert len(left.components) == 1

   assert left.components[0] is t[0]

   assert center is not p1
   assert len(center.components) == 1

   assert center.components[0] is t[1]

   assert right is not p1
   assert len(right.components) == 2
   
   assert right.components[0] is t[2]
   assert right.components[1] is t[3]

   source, left, center, right = second

   assert source is p2
   assert len(source.components) == 4

   assert source.components[0] is t[0]
   assert source.components[1] is t[1]
   assert source.components[2] is t[2]
   assert source.components[3] is t[3]

   assert left is not p2
   assert len(left.components) == 1

   assert left.components[0] is t[0]

   assert center is not p2
   assert len(center.components) == 1

   assert center.components[0] is t[1]

   assert right is not p2
   assert len(right.components) == 2
   
   assert right.components[0] is t[2]
   assert right.components[1] is t[3]
