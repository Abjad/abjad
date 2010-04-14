from abjad import *


def test_Scale_named_pitch_class_to_scale_degree_01( ):

   scale = tonalharmony.Scale('c', 'major')

   assert scale.named_pitch_class_to_scale_degree('c') == \
      tonalharmony.ScaleDegree(1)
   assert scale.named_pitch_class_to_scale_degree('d') == \
      tonalharmony.ScaleDegree(2)
   assert scale.named_pitch_class_to_scale_degree('e') == \
      tonalharmony.ScaleDegree(3)
   assert scale.named_pitch_class_to_scale_degree('f') == \
      tonalharmony.ScaleDegree(4)
   assert scale.named_pitch_class_to_scale_degree('g') == \
      tonalharmony.ScaleDegree(5)
   assert scale.named_pitch_class_to_scale_degree('a') == \
      tonalharmony.ScaleDegree(6)
   assert scale.named_pitch_class_to_scale_degree('b') == \
      tonalharmony.ScaleDegree(7)


def test_Scale_named_pitch_class_to_scale_degree_02( ):

   scale = tonalharmony.Scale('c', 'major')

   assert scale.named_pitch_class_to_scale_degree('cf') == \
      tonalharmony.ScaleDegree('flat', 1)
   assert scale.named_pitch_class_to_scale_degree('df') == \
      tonalharmony.ScaleDegree('flat', 2)
   assert scale.named_pitch_class_to_scale_degree('ef') == \
      tonalharmony.ScaleDegree('flat', 3)
   assert scale.named_pitch_class_to_scale_degree('ff') == \
      tonalharmony.ScaleDegree('flat', 4)
   assert scale.named_pitch_class_to_scale_degree('gf') == \
      tonalharmony.ScaleDegree('flat', 5)
   assert scale.named_pitch_class_to_scale_degree('af') == \
      tonalharmony.ScaleDegree('flat', 6)
   assert scale.named_pitch_class_to_scale_degree('bf') == \
      tonalharmony.ScaleDegree('flat', 7)


def test_Scale_named_pitch_class_to_scale_degree_03( ):

   scale = tonalharmony.Scale('c', 'major')

   assert scale.named_pitch_class_to_scale_degree('cs') == \
      tonalharmony.ScaleDegree('sharp', 1)
   assert scale.named_pitch_class_to_scale_degree('ds') == \
      tonalharmony.ScaleDegree('sharp', 2)
   assert scale.named_pitch_class_to_scale_degree('es') == \
      tonalharmony.ScaleDegree('sharp', 3)
   assert scale.named_pitch_class_to_scale_degree('fs') == \
      tonalharmony.ScaleDegree('sharp', 4)
   assert scale.named_pitch_class_to_scale_degree('gs') == \
      tonalharmony.ScaleDegree('sharp', 5)
   assert scale.named_pitch_class_to_scale_degree('as') == \
      tonalharmony.ScaleDegree('sharp', 6)
   assert scale.named_pitch_class_to_scale_degree('bs') == \
      tonalharmony.ScaleDegree('sharp', 7)
