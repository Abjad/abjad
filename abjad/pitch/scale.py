import re

from ..selectx import Selection
from ..sequence import Sequence
from ..storage import FormatSpecification, StorageFormatManager
from .Accidental import Accidental
from .PitchRange import PitchRange
from .intervalclasses import NamedInversionEquivalentIntervalClass
from .intervals import NamedInterval
from .pitchclasses import NamedPitchClass
from .pitches import NamedPitch
from .segments import IntervalClassSegment, PitchClassSegment, PitchSegment
from .sets import PitchSet


class ScaleDegree:
    """
    Scale degree.

    ..  container:: example

        >>> abjad.ScaleDegree('#4')
        ScaleDegree('#4')

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_accidental", "_number")

    _acceptable_numbers = tuple(range(1, 16))

    _numeral_to_number_name = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
        11: "eleven",
        12: "twelve",
        13: "thirteen",
        14: "fourteen",
        15: "fifteen",
    }

    _roman_numeral_string_to_scale_degree_number = {
        "I": 1,
        "II": 2,
        "III": 3,
        "IV": 4,
        "V": 5,
        "VI": 6,
        "VII": 7,
    }

    _scale_degree_number_to_roman_numeral_string = {
        1: "I",
        2: "II",
        3: "III",
        4: "IV",
        5: "V",
        6: "VI",
        7: "VII",
    }

    _scale_degree_number_to_scale_degree_name = {
        1: "tonic",
        2: "superdominant",
        3: "mediant",
        4: "subdominant",
        5: "dominant",
        6: "submediant",
        7: "leading tone",
    }

    _string_regex = re.compile(r"([#|b]*)([i|I|v|V|\d]+)")

    ### INITIALIZER ###

    def __init__(self, string=1):
        assert isinstance(string, (str, int, type(self))), repr(string)
        string = str(string)
        match = self._string_regex.match(string)
        if match is None:
            raise Exception(repr(string))
        groups = match.groups()
        accidental, roman_numeral = groups
        accidental = Accidental(accidental)
        roman_numeral = roman_numeral.upper()
        try:
            number = self._roman_numeral_string_to_scale_degree_number[roman_numeral]
        except KeyError:
            number = int(roman_numeral)
        self._accidental = accidental
        self._number = number

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a scale degree with number and
        accidental equal to those of this scale degree.

        ..  container:: example

            >>> degree_1 = abjad.ScaleDegree('#4')
            >>> degree_2 = abjad.ScaleDegree('#4')
            >>> degree_3 = abjad.ScaleDegree(5)

            >>> degree_1 == degree_1
            True
            >>> degree_1 == degree_2
            True
            >>> degree_1 == degree_3
            False

            >>> degree_2 == degree_1
            True
            >>> degree_2 == degree_2
            True
            >>> degree_2 == degree_3
            False

            >>> degree_3 == degree_1
            False
            >>> degree_3 == degree_2
            False
            >>> degree_3 == degree_3
            True

        Returns true or false.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self):
        """
        Hashes scale degree.

        Returns integer.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self):
        """
        Gets string representation of scale degree.

        ..  container:: example

            >>> str(abjad.ScaleDegree('#4'))
            '#4'

        Returns string.
        """
        return f"{self.accidental.symbol}{self.number}"

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.string]
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
        )

    ### PUBLIC METHODS ###

    @staticmethod
    def from_accidental_and_number(accidental, number):
        """
        Makes scale degree from ``accidental`` and ``number``.

        ..  container:: example

            >>> class_ = abjad.ScaleDegree
            >>> class_.from_accidental_and_number('sharp', 4)
            ScaleDegree('#4')

        Returns new scale degree.
        """
        accidental = Accidental(accidental)
        string = f"{accidental.symbol}{number}"
        return ScaleDegree(string=string)

    ### PUBLIC PROPERTIES ###

    @property
    def accidental(self):
        """
        Gets accidental.

        ..  container:: example

            >>> abjad.ScaleDegree('#4').accidental
            Accidental('sharp')

        Returns accidental.
        """
        return self._accidental

    @property
    def name(self):
        """
        Gets name.

        ..  container:: example

            >>> abjad.ScaleDegree(1).name
            'tonic'
            >>> abjad.ScaleDegree(2).name
            'superdominant'
            >>> abjad.ScaleDegree(3).name
            'mediant'
            >>> abjad.ScaleDegree(4).name
            'subdominant'
            >>> abjad.ScaleDegree(5).name
            'dominant'
            >>> abjad.ScaleDegree(6).name
            'submediant'
            >>> abjad.ScaleDegree(7).name
            'leading tone'

        Returns string.
        """
        if self.accidental.semitones == 0:
            return self._scale_degree_number_to_scale_degree_name[self.number]
        else:
            raise NotImplementedError

    @property
    def number(self):
        """
        Gets number.

        ..  container:: example

            >>> abjad.ScaleDegree('#4').number
            4

        Returns integer from 1 to 7, inclusive.
        """
        return self._number

    @property
    def roman_numeral_string(self):
        """
        Gets Roman numeral string.

        ..  container:: example

            >>> degree = abjad.ScaleDegree('#4')
            >>> degree.roman_numeral_string
            'IV'

        Returns string.
        """
        string = self._scale_degree_number_to_roman_numeral_string[self.number]
        return string

    @property
    def string(self):
        """
        Gets string.

        ..  container:: example

            >>> abjad.ScaleDegree('b4').string
            'b4'

            >>> abjad.ScaleDegree('4').string
            '4'

            >>> abjad.ScaleDegree('#4').string
            '#4'

        Returns string.
        """
        return f"{self.accidental.symbol}{self.number}"

    @property
    def title_string(self):
        """
        Gets title string.

        ..  container:: example

            >>> abjad.ScaleDegree('b4').title_string
            'FlatFour'

            >>> abjad.ScaleDegree('4').title_string
            'Four'

            >>> abjad.ScaleDegree('#4').title_string
            'SharpFour'

        Returns string.
        """
        if not self.accidental.name == "natural":
            accidental = self.accidental.name
        else:
            accidental = ""
        number = self._numeral_to_number_name[self.number]
        return f"{accidental.title()}{number.title()}"


