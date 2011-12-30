from abjad.core import _Immutable
from abjad.tools import markuptools
from abjad.tools.tonalitytools.ExtentIndicator import ExtentIndicator
from abjad.tools.tonalitytools.InversionIndicator import InversionIndicator
from abjad.tools.tonalitytools.QualityIndicator import QualityIndicator
from abjad.tools.tonalitytools.ScaleDegree import ScaleDegree
from abjad.tools.tonalitytools.SuspensionIndicator import SuspensionIndicator
import re


class TonalFunction(_Immutable):
    '''.. versionadded:: 2.0

    Abjad model of functions in tonal harmony: I, I6, I64, V, V7, V43, V42,
    bII, bII6, etc., also i, i6, i64, v, v7, etc.

    Value object that can not be cahnged after instantiation.
    '''

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
        object.__setattr__(self, '_scale_degree', scale_degree)
        object.__setattr__(self, '_quality', quality)
        object.__setattr__(self, '_extent', extent)
        object.__setattr__(self, '_inversion', inversion)
        object.__setattr__(self, '_suspension', suspension)

    ### OVERLOADS ###

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

    ### PRIVATE ATTRIBUTES ###

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
        '': 5, '6': 5, '6/4': 5,
        '7': 7, '6/5': 7, '4/3': 7, '4/2': 7,
    }

    _figured_bass_string_to_inversion = {
        '': 0, '6': 1, '6/4': 2,
        '7': 0, '6/5': 1, '4/3': 2, '4/2': 3,
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
        if self.extent == ExtentIndicator(5):
            if self.quality == QualityIndicator('diminished'):
                return 'o'
            elif self.quality == QualityIndicator('augmented'):
                return '+'
            else:
                return ''
        elif self.extent == ExtentIndicator(7):
            if self.quality == QualityIndicator('dominant'):
                return ''
            elif self.quality == QualityIndicator('major'):
                return 'M'
            #elif self.quality == QualityIndicator('minor'):
            #   return 'm'
            elif self.quality == QualityIndicator('diminished'):
                return 'o'
            elif self.quality == QualityIndicator('half diminished'):
                return '@'
            elif self.quality == QualityIndicator('augmented'):
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

    #_symbolic_string_regex = re.compile(
    #    r'([#|b]*)([i|I|v|V]+)([M|m|o|@|+]?)(\d*)')

    #_symbolic_string_regex = re.compile(
    #    r'([#|b]*)([i|I|v|V]+)([M|m|o|@|+]?)(\d*)(\s*)([#|b]?\d*-?[#|b]?\d*)')

    _symbolic_string_regex = re.compile(
        r'([#|b]*)([i|I|v|V]+)([M|m|o|@|+]?)(.*)')

    ### PRIVATE METHODS ###

    def _init_by_reference(self, tonal_function):
        args = (tonal_function.scale_degree, tonal_function.quality,
            tonal_function.extent, tonal_function.inversion)
        return self._init_by_scale_degree_quality_extent_and_inversion(self, *args)

    def _init_by_scale_degree_quality_extent_and_inversion(self, *args):
        scale_degree, quality, extent, inversion = args
        scale_degree = ScaleDegree(scale_degree)
        #self._scale_degree = scale_degree
        quality = QualityIndicator(quality)
        #self._quality = quality
        extent = ExtentIndicator(extent)
        #self._extent = extent
        inversion = InversionIndicator(inversion)
        #self._inversion = inversion
        #self._suspension = SuspensionIndicator()
        suspension = SuspensionIndicator()
        return scale_degree, quality, extent, inversion, suspension

    def _init_by_symbolic_string(self, symbolic_string):
        groups = self._symbolic_string_regex.match(symbolic_string).groups()
        #print groups
        accidental, roman_numeral, quality, figured_bass = groups
        scale_degree = ScaleDegree(accidental + roman_numeral)
        #self._scale_degree = scale_degree
        figured_bass_parts = figured_bass.split('/')
        naive_figured_bass = [x for x in figured_bass_parts if not '-' in x]
        naive_figured_bass = '/'.join(naive_figured_bass)
        extent = self._figured_bass_string_to_extent[naive_figured_bass]
        extent = ExtentIndicator(extent)
        #self._extent = extent
        uppercase = roman_numeral == roman_numeral.upper()
        quality = self._get_quality_name(uppercase, quality, extent.number)
        quality = QualityIndicator(quality)
        #self._quality = quality
        inversion = self._figured_bass_string_to_inversion[naive_figured_bass]
        inversion = InversionIndicator(inversion)
        #self._inversion = inversion
        suspension = [x for x in figured_bass_parts if '-' in x]
        if not suspension:
            suspension = SuspensionIndicator()
        elif 1 < len(suspension):
            raise NotImplementedError('no multiple suspensions yet.')
        else:
            suspension = SuspensionIndicator(suspension[0])
        #self._suspension = suspension
        return scale_degree, quality, extent, inversion, suspension

    def _init_with_suspension(self, *args):
        scale_degree, quality, extent, inversion, suspension = \
            self._init_by_scale_degree_quality_extent_and_inversion(*args[:-1])
        suspension = args[-1]
        #self._suspension = SuspensionIndicator(suspension)
        suspension = SuspensionIndicator(suspension)
        return scale_degree, quality, extent, inversion, suspension

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

    ### PUBLIC ATTRIBUTES ###

    @property
    def bass_scale_degree(self):
        root_scale_degree = self.root_scale_degree.number
        bass_scale_degree = root_scale_degree - 1
        bass_scale_degree += 2 * self.inversion.number
        bass_scale_degree %= 7
        bass_scale_degree += 1
        bass_scale_degree = ScaleDegree(bass_scale_degree)
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
        return markuptools.Markup(symbolic_string, 'down')

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
