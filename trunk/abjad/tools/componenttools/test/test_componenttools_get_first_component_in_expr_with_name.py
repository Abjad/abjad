from abjad import *
import py.test


def test_componenttools_get_first_component_in_expr_with_name_01( ):
   '''Find components by name.'''

   t = Staff(macros.scale(4))
   n = t[0]
   n.name = 'notename'

   assert componenttools.get_first_component_in_expr_with_name(t, 'notename') == n


#def test_componenttools_get_first_component_in_expr_with_name_02( ):
#   '''Find components by class.'''
#
#   t = Staff(macros.scale(4))
#
#   #assert componenttools.get_first_component_in_expr_with_name(t, klass = Note) == tuple(t[:])
#   assert componenttools.get_first_component_in_expr_with_name(t, klass = Note) == t[0]


#def test_componenttools_get_first_component_in_expr_with_name_03( ):
#   '''Find components by both name and class.'''
#
#   t = Staff(macros.scale(4))
#   n = t[0]
#   n.name = 'notename'
#
#   #assert componenttools.get_first_component_in_expr_with_name(t, 'notename', Note) == (n, )
#   assert componenttools.get_first_component_in_expr_with_name(t, 'notename', Note) == n


#def test_componenttools_get_first_component_in_expr_with_name_04( ):
#   '''Return all nodes, including start node.'''
#
#   v1 = Voice([Note(i, (1, 4)) for i in range(2)])
#   v2 = Voice([Note(i, (1, 4)) for i in range(2, 4)])
#   t = Staff([v1, v2])
#
#   #assert componenttools.get_first_component_in_expr_with_name(t) == (t, v1, v1[0], v1[1], v2, v2[0], v2[1])
#   assert componenttools.get_first_component_in_expr_with_name(t) == t


#def test_componenttools_get_first_component_in_expr_with_name_05( ):
#   '''Find all class instances.'''
#
#   v1 = Voice([Note(i, (1, 4)) for i in range(2)])
#   v2 = Voice([Note(i, (1, 4)) for i in range(2, 4)])
#   t = Staff([v1, v2])
#
#   #assert componenttools.get_first_component_in_expr_with_name(t, klass = Voice) == (v1, v2)
#   assert componenttools.get_first_component_in_expr_with_name(t, klass = Voice) == v1


def test_componenttools_get_first_component_in_expr_with_name_06( ):
   '''Find by name.'''

   v1 = Voice([Note(i, (1, 4)) for i in range(2)])
   v2 = Voice([Note(i, (1, 4)) for i in range(2, 4)])
   v1.name = 'voiceOne'
   t = Staff([v1, v2])

   #assert componenttools.get_first_component_in_expr_with_name(t, name = 'voiceOne') == (v1, )
   assert componenttools.get_first_component_in_expr_with_name(t, name = 'voiceOne') == v1


#def test_componenttools_get_first_component_in_expr_with_name_07( ):
#   '''Find by context.'''
#
#   v = Voice(macros.scale(4))
#   v.context = 'MyStrangeVoice'
#   t = Staff([v])
#
#   #assert componenttools.get_first_component_in_expr_with_name(t, context = 'MyStrangeVoice') == (v, )
#   assert componenttools.get_first_component_in_expr_with_name(t, context = 'MyStrangeVoice') == v


#def test_componenttools_get_first_component_in_expr_with_name_08( ):
#   '''Find by both name and context.'''
#
#   v = Voice(macros.scale(4))
#   v.context = 'MyStrangeVoice'
#   v.name = 'voice_1'
#   t = Staff([v])
#
#   #assert componenttools.get_first_component_in_expr_with_name(t, name = 'voice_1', context = 'MyStrangeVoice') \
#   #   == (v, )
#   assert componenttools.get_first_component_in_expr_with_name(t, name = 'voice_1', context = 'MyStrangeVoice') \
#      == v


def test_componenttools_get_first_component_in_expr_with_name_09( ):
   '''Raise missing component error on no match.'''

   v = Voice(macros.scale(4))
   v.context = 'MyStrangeVoice'
   v.name = 'voice_1'
   t = Staff([v])

   assert py.test.raises(
      MissingComponentError, "componenttools.get_first_component_in_expr_with_name(t, name = 'voice_200')")


def test_componenttools_get_first_component_in_expr_with_name_10( ):
   '''Full test.'''

   vl1 = Voice([Note(i, (1, 8)) for i in range(4)])
   vl1.name = 'low'
   vl2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   vl2.name = 'low'
   vh1 = Voice([Note(i, (1, 8)) for i in range(12, 16)])
   vh1.name = 'high'
   vh2 = Voice([Note(i, (1, 8)) for i in range(16, 20)])
   vh2.name = 'high'

   s1 = Staff([vh1, vl1])
   s1.name = 'mystaff'
   s1.parallel = True
   s2 = Staff([vh2, vl2])
   s2.name = 'mystaff'
   s2.parallel = True

   fn = vl1[0]
   fn.name = 'parangaricutirimicuaro'

   seq = Container([s1, s2])

   assert componenttools.get_first_component_in_expr_with_name(seq, 'parangaricutirimicuaro') == fn
   assert componenttools.get_first_component_in_expr_with_name(seq, name = 'parangaricutirimicuaro') == fn
   assert componenttools.get_first_component_in_expr_with_name(seq, 'mystaff') == s1
   assert componenttools.get_first_component_in_expr_with_name(seq, 'low') == vl1
   assert componenttools.get_first_component_in_expr_with_name(seq, 'high') == vh1
   #assert componenttools.get_first_component_in_expr_with_name(seq, klass = Voice) == vh1
   #assert componenttools.get_first_component_in_expr_with_name(seq, klass = Voice, name = 'low') == vl1
   assert py.test.raises(
      MissingComponentError, "componenttools.get_first_component_in_expr_with_name(seq, 'nonexistent')")
