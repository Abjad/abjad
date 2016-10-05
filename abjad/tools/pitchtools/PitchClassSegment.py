# -* coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.pitchtools.Segment import Segment
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import new


class PitchClassSegment(Segment):
    r'''Pitch-class segment.

    ..  container:: example

        Numbered segment:

        ::

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = pitchtools.PitchClassSegment(items=items)
            >>> show(segment) # doctest: +SKIP

        ..  doctest::

            >>> lilypond_file = segment.__illustrate__()
            >>> f(lilypond_file._get_first_voice())
            \new Voice {
                bf'8
                bqf'8
                fs'8
                g'8
                bqf'8
                g'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

    ..  container:: example

        Named segment:

        ::

            >>> items = ['c', 'ef', 'bqs,', 'd']
            >>> segment = pitchtools.PitchClassSegment(
            ...     items=items,
            ...     item_class=pitchtools.NamedPitchClass,
            ...     )
            >>> show(segment) # doctest: +SKIP

        ..  doctest::

            >>> lilypond_file = segment.__illustrate__()
            >>> f(lilypond_file._get_first_voice())
            \new Voice {
                c'8
                ef'8
                bqs'8
                d'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }

    ..  container:: example

        Interpreter representation:

        ::

            >>> segment
            PitchClassSegment(['c', 'ef', 'bqs', 'd'])

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        item_class=None,
        ):
        if not items and not item_class:
            item_class = self._named_item_class
        Segment.__init__(
            self,
            items=items,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        r'''Gets `i` from segment.

        ..  container:: example

            Example segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

        ..  container:: example

            Gets item at nonnegative index:

            ::

                >>> segment[0]
                NumberedPitchClass(10)

        ..  container:: example

            Gets item at negative index:

            ::

                >>> segment[-1]
                NumberedPitchClass(7)
                
        ..  container:: example

            Gets slice:

            ::

                >>> segment[:4]
                PitchClassSegment([10, 10.5, 6, 7])

        ..  container:: example

            Returns pitch-class or pitch-class segment segment:

            ::

                >>> isinstance(segment[:4], pitchtools.PitchClassSegment)
                True

        '''
        superclass = super(PitchClassSegment, self)
        return superclass.__getitem__(i)

    def __illustrate__(self, **kwargs):
        r'''Illustrates segment.

        ..  container:: example

            Illustrates numbered segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Illustrates named segment:

            ::

                >>> items = ['c', 'ef', 'bqs,', 'd']
                >>> segment = pitchtools.PitchClassSegment(
                ...     items=items,
                ...     item_class=pitchtools.NumberedPitchClass,
                ...     )
                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    c'8
                    ef'8
                    bqs'8
                    d'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns LilyPond file:

            ::

                >>> isinstance(segment.__illustrate__(), lilypondfiletools.LilyPondFile)
                True

        '''
        superclass = super(PitchClassSegment, self)
        return superclass.__illustrate__(**kwargs)

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedPitchClass

    @property
    def _numbered_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitchClass

    @property
    def _parent_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.PitchClass

    ### PRIVATE METHODS ###

    def _is_equivalent_under_transposition(self, expr):
        r'''Is true when `expr` is equivalent to segment under transposition.
        
        Otherwise False.

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        if not isinstance(expr, type(self)):
            return False
        if not len(self) == len(expr):
            return False
        difference = -(pitchtools.NamedPitch(expr[0], 4) -
            pitchtools.NamedPitch(self[0], 4))
        new_pitch_classes = (x + difference for x in self)
        new_pitch_classes = new(self, items=new_pitch_classes)
        return expr == new_pitch_classes

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        r'''Gets item class of segment.

        ..  container:: example

            Gets item class of numbered segment:
        
            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

            ::

                >>> segment.item_class
                <class 'abjad.tools.pitchtools.NumberedPitchClass.NumberedPitchClass'>

        ..  container:: example


            Gets item class of named segment:

            ::

                >>> items = ['c', 'ef', 'bqs,', 'd']
                >>> segment = pitchtools.PitchClassSegment(
                ...     items=items,
                ...     item_class=pitchtools.NamedPitchClass,
                ...     )
                >>> show(segment) # doctest: +SKIP

            ::
                
                >>> segment.item_class
                <class 'abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass'>

        ..  container:: example

            Returns class:

            ::

                >>> type(segment.item_class)
                <class 'abc.ABCMeta'>

        '''
        superclass = super(PitchClassSegment, self)
        return superclass.item_class

    @property
    def items(self):
        r'''Gets items in segment.

        ..  container:: example

            Gets items in numbered segment:
        
            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

            ::

                >>> for item in segment.items:
                ...     item
                NumberedPitchClass(10)
                NumberedPitchClass(10.5)
                NumberedPitchClass(6)
                NumberedPitchClass(7)
                NumberedPitchClass(10.5)
                NumberedPitchClass(7)

        ..  container:: example

            Gets items in named segment:

            ::

                >>> items = ['c', 'ef', 'bqs,', 'd']
                >>> segment = pitchtools.PitchClassSegment(
                ...     items=items,
                ...     item_class=pitchtools.NamedPitchClass,
                ...     )
                >>> show(segment) # doctest: +SKIP

            ::
                
                >>> for item in segment.items:
                ...     item
                NamedPitchClass('c')
                NamedPitchClass('ef')
                NamedPitchClass('bqs')
                NamedPitchClass('d')

        ..  container:: example

            Returns list:

            ::

                >>> isinstance(segment.items, list)
                True

        '''
        superclass = super(PitchClassSegment, self)
        return superclass.items

    ### PUBLIC METHODS ###

    def alpha(self):
        r'''Gets alpha transform of segment.

        ..  container:: example

            Example segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

        ..  container:: example

            Gets alpha transform of segment:

            ::

                >>> segment_ = segment.alpha()
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    b'8
                    bqs'8
                    g'8
                    fs'8
                    bqs'8
                    fs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: Example

            Gets alpha transform of alpha transform of segment:

            ::

                >>> segment_ = segment.alpha().alpha()
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            ::

                >>> segment_ == segment
                True

        ..  container:: example

            Returns pitch-class segment:

            ::

                >>> isinstance(segment_, pitchtools.PitchClassSegment)
                True

        '''
        numbers = []
        for pc in self:
            pc = abs(float(pc))
            is_integer = True
            if not mathtools.is_integer_equivalent_number(pc):
                is_integer = False
                fraction_part = pc - int(pc)
                pc = int(pc)
            if abs(pc) % 2 == 0:
                number = (abs(pc) + 1) % 12
            else:
                number = abs(pc) - 1
            if not is_integer:
                number += fraction_part
            else:
                number = int(number)
            numbers.append(number)
        return new(self, items=numbers)

    def count(self, item):
        r'''Counts `item` in segment.

        ..  container:: example

            Example segment:
        
            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

        ..  container:: example

            Counts existing item in segment:

            ::
                
                >>> segment.count(-1.5)
                2

        ..  container:: example

            Counts nonexisting item in segment:

            ::
                
                >>> segment.count('text')
                0

        ..  container:: example

            Returns nonnegative integer:

            ::

                >>> isinstance(segment.count('text'), int)
                True

        '''
        superclass = super(PitchClassSegment, self)
        return superclass.count(item)

    @classmethod
    def from_selection(class_, selection, item_class=None):
        r'''Initializes segment from `selection`.

        ..  container:: example

            itializes from selection:

            ::

                >>> staff_1 = Staff("c'4 <d' fs' a'>4 b2")
                >>> staff_2 = Staff("c4. r8 g2")
                >>> staff_group = StaffGroup([staff_1, staff_2])
                >>> show(staff_group) # doctest: +SKIP

            ::

                >>> selection = select((staff_1, staff_2))
                >>> segment = pitchtools.PitchClassSegment.from_selection(selection)
                >>> show(segment) # doctest: +SKIP

        ..  container:: example

            Returns pitch-class segment:

            ::

                >>> segment
                PitchClassSegment(['c', 'd', 'fs', 'a', 'b', 'c', 'g'])

        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        return class_(
            items=pitch_segment,
            item_class=item_class,
            )

    def has_duplicates(self):
        r'''Is true when segment contains duplicate items. Otherwise false.

        ..  container:: example

            Has duplicates:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

            ::

                >>> segment.has_duplicates()
                True

        ..  container:: example

            Has no duplicates:

            ::

                >>> items = "c d e f g a b"
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

            ::

                >>> segment.has_duplicates()
                False

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        return len(pitchtools.PitchClassSet(self)) < len(self)

    def index(self, item):
        r'''Gets index of `item` in segment.

        ..  container:: example

            Example segment:
        
            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

        ..  container:: example

            Gets index of first item in segment:
        
            ::

                >>> segment.index(-2)
                0

        ..  container:: example

            Gets index of second item in segment:

            ::
                
                >>> segment.index(-1.5)
                1

        ..  container:: example

            Returns nonnegative integer:

            ::
                
                >>> isinstance(segment.index(-1.5), int)
                True

        '''
        superclass = super(PitchClassSegment, self)
        return superclass.index(item)

    def invert(self, axis=None):
        r'''Inverts segment.

        ..  container:: example

            Example segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

        ..  container:: example

            Inverts segment:

            ::

                >>> segment_ = segment.invert()
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_fild = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Inverts inversion of segment:

            ::

                >>> segment_ = segment.invert().invert()
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_fild = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            ::

                >>> segment_ == segment
                True

        ..  container:: example

            Returns pitch-class segment:

            ::

                >>> isinstance(segment_, pitchtools.PitchClassSegment)
                True

        '''
        items = (pc.invert(axis=axis) for pc in self)
        return new(self, items=items)

    def make_notes(self, n=None, written_duration=None):
        r'''Makes first `n` notes in segment.

        ..  container:: example

            Example segment:

            ::

                >>> items = [2, 4.5, 6, 11, 4.5, 10]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

        ..  container:: example

            Makes eighth notes:

            ::

                >>> notes = segment.make_notes()
                >>> staff = Staff(notes)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    d'8
                    eqs'8
                    fs'8
                    b'8
                    eqs'8
                    bf'8
                }

        ..  container:: example

            Makes notes with nonassignable durations:

            ::

                >>> notes = segment.make_notes(4, Duration(5, 16))
                >>> staff = Staff(notes)
                >>> time_signature = TimeSignature((5, 4))
                >>> attach(time_signature, staff)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \time 5/4
                    d'4 ~
                    d'16
                    eqs'4 ~
                    eqs'16
                    fs'4 ~
                    fs'16
                    b'4 ~
                    b'16
                }

        Interprets none-valued `n` equal to length of segment.

        Interprets none-valued `written_duration` equal to 1/8.

        ..  container:: example

            Returns selection:

            ::

                >>> isinstance(segment.make_notes(), selectiontools.Selection)
                True

        '''
        from abjad.tools import scoretools
        from abjad.tools import pitchtools
        n = n or len(self)
        written_duration = written_duration or durationtools.Duration(1, 8)
        result = scoretools.make_notes([0] * n, [written_duration])
        for i, logical_tie in enumerate(iterate(result).by_logical_tie()):
            pitch_class = pitchtools.NamedPitchClass(self[i % len(self)])
            pitch = pitchtools.NamedPitch(pitch_class, 4)
            for note in logical_tie:
                note.written_pitch = pitch
        return result

    def multiply(self, n=1):
        r'''Multiplies pitch-classes in segment by `n`.

        ..  container:: example

            Example segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

        ..  container:: example

            Multiplies pitch-classes in segment by 5:

            ::

                >>> segment_ = segment.multiply(n=5)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    d'8
                    eqs'8
                    fs'8
                    b'8
                    eqs'8
                    b'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies pitch-classes in segment by 7:

            ::

                >>> segment_ = segment.multiply(n=7)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    bf'8
                    dqf'8
                    fs'8
                    cs'8
                    dqf'8
                    cs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Multiplies pitch-classes in segment by 1:

            ::

                >>> segment_ = segment.multiply(n=1)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns pitch-class segment:

            ::

                >>> isinstance(segment_, pitchtools.PitchClassSegment)
                True

        '''
        from abjad.tools import pitchtools
        items = (pitchtools.NumberedPitchClass(pc).multiply(n)
            for pc in self)
        return new(self, items=items)

    def retrograde(self):
        r'''Gets retrograde of segment.

        ..  container:: example

            Example segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

        ..  container:: example

            Gets retrograde of segment:

            ::

                >>> segment_ = segment.retrograde()
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    g'8
                    bqf'8
                    g'8
                    fs'8
                    bqf'8
                    bf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Gets retrograde of retrograde of segment:

            ::

                >>> segment_ = segment.retrograde().retrograde()
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns pitch-class segment:

            ::

                >>> isinstance(segment_, pitchtools.PitchClassSegment)
                True

        '''
        return new(self, items=reversed(self))

    def rotate(self, n=0, stravinsky=False):
        r'''Rotates segment.

        ..  container:: example

            Example segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

        ..  container:: example

            Rotates segment to the right:

            ::

                >>> segment_ = segment.rotate(n=1)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    g'8
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Rotates segment to the left:

            ::

                >>> segment_ = segment.rotate(n=-1)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    bf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Rotates segment by zero:

            ::

                >>> segment_ = segment.rotate(n=0)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            ::

                >>> segment_ == segment
                True

        ..  container:: example

            Stravinsky-style rotation back-transposes segment to
            begin at zero:

            ::

                >>> segment_ = segment.rotate(1, stravinsky=True)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    c'8
                    ef'8
                    eqf'8
                    b'8
                    c'8
                    eqf'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Returns pitch-class segment:

            ::

                >>> isinstance(segment_, pitchtools.PitchClassSegment)
                True

        '''
        items = sequencetools.rotate_sequence(self._collection, n)
        new_segment = new(self, items=items)
        if stravinsky:
            interval_of_transposition = 0 - float(new_segment[0])
            new_segment = new_segment.transpose(interval_of_transposition)
        return new_segment

    def transpose(self, n=0):
        r'''Transposes segment by index `n`.

        ..  container:: example

            Example segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

        ..  container:: example

            Transposes segment by positive index:

            ::

                >>> segment_ = segment.transpose(n=13)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    b'8
                    bqs'8
                    g'8
                    af'8
                    bqs'8
                    af'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Transposes segment by negative index:

            ::

                >>> segment_ = segment.transpose(n=-13)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    a'8
                    aqs'8
                    f'8
                    fs'8
                    aqs'8
                    fs'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            Transposes segment by zero index:

            ::

                >>> segment_ = segment.transpose(n=0)
                >>> show(segment_) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment_.__illustrate__()
                >>> f(lilypond_file._get_first_voice())
                \new Voice {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            ::

                >>> segment_ == segment
                True

        ..  container:: example

            Returns pitch-class segment:

            ::

                >>> isinstance(segment_, pitchtools.PitchClassSegment)
                True

        '''
        items = (pitch_class.transpose(n=n) for pitch_class in self)
        return new(self, items=items)

    def voice_horizontally(self, initial_octave=4):
        r'''Voices segment with each pitch as close to the previous pitch as
        possible.

        ..  todo:: Should be implemented somewhere else.

        ..  container:: example

            Voices horizontally:

            ::

                >>> items = "c b d e f g e b a c"
                >>> segment = pitchtools.PitchClassSegment(items=items)
                >>> show(segment) # doctest: +SKIP

            ::

                >>> voiced_segment = segment.voice_horizontally()
                >>> show(voiced_segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = voiced_segment.__illustrate__()
                >>> f(lilypond_file._get_score())
                \new Score \with {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                } <<
                    \new PianoStaff <<
                        \context Staff = "treble" {
                            \clef "treble"
                            c'1 * 1/8
                            b1 * 1/8
                            d'1 * 1/8
                            e'1 * 1/8
                            f'1 * 1/8
                            g'1 * 1/8
                            e'1 * 1/8
                            b1 * 1/8
                            r1 * 1/8
                            c'1 * 1/8
                        }
                        \context Staff = "bass" {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            a1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

        ..  container:: example

            Returns pitch segment:

            ::

                >>> voiced_segment
                PitchSegment(["c'", 'b', "d'", "e'", "f'", "g'", "e'", 'b', 'a', "c'"])

        '''
        from abjad.tools import pitchtools
        initial_octave = pitchtools.Octave(initial_octave)
        pitches = []
        if self:
            pitch_class = pitchtools.NamedPitchClass(self[0])
            pitch = pitchtools.NamedPitch(pitch_class, initial_octave)
            pitches.append(pitch)
            for pitch_class in self[1:]:
                pitch_class = pitchtools.NamedPitchClass(pitch_class)
                pitch = pitchtools.NamedPitch(pitch_class, initial_octave)
                semitones = abs((pitch - pitches[-1]).semitones)
                while 6 < semitones:
                    if pitch < pitches[-1]:
                        pitch += 12
                    else:
                        pitch -= 12
                    semitones = abs((pitch - pitches[-1]).semitones)
                pitches.append(pitch)
        if self.item_class is pitchtools.NamedPitchClass:
            item_class = pitchtools.NamedPitch
        else:
            item_class = pitchtools.NumberedPitch
        return pitchtools.PitchSegment(
            items=pitches,
            item_class=item_class,
            )

    def voice_vertically(self, initial_octave=4):
        r'''Voices segment with each pitch higher than the previous.

        ..  todo:: Should be implemented somewhere else.

        ..  container:: example

            Voices vertically:

            ::

                >>> scale_degree_numbers = [1, 3, 5, 7, 9, 11, 13]
                >>> scale = tonalanalysistools.Scale('c', 'minor')
                >>> segment = pitchtools.PitchClassSegment((
                ...     scale.scale_degree_to_named_pitch_class(x)
                ...     for x in scale_degree_numbers))
                >>> show(segment) # doctest: +SKIP

            ::

                >>> voiced_segment = segment.voice_vertically()
                >>> show(voiced_segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = voiced_segment.__illustrate__()
                >>> f(lilypond_file._get_score())
                \new Score \with {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                } <<
                    \new PianoStaff <<
                        \context Staff = "treble" {
                            \clef "treble"
                            c'1 * 1/8
                            ef'1 * 1/8
                            g'1 * 1/8
                            bf'1 * 1/8
                            d''1 * 1/8
                            f''1 * 1/8
                            af''1 * 1/8
                        }
                        \context Staff = "bass" {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

        ..  container:: example

            Returns pitch segment:

            ::

                >>> voiced_segment
                PitchSegment(["c'", "ef'", "g'", "bf'", "d''", "f''", "af''"])

        '''
        from abjad.tools import pitchtools
        initial_octave = pitchtools.Octave(initial_octave)
        pitches = []
        if self:
            pitch_class = pitchtools.NamedPitchClass(self[0])
            pitch = pitchtools.NamedPitch(pitch_class, initial_octave)
            pitches.append(pitch)
            for pitch_class in self[1:]:
                pitch_class = pitchtools.NamedPitchClass(pitch_class)
                pitch = pitchtools.NamedPitch(pitch_class, initial_octave)
                while pitch < pitches[-1]:
                    pitch += 12
                pitches.append(pitch)
        if self.item_class is pitchtools.NamedPitchClass:
            item_class = pitchtools.NamedPitch
        else:
            item_class = pitchtools.NumberedPitch
        return pitchtools.PitchSegment(
            items=pitches,
            item_class=item_class,
            )
