from abjad import *


def test_container_get_01( ):
   '''get( ) with single string argument searches names.'''
   t = Staff(Note(0 , (1,4)) *  4)
   n = t[0]
   n.name = 'notename'
   assert t.get('notename') == [n]


def test_container_get_02( ):
   '''get( ) can search class names.'''
   t = Staff(Note(0 , (1,4)) *  4)
   assert t.get(classtype = Note) == t[:]


def test_container_get_03( ):
   '''get( ) finds Components (nodes) matching both name and class name.'''
   t = Staff(Note(0 , (1,4)) *  4)
   n = t[0]
   n.name = 'notename'
   assert t.get(name = 'notename', classtype = Note) == [n]


def test_container_get_04( ):
   '''get( ) with no arguments returns all subnodes, including caller node.'''
   v1 = Voice([Note(i, (1,4)) for i in range(2)])
   v2 = Voice([Note(i, (1,4)) for i in range(2,4)])
   t = Staff([v1, v2])
   assert t.get( ) == [t, v1, v1[0], v1[1], v2, v2[0], v2[1]]


def test_container_get_05( ):
   '''get( ) returns all classes with given class name.'''
   v1 = Voice([Note(i, (1,4)) for i in range(2)])
   v2 = Voice([Note(i, (1,4)) for i in range(2,4)])
   t = Staff([v1, v2])
   assert t.get(classtype = Voice) == [v1, v2]


def test_container_get_06( ):
   '''get( ) searches for name in Context.invocation.'''
   v1 = Voice([Note(i, (1,4)) for i in range(2)])
   v2 = Voice([Note(i, (1,4)) for i in range(2,4)])
   v1.invocation.name = 'voiceOne'
   t = Staff([v1, v2])
   assert t.get('voiceOne') == [v1]


def test_container_get_07( ):
   '''get( ) can search class types for Contexts with invocation.'''
   v = Voice(Note(0 , (1, 4)) *  4) 
   v.invocation.type = 'MyStrangeVoice'
   t = Staff([v])
   assert t.get(classtype = 'MyStrangeVoice') == [v]


def test_container_get_08( ):
   '''get( ) can search both invocation names and class types in Contexts.'''
   v = Voice(Note(0 , (1,4)) *  4) 
   v.invocation.type = 'MyStrangeVoice'
   v.invocation.name = 'voice_1'
   t = Staff([v])
   assert t.get(name = 'voice_1', classtype = 'MyStrangeVoice') == [v]


def test_container_get_09( ):
   '''get( ) returns empty if either name or classtype does not match.'''
   v = Voice(Note(0 , (1,4)) *  4) 
   v.invocation.type = 'MyStrangeVoice'
   v.invocation.name = 'voice_1'
   t = Staff([v])
   assert t.get(name = 'voice_200', classtype = 'MyStrangeVoice') == [ ]


def test_container_get_10( ):
   '''Full test.'''
   vl1 = Voice([Note(i, (1,8)) for i in range(4)])
   vl1.invocation.name = 'low'
   vl2 = Voice([Note(i, (1,8)) for i in range(4,8)])
   vl2.invocation.name = 'low'
   vh1 = Voice([Note(i, (1,8)) for i in range(12,16)])
   vh1.invocation.name = 'high'
   vh2 = Voice([Note(i, (1,8)) for i in range(16,20)])
   vh2.invocation.name = 'high'

   s1 = Staff([vh1, vl1])
   s1.invocation.name = 'mystaff'
   s1.brackets = 'double-angle'
   s2 = Staff([vh2, vl2])
   s2.invocation.name = 'mystaff'
   s2.brackets = 'double-angle'

   fn = vl1[0] # first note
   fn.name = 'parangaricutirimicuaro'

   seq = Sequential([s1, s2])

   assert seq.get('parangaricutirimicuaro') == [fn]
   assert seq.get(name = 'parangaricutirimicuaro') == [fn]
   assert seq.get('mystaff') == [s1, s2]
   assert seq.get('low') == [vl1, vl2]
   assert seq.get('high') == [vh1, vh2]
   assert seq.get(classtype = Voice) == [vh1, vl1, vh2, vl2]
   assert seq.get(classtype = Voice, name = 'low') == [vl1, vl2]
   assert seq.get('nonexistent') == [ ]
