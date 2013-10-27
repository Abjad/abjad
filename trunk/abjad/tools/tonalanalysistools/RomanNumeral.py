# -*- encoding: utf-8 -*-
import re
from abjad.tools import marktools
from abjad.tools.abctools import AbjadObject


class RomanNumeral(AbjadObject):
    '''A functions in tonal harmony: I, I6, I64, V, V7, V43, V42,
    bII, bII6, etc., also i, i6, i64, v, v7, etc.

    Value object that can not be changed after instantiation.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_extent',
        '_inversion',
        '_quality',
        '_scale_degree',
        '_suspension',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], type(self)):
            scale_degree, quality, extent, inversion, suspension = \
                self._init_by_reference(args[0])
        elif len(args) == 1 and isinstance(args[0], str):
            scale_degree, quality, extent, inversion, suspension = \
                self._init_by_symbolic_string(args[0])
        elif len(args) == 4:
            scale_degree, quality, extent, inversion, suspension = \
                self._init_by_scale_degree_quality_extent_and_inversion(*args)
        elif len(args) == 5:
            scale_degree, quality, extent, inversion, suspension = \
                self._init_with_suspension(*args)
        else:
            raise ValueError('can not initialize tonal function.')
        self._scale_degree = scale_degree
        self._quality = quality
        self._extent = extent
        self._inversion = inversion
        self._suspension = suspension

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.scale_degree == arg.scale_degree:
                if self.quality == arg.quality:
                    if self.extent == arg.extent:
                        if self.inversion == arg.inversion:
                            if self.suspension == arg.suspension:
                                return True
        return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _accidental_name(self):
        accidental = self.scale_degree.accidental
        if accidental.is_adjusted:
            return accidental.name.title()
        return ''

    @property
    def _figured_bass_digits(self):
        characters = self._figured_bass_string
        if characters:
            characters = characters.split('/')
            digits = [int(x) for x in characters]
            return tuple(digits)
        return ()

    @property
    def _figured_bass_string(self):
        return self.inversion.extent_to_figured_bass_string(self.extent.number)

    _figured_bass_string_to_extent = {
        '': 5, 
        '6': 5, 
        '6/4': 5,
        '7': 7, 
        '6/5': 7, 
        '4/3': 7, 
        '4/2': 7,
    }

    _figured_bass_string_to_inversion = {
        '': 0, 
        '6': 1, 
        '6/4': 2,
        '7': 0, 
        '6/5': 1, 
        '4/3': 2, 
        '4/2': 3,
    }

    @property
    def _format_string(self):
        result = []
        result.append(self._accidental_name)
        result.append(self._roman_numeral_string)
        result.append(self.quality.quality_string.title())
        result.append(self.extent.name.title())
        result.append('In')
        result.append(self.inversion.title)
        if not self.suspension.is_empty:
            result.append('With')
            result.append(self.suspension.title_string)
        return ''.join(result)

    @property
    def _quality_symbolic_string(self):
        from abjad.tools import tonalanalysistools
        if self.extent == tonalanalysistools.ExtentIndicator(5):
            if self.quality == tonalanalysistools.QualityIndicator('diminished'):
                return 'o'
            elif self.quality == tonalanalysistools.QualityIndicator('augmented'):
                return '+'
            else:
                return ''
        elif self.extent == tonalanalysistools.ExtentIndicator(7):
            if self.quality == tonalanalysistools.QualityIndicator('dominant'):
                return ''
            elif self.quality == tonalanalysistools.QualityIndicator('major'):
                return 'M'
            elif self.quality == \
                tonalanalysistools.QualityIndicator('diminished'):
                return 'o'
            elif self.quality == \
                tonalanalysistools.QualityIndicator('half diminished'):
                return '@'
            elif self.quality == tonalanalysistools.QualityIndicator('augmented'):
                return '+'
            else:
                return ''
        else:
            raise NotImplementedError

    @property
    def _roman_numeral_string(self):
        roman_numeral_string = self.scale_degree.roman_numeral_string
        if not self.quality.is_uppercase:
            roman_numeral_string = roman_numeral_string.lower()
        return roman_numeral_string

    _symbolic_string_regex = re.compile(
        r'([#|b]*)([i|I|v|V]+)([M|m|o|@|+]?)(.*)')

    ### PRIVATE METHODS ###

    def _get_quality_name(self, uppercase, quality_string, extent):
        if quality_string == 'o':
            return 'diminished'
        elif quality_string == '@':
            return 'half diminished'
        elif quality_string == '+':
            return 'augmented'
        elif quality_string == 'M':
            return 'major'
        elif quality_string == 'm':
            return 'minor'
        elif extent == 5:
            if quality_string == '' and uppercase:
                return 'major'
            elif quality_string == '' and not uppercase:
                return 'minor'
            else:
                raise ValueError
        elif extent == 7:
            if quality_string == '' and uppercase:
                return 'dominant'
            elif quality_string == '' and not uppercase:
                return 'minor'
            else:
                raise ValueError
        else:
            raise ValueError

    def _init_by_reference(self, tonal_function):
        args = (tonal_function.scale_degree, tonal_function.quality,
            tonal_function.extent, tonal_function.inversion)
        return self._init_by_scale_degree_quality_extent_and_inversion(
            self, *args)

    def _init_by_scale_degree_quality_extent_and_inversion(self, *args):
        from abjad.tools import tonalanalysistools
        scale_degree, quality, extent, inversion = args
        scale_degree = tonalanalysistools.ScaleDegree(scale_degree)
        quality = tonalanalysistools.QualityIndicator(quality)
        extent = tonalanalysistools.ExtentIndicator(extent)
        inversion = tonalanalysistools.InversionIndicator(inversion)
        suspension = tonalanalysistools.SuspensionIndicator()
        return scale_degree, quality, extent, inversion, suspension

    def _init_by_symbolic_string(self, symbolic_string):
        from abjad.tools import tonalanalysistools
        groups = self._symbolic_string_regex.match(symbolic_string).groups()
        accidental, roman_numeral, quality, figured_bass = groups
        scale_degree = tonalanalysistools.ScaleDegree(accidental + roman_numeral)
        figured_bass_parts = figured_bass.split('/')
        naive_figured_bass = [x for x in figured_bass_parts if not '-' in x]
        naive_figured_bass = '/'.join(naive_figured_bass)
        extent = self._figured_bass_string_to_extent[naive_figured_bass]
        extent = tonalanalysistools.ExtentIndicator(extent)
        uppercase = roman_numeral == roman_numeral.upper()
        quality = self._get_quality_name(uppercase, quality, extent.number)
        quality = tonalanalysistools.QualityIndicator(quality)
        inversion = self._figured_bass_string_to_inversion[naive_figured_bass]
        inversion = tonalanalysistools.InversionIndicator(inversion)
        suspension = [x for x in figured_bass_parts if '-' in x]
        if not suspension:
            suspension = tonalanalysistools.SuspensionIndicator()
        elif 1 < len(suspension):
            raise NotImplementedError('no multiple suspensions yet.')
        else:
            suspension = tonalanalysistools.SuspensionIndicator(suspension[0])
        return scale_degree, quality, extent, inversion, suspension

    def _init_with_suspension(self, *args):
        from abjad.tools import tonalanalysistools
        scale_degree, quality, extent, inversion, suspension = \
            self._init_by_scale_degree_quality_extent_and_inversion(*args[:-1])
        suspension = args[-1]
        suspension = tonalanalysistools.SuspensionIndicator(suspension)
        return scale_degree, quality, extent, inversion, suspension

    ### PUBLIC PROPERTIES ###

    @property
    def bass_scale_degree(self):
        from abjad.tools import tonalanalysistools
        root_scale_degree = self.root_scale_degree.number
        bass_scale_degree = root_scale_degree - 1
        bass_scale_degree += 2 * self.inversion.number
        bass_scale_degree %= 7
        bass_scale_degree += 1
        bass_scale_degree = tonalanalysistools.ScaleDegree(bass_scale_degree)
        return bass_scale_degree

    @property
    def extent(self):
        return self._extent

    @property
    def figured_bass_string(self):
        digits = self._figured_bass_digits
        if self.suspension.is_empty:
            return '/'.join([str(x) for x in digits])
        suspension_pair = self.suspension.figured_bass_pair
        figured_bass_list = []
        for n in range(9, 1, -1):
            if n == suspension_pair[0]:
                figured_bass_list.append(str(self.suspension))
            elif n == suspension_pair[1]:
                pass
            elif n in digits:
                figured_bass_list.append(str(n))
        figured_bass_string = '/'.join(figured_bass_list)
        return figured_bass_string

    @property
    def inversion(self):
        return self._inversion

    @property
    def markup(self):
        symbolic_string = self.symbolic_string
        symbolic_string = symbolic_string.replace('#', r'\sharp ')
        return markuptools.Markup(symbolic_string, Down)

    @property
    def quality(self):
        return self._quality

    @property
    def root_scale_degree(self):
        return self._scale_degree

    # TODO: deprecate scale_degree in favor of root_scale_degree #
    @property
    def scale_degree(self):
        return self._scale_degree

    @property
    def suspension(self):
        return self._suspension

    @property
    def symbolic_string(self):
        result = ''
        result += self.scale_degree.accidental.symbolic_accidental_string
        result += self._roman_numeral_string
        result += self._quality_symbolic_string
        result += self.figured_bass_string
        return result
