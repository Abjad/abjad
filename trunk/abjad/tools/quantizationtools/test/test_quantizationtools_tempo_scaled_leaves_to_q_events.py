from abjad import Chord
from abjad import Note
from abjad import Rest
from abjad import Staff
from abjad.tools.contexttools import TempoMark
from abjad.tools.durtools import Duration
from abjad.tools.durtools import Offset
from abjad.tools.quantizationtools import QEvent
from abjad.tools.quantizationtools import tempo_scaled_leaves_to_q_events
from abjad.tools.skiptools import Skip
from abjad.tools.tietools import TieSpanner


def test_quantizationtools_tempo_scaled_leaves_to_q_events_01( ):

   staff = Staff([ ])

   staff.append(Note(0, (1, 4)))
   staff.append(Rest((1, 4)))
   staff.append(Rest((1, 8)))
   staff.append(Note(1, (1, 8)))
   staff.append(Note(1, (1, 8)))
   staff.append(Note(2, (1, 8)))
   staff.append(Note(2, (1, 8)))
   staff.append(Note(3, (1, 8)))
   staff.append(Skip((1, 4)))
   staff.append(Rest((1, 4)))
   staff.append(Note(3, (1, 8)))
   staff.append(Chord([0, 1, 4], (1, 4)))

   TieSpanner(staff[3:5])
   TieSpanner(staff[5:7])
   TieSpanner(staff[7:11])

   tempo = TempoMark((1, 4), 55)

   q_events = tempo_scaled_leaves_to_q_events(staff.leaves, tempo)

   assert q_events == [
      QEvent(Offset(0, 1), Duration(12000, 11), 0),
      QEvent(Offset(12000, 11), Duration(18000, 11), None),
      QEvent(Offset(30000, 11), Duration(12000, 11), 1),
      QEvent(Offset(42000, 11), Duration(12000, 11), 2),
      QEvent(Offset(54000, 11), Duration(6000, 11), 3),
      QEvent(Offset(60000, 11), Duration(24000, 11), None),
      QEvent(Offset(84000, 11), Duration(6000, 11), 3),
      QEvent(Offset(90000, 11), Duration(12000, 11), (0, 1, 4))]


def test_quantizationtools_tempo_scaled_leaves_to_q_events_02( ):
      
   staff = Staff([ ])
      
   staff.append(Note(0, (1, 4)))
   staff.append(Rest((1, 4)))
   staff.append(Rest((1, 8)))
   staff.append(Note(1, (1, 8)))
   staff.append(Note(1, (1, 8)))
   staff.append(Note(2, (1, 8)))
   staff.append(Note(2, (1, 8)))
   staff.append(Note(3, (1, 8)))
   staff.append(Skip((1, 4)))
   staff.append(Rest((1, 4)))
   staff.append(Note(3, (1, 8)))
   staff.append(Chord([0, 1, 4], (1, 4)))

   TieSpanner(staff[3:5])
   TieSpanner(staff[5:7])
   TieSpanner(staff[7:11])

   TempoMark((1, 4), 58, target_context = Staff)(staff[0])
   TempoMark((1, 4), 77, target_context = Staff)(staff[9])

   q_events = tempo_scaled_leaves_to_q_events(staff.leaves)

   assert q_events == [
      QEvent(Offset(0, 1), Duration(30000, 29), 0),
      QEvent(Offset(30000, 29), Duration(45000, 29), None),
      QEvent(Offset(75000, 29), Duration(30000, 29), 1),
      QEvent(Offset(105000, 29), Duration(30000, 29), 2),
      QEvent(Offset(135000, 29), Duration(15000, 29), 3),
      QEvent(Offset(150000, 29), Duration(4050000, 2233), None),
      QEvent(Offset(15600000, 2233), Duration(30000, 77), 3),
      QEvent(Offset(16470000, 2233), Duration(60000, 77), (0, 1, 4))]