class Scale(PitchClassSegment):
    """
    Scale.

    ..  container:: example

        Initializes from pair:

        >>> abjad.Scale(('c', 'minor'))
        Scale("c d ef f g af bf")

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_key_signature",)

    ### INITIALIZER ###

    def __init__(self, key_signature=None):
        from ..indicators.KeySignature import KeySignature

        if key_signature is None:
            key_signature = KeySignature("c", "major")
        elif isinstance(key_signature, tuple):
            key_signature = KeySignature(*key_signature)
        elif isinstance(key_signature, type(self)):
            key_signature = key_signature.key_signature
        if not isinstance(key_signature, KeySignature):
            raise Exception(key_signature)
        npcs = [key_signature.tonic]
        for mdi in key_signature.mode.named_interval_segment[:-1]:
            named_pitch_class = npcs[-1] + mdi
            npcs.append(named_pitch_class)
        PitchClassSegment.__init__(self, items=npcs, item_class=NamedPitchClass)
        self._key_signature = key_signature

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        """
        Gets item in scale.

        Returns pitch-class segment.
        """
        segment = PitchClassSegment(self)
        return segment.__getitem__(argument)

    ### PRIVATE PROPERTIES ###

    @property
    def _capital_name(self):
        letter = str(self.key_signature.tonic).title()
        mode = self.key_signature.mode.mode_name.title()
        return f"{letter}{mode}"

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=[
                str(self.key_signature.tonic),
                self.key_signature.mode.mode_name,
            ],
        )

    def _set_ascending_named_diatonic_pitches_on_logical_ties(self, argument):
        dicg = self.named_interval_class_segment
        length = len(dicg)
        octave_number = 4
        pitch = NamedPitch((self[0].name, octave_number))
        for i, logical_tie in enumerate(Selection(argument).logical_ties()):
            if hasattr(logical_tie[0], "written_pitch"):
                for note in logical_tie:
                    note.written_pitch = pitch
            elif hasattr(logical_tie[0], "written_pitches"):
                for chord in logical_tie:
                    chord.written_pitches = [pitch]
            else:
                pass
            dic = dicg[i % length]
            ascending_mdi = NamedInterval((dic.quality, dic.number))
            pitch += ascending_mdi

    ### PUBLIC PROPERTIES ###

    @property
    def dominant(self):
        """
        Gets dominant.

        ..  container:: example

            >>> abjad.Scale(('c', 'minor')).dominant
            NamedPitchClass('g')

        Return pitch-class.
        """
        return self[4]

    @property
    def key_signature(self):
        """
        Gets key signature.

        ..  container:: example

            >>> abjad.Scale(('c', 'minor')).key_signature
            KeySignature(NamedPitchClass('c'), Mode('minor'))

        Returns key signature.
        """
        return self._key_signature

    @property
    def leading_tone(self):
        """
        Gets leading tone.

        ..  container:: example

            >>> abjad.Scale(('c', 'minor')).leading_tone
            NamedPitchClass('bf')

        Returns pitch-class.
        """
        return self[-1]

    @property
    def mediant(self):
        """
        Gets mediant.

        ..  container:: example

            >>> abjad.Scale(('c', 'minor')).mediant
            NamedPitchClass('ef')

        Returns pitch-class.
        """
        return self[2]

    @property
    def named_interval_class_segment(self):
        """
        Gets named interval class segment.

        ..  container:: example

            >>> scale = abjad.Scale(('c', 'minor'))
            >>> str(scale.named_interval_class_segment)
            '<+M2, +m2, +M2, +M2, +m2, +M2, +M2>'

            >>> scale = abjad.Scale(('d', 'dorian'))
            >>> str(scale.named_interval_class_segment)
            '<+M2, +m2, +M2, +M2, +M2, +m2, +M2>'

        Returns interval-class segment.
        """
        dics = []
        for left, right in Sequence(self).nwise(wrapped=True):
            dic = left - right
            dics.append(dic)
        dicg = IntervalClassSegment(
            items=dics, item_class=NamedInversionEquivalentIntervalClass
        )
        return dicg

    @property
    def subdominant(self):
        """
        Gets subdominant.

        ..  container:: example

            >>> abjad.Scale(('c', 'minor')).subdominant
            NamedPitchClass('f')

        Returns pitch-class.
        """
        return self[3]

    @property
    def submediant(self):
        """
        Submediate of scale.

        ..  container:: example

            >>> abjad.Scale(('c', 'minor')).submediant
            NamedPitchClass('af')

        Returns pitch-class.
        """
        return self[5]

    @property
    def superdominant(self):
        """
        Gets superdominant.

        ..  container:: example

            >>> abjad.Scale(('c', 'minor')).superdominant
            NamedPitchClass('d')

        Returns pitch-class.
        """
        return self[1]

    @property
    def tonic(self):
        """
        Gets tonic.

        ..  container:: example

            >>> abjad.Scale(('c', 'minor')).tonic
            NamedPitchClass('c')

        Returns pitch-class.
        """
        return self[0]

    ### PUBLIC METHODS ###

    def create_named_pitch_set_in_pitch_range(self, pitch_range):
        """
        Creates named pitch-set in ``pitch_range``.

        Returns pitch-set.
        """
        if not isinstance(pitch_range, PitchRange):
            pitch_range = PitchRange(
                float(NamedPitch(pitch_range[0])),
                float(NamedPitch(pitch_range[1])),
            )
        low = pitch_range.start_pitch.octave.number
        high = pitch_range.stop_pitch.octave.number
        pitches = []
        octave = low
        while octave <= high:
            for x in self:
                pitch = NamedPitch((x.name, octave))
                if pitch_range.start_pitch <= pitch and pitch <= pitch_range.stop_pitch:
                    pitches.append(pitch)
            octave += 1
        return PitchSet(items=pitches, item_class=NamedPitch)

    @classmethod
    def from_selection(class_, selection, item_class=None, name=None):
        """
        Makes scale from ``selection``.

        Returns new scale.
        """
        raise NotImplementedError

    def named_pitch_class_to_scale_degree(self, pitch_class):
        """
        Changes named ``pitch_class`` to scale degree.

        ..  container:: example

            >>> scale = abjad.Scale(('c', 'major'))
            >>> scale.named_pitch_class_to_scale_degree('c')
            ScaleDegree('1')
            >>> scale.named_pitch_class_to_scale_degree('d')
            ScaleDegree('2')
            >>> scale.named_pitch_class_to_scale_degree('e')
            ScaleDegree('3')
            >>> scale.named_pitch_class_to_scale_degree('f')
            ScaleDegree('4')
            >>> scale.named_pitch_class_to_scale_degree('g')
            ScaleDegree('5')
            >>> scale.named_pitch_class_to_scale_degree('a')
            ScaleDegree('6')
            >>> scale.named_pitch_class_to_scale_degree('b')
            ScaleDegree('7')

            >>> scale.named_pitch_class_to_scale_degree('df')
            ScaleDegree('b2')

        Returns scale degree.
        """
        foreign_pitch_class = NamedPitchClass(pitch_class)
        letter = foreign_pitch_class._get_diatonic_pc_name()
        for i, pc in enumerate(self):
            if pc._get_diatonic_pc_name() == letter:
                native_pitch_class = pc
                scale_degree_index = i
                number = scale_degree_index + 1
                break
        native_pitch = NamedPitch((native_pitch_class.name, 4))
        foreign_pitch = NamedPitch((foreign_pitch_class.name, 4))
        accidental = foreign_pitch.accidental - native_pitch.accidental
        scale_degree = ScaleDegree.from_accidental_and_number(accidental, number)
        return scale_degree

    def scale_degree_to_named_pitch_class(self, scale_degree):
        """
        Changes scale degree to named pitch-class.

        ..  container:: example

            >>> scale = abjad.Scale(('c', 'major'))
            >>> scale.scale_degree_to_named_pitch_class('1')
            NamedPitchClass('c')
            >>> scale.scale_degree_to_named_pitch_class('2')
            NamedPitchClass('d')
            >>> scale.scale_degree_to_named_pitch_class('3')
            NamedPitchClass('e')
            >>> scale.scale_degree_to_named_pitch_class('4')
            NamedPitchClass('f')
            >>> scale.scale_degree_to_named_pitch_class('5')
            NamedPitchClass('g')
            >>> scale.scale_degree_to_named_pitch_class('6')
            NamedPitchClass('a')
            >>> scale.scale_degree_to_named_pitch_class('7')
            NamedPitchClass('b')

            >>> scale.scale_degree_to_named_pitch_class('b2')
            NamedPitchClass('df')

        Returns named pitch-class.
        """
        scale_degree = ScaleDegree(scale_degree)
        scale_index = (scale_degree.number - 1) % 7
        pitch_class = self[scale_index]
        pitch_class = scale_degree.accidental(pitch_class)
        return pitch_class

    def voice_scale_degrees_in_open_position(self, scale_degrees):
        r"""
        Voices ``scale_degrees`` in open position.

        ..  container:: example

            >>> scale = abjad.Scale(('c', 'major'))
            >>> scale_degrees = [1, 3, 'b5', 7, '#9']
            >>> segment = scale.voice_scale_degrees_in_open_position(
            ...     scale_degrees)
            >>> segment
            PitchSegment("c' e' gf' b' ds''")

        Return pitch segment.
        """
        scale_degrees = [ScaleDegree(x) for x in scale_degrees]
        pitch_classes = [
            self.scale_degree_to_named_pitch_class(x) for x in scale_degrees
        ]
        pitches = [NamedPitch(pitch_classes[0])]
        for pitch_class in pitch_classes[1:]:
            pitch = NamedPitch(pitch_class)
            while pitch < pitches[-1]:
                pitch += 12
            pitches.append(pitch)
        pitches = PitchSegment(pitches)
        return pitches
