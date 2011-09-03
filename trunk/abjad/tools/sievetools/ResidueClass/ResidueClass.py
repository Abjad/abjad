from abjad.core import _Immutable
from abjad.tools.sievetools._BaseResidueClass import _BaseResidueClass
from abjad.tools.sievetools._process_min_max_attribute import _process_min_max_attribute


class ResidueClass(_BaseResidueClass, _Immutable):
    '''Residue class (or congruence class).
    Residue classes form the basis of Xenakis sieves. They can be used to
    construct any complex periodic integer (or boolean) sequence as a
    combination of simple periodic sequences.

    Example from the opening of Xenakis's *Psappha* for solo percussion::

        abjad> from abjad.tools.sievetools import ResidueClass as RC

        abjad> s1 = (RC(8, 0) | RC(8, 1) | RC(8, 7)) & (RC(5, 1) | RC(5, 3))
        abjad> s2 = (RC(8, 0) | RC(8, 1) | RC(8, 2)) & RC(5, 0)
        abjad> s3 = RC(8, 3)
        abjad> s4 = RC(8, 4)
        abjad> s5 = (RC(8, 5) | RC(8, 6)) & (RC(5, 2) | RC(5, 3) | RC(5, 4))
        abjad> s6 = (RC(8, 1) & RC(5, 2))
        abjad> s7 = (RC(8, 6) & RC(5, 1))

        abjad> y = s1 | s2 | s3 | s4 | s5 | s6 | s7
        abjad> y
        {{{ResidueClass(8, 0) | ResidueClass(8, 1) | ResidueClass(8, 7)} & {ResidueClass(5, 1) | ResidueClass(5, 3)}} | {{ResidueClass(8, 0) | ResidueClass(8, 1) | ResidueClass(8, 2)} & ResidueClass(5, 0)} | ResidueClass(8, 3) | ResidueClass(8, 4) | {{ResidueClass(8, 5) | ResidueClass(8, 6)} & {ResidueClass(5, 2) | ResidueClass(5, 3) | ResidueClass(5, 4)}} | {ResidueClass(5, 2) & ResidueClass(8, 1)} | {ResidueClass(5, 1) & ResidueClass(8, 6)}}

        abjad> y.get_congruent_bases(40)
            [0, 1, 3, 4, 6, 8, 10, 11, 12, 13, 14, 16, 17, 19, 20, 22, 23, 25, 27,
            28, 29, 31, 33, 35, 36, 37, 38, 40]
        abjad> y.get_boolean_train(40)
            [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0,
            1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0]

    Return residue class.
    '''

    def __init__(self, *args):
        if len(args) == 1:
            self._init_by_rc_instance(*args)
        elif len(args) == 2:
            self._init_by_modulo_and_residue(*args)
        else:
            raise ValueError('unknown init arguments.')

    ### OVERLOADS ###

    def __eq__(self, exp):
        if isinstance(exp, ResidueClass):
            return (self.modulo == exp.modulo) and (self.residue == exp.residue)
        else:
            return False

    def __gt__(self, expr):
        if not isinstance(expr, ResidueClass):
            raise TypeError('must be residue class.')
        if self.modulo == expr.modulo:
            return expr.residue < self.residue
        return expr.modulo < self.modulo

    def __ge__(self, expr):
        if not isinstance(expr, ResidueClass):
            raise TypeError('must be residue class.')
        if self.modulo == expr.modulo:
            return expr.residue <= self.residue
        return expr.modulo <= self.modulo

    def __lt__(self, expr):
        if not isinstance(expr, ResidueClass):
            raise TypeError('must be residue class.')
        if self.modulo == expr.modulo:
            return self.residue < expr.residue
        return self.modulo < expr.modulo

    def __le__(self, expr):
        if not isinstance(expr, ResidueClass):
            raise TypeError('must be residue class.')
        if self.modulo == expr.modulo:
            return self.residue <= expr.residue
        return self.modulo <= expr.modulo

    def __ne__(self, expr):
        return not self == expr

    def __repr__(self):
        return '%s(%i, %i)' % (type(self).__name__, self.modulo, self.residue)

    ### PRIVATE METHODS ###

    def _init_by_rc_instance(self, rc):
        if not isinstance(rc, ResidueClass):
            raise TypeError('must be rc instance.')
        #self.modulo = rc.modulo # period
        #self.residue = rc.residue # phase
        object.__setattr__(self, '_modulo', rc.modulo) # period
        object.__setattr__(self, '_residue', rc.residue) # phase

    def _init_by_modulo_and_residue(self, modulo, residue):
        if not 0 < modulo:
            raise ValueError('modulo must be positive.')
        if not 0 <= residue < modulo:
            raise ValueError('abs(residue) must be < modulo')
        #self.modulo = modulo # period
        #self.residue = residue # phase
        object.__setattr__(self, '_modulo', modulo) # period
        object.__setattr__(self, '_residue', residue) # phase

    ### PUBLIC ATTRIBUTES ###

    @property
    def modulo(self):
        '''Period of residue class.
        '''
        return self._modulo

    @property
    def residue(self):
        '''Residue of residue class.
        '''
        return self._residue

    ### PUBLIC METHODS ###

    def get_boolean_train(self, *min_max):
        '''Returns a boolean train with 0s mapped to the integers
        that are not congruent bases of the residue class and 1s mapped
        to those that are.
        The method takes one or two integer arguments. If only one is given,
        it is taken as the max range and the min is assumed to be 0.

        Example::

            abjad> from abjad.tools.sievetools import ResidueClass as RC

            abjad> r = RC(3, 0)
            abjad> r.get_boolean_train(6)
            [1, 0, 0, 1, 0, 0]
            abjad> r.get_congruent_bases(-6, 6)
            [-6, -3, 0, 3, 6]

        Return list.
        '''

        min, max = _process_min_max_attribute(*min_max)
        result = []
        for i in range(min, max):
            if i % self.modulo == self.residue:
                result.append(1)
            else:
                result.append(0)
        return result

    def get_congruent_bases(self, *min_max):
        '''Returns all the congruent bases of this residue class
        within the given range.
        The method takes one or two integer arguments.
        If only one it given, it is taken as the max range and
        the min is assumed to be 0.

        Example::

            abjad> from abjad.tools.sievetools import ResidueClass as RC

            abjad> r = RC(3, 0)
            abjad> r.get_congruent_bases(6)
            [0, 3, 6]
            abjad> r.get_congruent_bases(-6, 6)
            [-6, -3, 0, 3, 6]

        Return list.
        '''

        min, max = _process_min_max_attribute(*min_max)
        result = []
        for i in range(min, max + 1):
            if i % self.modulo == self.residue:
                result.append(i)
        return result


if __name__ == '__main__':
    print 'Psappha B2[0:40]'
    RC = ResidueClass
    s1 = (RC(8, 0) | RC(8, 1) | RC(8, 7)) & (RC(5, 1) | RC(5, 3))
    s2 = (RC(8, 0) | RC(8, 1) | RC(8, 2)) & RC(5, 0)
    s3 = RC(8, 3) #&  RC(1, 0)
    s4 = RC(8, 4) #&  RC(1, 0)
    s5 = (RC(8, 5) | RC(8, 6)) & (RC(5, 2) | RC(5, 3) | RC(5, 4))
    s6 = (RC(8, 1) & RC(5, 2))
    s7 = (RC(8, 6) & RC(5, 1))

    y = s1 | s2 | s3 | s4 | s5 | s6 | s7
    print y
    print 'congruent bases:\n', y.get_congruent_bases(40)
    print 'boolen train:\n', y.get_boolean_train(40)
