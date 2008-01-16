from types import ModuleType

from beam.spanner import Beam
from chord.chord import Chord
from dynamics.crescendo import Crescendo
from containers.container import Container
from dynamics.decrescendo import Decrescendo
from duration.duration import Duration
from tuplet.fdtuplet import FixedDurationTuplet
from tuplet.fmtuplet import FixedMultiplierTuplet
from glissando.spanner import Glissando
from dynamics.hairpin import Hairpin
from measure.measure import Measure
from note.note import Note
from octavation.spanner import Octavation
from override.spanner import Override
from containers.parallel import Parallel
from pitch.pitch import Pitch
from duration.rational import Rational
from rest.rest import Rest
from score.score import Score
from containers.sequential import Sequential
from skip.skip import Skip
from staff.staff import Staff
from voice.voice import Voice

from types import ModuleType

items = globals().items()
for key, value in items:
   if isinstance(value, ModuleType) and not key.startswith('_'):
      globals().pop(key)

del key, items, value, ModuleType

