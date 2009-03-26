from abjad import *


def test_find_01( ):
   '''Find components by name.'''

   t = Staff(scale(4))
   n = t[0]
   n.name = 'notename'

   assert find(t, 'notename') == [n]


def test_find_02( ):
   '''Find components by class.'''

   t = Staff(scale(4))

   assert find(t, klass = Note) == t[:]


def test_find_03( ):
   '''Find components by both name and class.'''

   t = Staff(scale(4))
   n = t[0]
   n.name = 'notename'

   assert find(t, 'notename', Note) == [n]


def test_find_04( ):
   '''Return all nodes, including start node.'''

   v1 = Voice([Note(i, (1, 4)) for i in range(2)])
   v2 = Voice([Note(i, (1, 4)) for i in range(2, 4)])
   t = Staff([v1, v2])

   assert find(t) == [t, v1, v1[0], v1[1], v2, v2[0], v2[1]]


def test_find_05( ):
   '''Find all class instances.'''

   v1 = Voice([Note(i, (1,4)) for i in range(2)])
   v2 = Voice([Note(i, (1,4)) for i in range(2,4)])
   t = Staff([v1, v2])

   assert find(t, klass = Voice) == [v1, v2]


def test_find_06( ):
   '''Find by invocation name.'''

   v1 = Voice([Note(i, (1,4)) for i in range(2)])
   v2 = Voice([Note(i, (1,4)) for i in range(2,4)])
   v1.invocation.name = 'voiceOne'
   t = Staff([v1, v2])

   assert find(t, name = 'voiceOne') == [v1]


def test_find_07( ):
   '''Find by invocation type.'''

   v = Voice(scale(4))
   v.invocation.type = 'MyStrangeVoice'
   t = Staff([v])

   assert find(t, klass = 'MyStrangeVoice') == [v]


def test_find_08( ):
   '''Find by both invocation name and invocation type.'''

   v = Voice(scale(4))
   v.invocation.type = 'MyStrangeVoice'
   v.invocation.name = 'voice_1'
   t = Staff([v])

   assert find(t, name = 'voice_1', klass = 'MyStrangeVoice') == [v]


def test_find_09( ):
   '''Return empty list on no match.'''

   v = Voice(scale(4))
   v.invocation.type = 'MyStrangeVoice'
   v.invocation.name = 'voice_1'
   t = Staff([v])

   assert find(t, name = 'voice_200', klass = 'MyStrangeVoice') == [ ]


def test_find_10( ):
   '''Full test.'''

   vl1 = Voice([Note(i, (1, 8)) for i in range(4)])
   vl1.invocation.name = 'low'
   vl2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   vl2.invocation.name = 'low'
   vh1 = Voice([Note(i, (1, 8)) for i in range(12, 16)])
   vh1.invocation.name = 'high'
   vh2 = Voice([Note(i, (1, 8)) for i in range(16, 20)])
   vh2.invocation.name = 'high'

   s1 = Staff([vh1, vl1])
   s1.invocation.name = 'mystaff'
   #s1.brackets = 'double-angle'
   s1.parallel = True
   s2 = Staff([vh2, vl2])
   s2.invocation.name = 'mystaff'
   #s2.brackets = 'double-angle'
   s2.parallel = True

   fn = vl1[0]
   fn.name = 'parangaricutirimicuaro'

   seq = Sequential([s1, s2])

   assert find(seq, 'parangaricutirimicuaro') == [fn]
   assert find(seq, name = 'parangaricutirimicuaro') == [fn]
   assert find(seq, 'mystaff') == [s1, s2]
   assert find(seq, 'low') == [vl1, vl2]
   assert find(seq, 'high') == [vh1, vh2]
   assert find(seq, klass = Voice) == [vh1, vl1, vh2, vl2]
   assert find(seq, klass = Voice, name = 'low') == [vl1, vl2]
   assert find(seq, 'nonexistent') == [ ]
