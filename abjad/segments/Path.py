import importlib
import os
import pathlib
import shutil
import typing
from .Line import Line
from .Part import Part
from .PartManifest import PartManifest
from abjad.core.MultimeasureRest import MultimeasureRest
from abjad.core.Container import Container
from abjad.core.Score import Score
from abjad.core.Staff import Staff
from abjad.core.StaffGroup import StaffGroup
from abjad.indicators.Clef import Clef
from abjad.indicators.LilyPondLiteral import LilyPondLiteral
from abjad.indicators.MarginMarkup import MarginMarkup
from abjad.indicators.TimeSignature import TimeSignature
from abjad.system.IOManager import IOManager
from abjad.system.LilyPondFormatManager import LilyPondFormatManager
from abjad.system.Tags import Tags
from abjad.top.activate import activate
from abjad.top.attach import attach
from abjad.top.deactivate import deactivate
from abjad.top.iterate import iterate
from abjad.utilities.CyclicTuple import CyclicTuple
from abjad.utilities.OrderedDict import OrderedDict
from abjad.utilities.String import String


class Path(pathlib.PosixPath):
    """
    Path in an Abjad score package.

    ..  container:: example

        >>> path = abjad.Path(
        ...     '/path/to/scores/my_score/my_score',
        ...     scores='/path/to/scores',
        ...     )

        >>> path.materials
        Path*('/path/to/scores/my_score/my_score/materials')

        >>> path.materials('instruments')
        Path*('/path/to/scores/my_score/my_score/materials/instruments')

        >>> path.materials('instruments').is_material()
        True

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segment-makers'

    _known_directories = (
        '_assets',
        '_segments',
        'builds',
        'distribution',
        'etc',
        'materials',
        'segments',
        'stylesheets',
        'test',
        'tools',
        )

    _secondary_names = (
        '.gitignore',
        '__init__.py',
        '__make_pdf__.py',
        '__make_midi__.py',
        '__metadata__.py',
        '_assets',
        '_segments',
        'stylesheet.ily',
        )

    ### CONSTRUCTOR ###

    def __new__(class_, *arguments, scores=None):
        import abjad
        configuration = abjad.abjad_configuration
        if not arguments:
            raise Exception('must provide at least one argument.')
        argument = arguments[0]
        _arguments = arguments[1:]
        if isinstance(argument, pathlib.Path) or os.sep in argument:
            self = pathlib.Path.__new__(class_, argument)
        else:
            argument_list = []
            if argument == 'boilerplate':
                argument_list.append(configuration.boilerplate_directory)
            elif scores is not None:
                argument_list.append(scores)
                argument_list.extend(2 * [argument])
            else:
                argument_list.append(configuration.composer_scores_directory)
                argument_list.extend(2 * [argument])
            argument_list.extend(_arguments)
            self = pathlib.Path.__new__(class_, *argument_list)
        if scores is not None:
            scores = type(self)(scores)
        self._scores = scores
        return self

    ### SPECIAL METHODS ###

    def __call__(self, *names) -> 'Path':
        """
        Calls path on ``names``.
        """
        path = self
        for name in names:
            path /= name
        return path

    def __repr__(self) -> str:
        """
        Gets interpreter representation of path.
        """
        if bool(getattr(self, '_scores', None)):
            return "Path*('{}')".format(self)
        else:
            return "Path('{}')".format(self)

    def __rtruediv__(self, argument):
        """
        Joins path to ``argument``.

        Returns new path.
        """
        result = super().__rtruediv__(argument)
        result._scores = getattr(self, '_scores', None)
        return result

    def __truediv__(self, argument):
        """
        Joins ``argument`` to path.

        Returns new path.
        """
        result = super().__truediv__(argument)
        result._scores = getattr(self, '_scores', None)
        return result

    ### PRIVATE PROPERTIES ###

    @property
    def _assets(self) -> typing.Optional['Path']:
        """
        Gets _assets directory.
        """
        if self.is_builds():
            return self / '_assets'
        if self.is_score_build():
            return self / '_assets'
        if self.is_parts():
            return self / '_assets'
        if self.is_part():
            return self.parent / '_assets'
        return None

    @property
    def _segments(self) -> typing.Optional['Path']:
        """
        Gets _segments directory.

        Directory must be build directory, _segments direcotry or part
        directory.

        ..  container:: example

            >>> build = abjad.Path(
            ...     '/path/to/scores/my_score/my_score/builds/letter-score',
            ...     scores='/path/to/scores',
            ...     )

            Works when path is build directory:

            >>> build._segments
            Path*('/path/to/scores/my_score/my_score/builds/letter-score/_segments')

            Works when path is _segments directory:

            >>> (build / '_segments')._segments
            Path*('/path/to/scores/my_score/my_score/builds/letter-score/_segments')

            Works when path is _assets directory:

            >>> (build / '_assets')._segments
            Path('/path/to/scores/my_score/my_score/builds/letter-score/_segments')

            Works when path is parts directory:

            >>> parts = abjad.Path(
            ...     '/path/to/scores/my_score/my_score/builds/letter-parts',
            ...     scores='/path/to/scores',
            ...     )

            >>> parts._segments
            Path*('/path/to/scores/my_score/my_score/builds/letter-parts/_segments')

            Works when path is part directory:

            >>> (parts / 'bass-clarinet-part')._segments
            Path('/path/to/scores/my_score/my_score/builds/letter-parts/_segments')

            Works when path is file in part directory:

            >>> (parts / 'bass-clarinet-part' / 'layout.ly')._segments
            Path('/path/to/scores/my_score/my_score/builds/letter-parts/_segments')

        """
        if self.is__assets():
            return self.parent / '_segments'
        if self.is__segments():
            return self
        if self.is_score_build():
            return self / '_segments'
        if self.is_parts():
            return self / '_segments'
        if self.is_part():
            return self.parent / '_segments'
        if self.parent._segments is not None:
            return self.parent._segments
        return None

    ### PRIVATE METHODS ###

    def _context_name_to_first_appearance_margin_markup(self, context_name):
        module = self._import_score_package()
        margin_markups = getattr(module, 'margin_markups', None)
        if not margin_markups:
            return []
        dictionary = OrderedDict()
        string = 'first_appearance_margin_markup'
        for segment in self.segments.list_paths():
            dictionary_ = segment.get_metadatum(string, [])
            dictionary.update(dictionary_)
        key = dictionary.get(context_name)
        if key is None:
            return []
        margin_markup = margin_markups.get(key)
        if margin_markup is None:
            return []
        markup = margin_markup.markup
        assert markup is not None, repr(margin_markup)
        strings = markup._get_format_pieces()
        strings.insert(0, 'shortInstrumentName =')
        indent = 4 * ' '
        strings = [indent + _ for _ in strings]
        strings = [r'\with', '{'] + strings + ['}']
        return strings

    def _filter_by_view(self, paths):
        view = self.get_metadatum('view')
        if view is None:
            return paths
        filtered_paths = []
        for pattern in view:
            if ':ds:' in pattern:
                for path in paths:
                    if path._match_identifier_pattern(pattern):
                        filtered_paths.append(path)
            elif 'md:' in pattern:
                pairs = []
                for path in paths:
                    metadatum = path._match_metadata_pattern(pattern)
                    if metadatum is not None:
                        pairs.append((metadatum, path))
                pairs.sort(key=lambda _: _[0])
                pairs.reverse()
                filtered_paths_ = [_[-1] for _ in pairs]
                filtered_paths.extend(filtered_paths_)
            elif ':path:' in pattern:
                for path in paths:
                    if path._match_path_pattern(pattern):
                        filtered_paths.append(path)
            else:
                for path in paths:
                    if pattern == path.get_identifier():
                        filtered_paths.append(path)
        return filtered_paths

    def _find_empty_wrapper(self):
        if not self.scores:
            return
        for path in self.scores.iterdir():
            if not path.name[0].isalpha():
                continue
            if not path.name[0].islower():
                continue
            if not path.is_dir():
                continue
            has_contents = False
            if all(_.name.startswith('.') for _ in path.iterdir()):
                return type(self)(path)

    def _get_file_path_ending_with(self, string):
        if not self.is_dir():
            return
        glob = '*{}'.format(string)
        for path in sorted(self.glob(glob)):
            if path.is_file():
                return path

    def _get_part_manifest(self):
        assert self.is_score_package_path()
        score_template = self._import_score_template()
        score_template = score_template()
        part_manifest = score_template.part_manifest
        assert isinstance(part_manifest, PartManifest), repr(part_manifest)
        return part_manifest

    def _get_score_pdf(self):
        path = self.distribution._get_file_path_ending_with('score.pdf')
        if not path:
            path = self.builds._get_file_path_ending_with('score.pdf')
        return path

    def _import_score_package(self):
        assert self.is_score_package_path()
        try:
            module = importlib.import_module(self.contents.name)
        except:
            return
        return module

    def _import_score_template(self):
        module = self._import_score_package()
        if not module:
            raise Exception('can not import score package.')
        score_template = getattr(module, 'ScoreTemplate', None)
        if not score_template:
            raise Exception('can not import score template.')
        return score_template

    def _list_paths(self):
        paths = []
        if not self.exists():
            return paths
        predicate = self.get_name_predicate()
        is_external = self.is_external()
        is_scores = self.is_scores()
        is_segments = self.is_segments()
        names = []
        for name in sorted([_.name for _ in self.iterdir()]):
            name = String(name)
            if name.startswith('_') and not (is_external or is_segments):
                continue
            if name in ('.DS_Store', '.cache', '.git', '.gitmodules'):
                continue
            if name in ('__init__.py', '__pycache__'):
                continue
            if (predicate is not None and
                not predicate(name) and
                name != '_assets' and
                name != '_segments'):
                continue
            if name == 'stylesheet.ily' and self.is_stylesheets():
                pass
            elif name in self._secondary_names:
                continue
            path = self(name)
            try:
                path.relative_to(self)
            except ValueError:
                continue
            names.append(name)
        if is_segments:
            names = [_ for _ in names if _.is_segment_name()]
            names = String.sort_segment_names(names)
        if self.is__segments():
            prefix = 'segment-'
            names = [_ for _ in names if _.startswith(prefix)]
            single_character_names, double_character_names = [], []
            for name in names:
                segment_name = name[len(prefix):]
                segment_name = segment_name.replace('-', '_')
                if segment_name.endswith('.ly'):
                    segment_name = segment_name[:-3]
                elif segment_name.endswith('.ily'):
                    segment_name = segment_name[:-4]
                else:
                    raise ValueError(segment_name)
                if len(segment_name) == 1:
                    single_character_names.append(name)
                elif len(segment_name) == 2:
                    double_character_names.append(name)
                else:
                    raise NotImplementedError(segment_name)
            names = single_character_names + double_character_names
        paths = [self / _ for _ in names]
        return paths

    def _match_identifier_pattern(self, pattern):
        token = ':ds:'
        assert token in pattern, repr(pattern)
        identifier = self.get_identifier()
        pattern = pattern.replace(token, repr(identifier))
        try:
            result = eval(pattern)
        except:
            traceback.print_exc()
            result = False
        return result

    def _match_metadata_pattern(self, pattern):
        count = pattern.count('md:')
        for _ in range(count + 1):
            parts = pattern.split()
            for part in parts:
                if part.startswith('md:'):
                    metadatum_name = part[3:]
                    metadatum = self.get_metadatum(metadatum_name)
                    metadatum = repr(metadatum)
                    pattern = pattern.replace(part, metadatum)
        try:
            result = eval(pattern)
        except:
            traceback.print_exc()
            return False
        return result

    def _match_path_pattern(self, pattern):
        token = ':path:'
        assert token in pattern, repr(pattern)
        pattern = pattern.replace(token, repr(self))
        try:
            result = eval(pattern)
        except:
            traceback.print_exc()
            return False
        return result

    def _part_name_to_default_clef(self, part_name):
        module = self._import_score_package()
        instruments = getattr(module, 'instruments', None)
        if not instruments:
            raise Exception(f'can not find instruments: {self!r}.')
        words = String(part_name).delimit_words()
        if words[-1].isdigit():
            words = words[:-1]
        if words[0] in ('First', 'Second'):
            words = words[1:]
        key = ''.join(words)
        instrument = instruments.get(key, None)
        if not instrument:
            raise Exception(f'can not find {key!r}.')
        clef = Clef(instrument.allowable_clefs[0])
        return clef

    @staticmethod
    def _sort_by_identifier(paths):
        pairs = []
        for path in paths:
            identifier = String(path.get_identifier())
            identifier = identifier.strip_diacritics().replace("'", '')
            pairs.append((identifier, path))
        pairs.sort(key=lambda _: _[0])
        paths = [_[-1] for _ in pairs]
        return paths

    ### PUBLIC PROPERTIES ###

    @property
    def build(self) -> typing.Optional['Path']:
        """
        Gets build directory.
        
        Directory must be build directory, _segments direcotry or part
        directory.

        ..  container:: example

            >>> build = abjad.Path(
            ...     '/path/to/scores/my_score/my_score/builds/letter-score',
            ...     scores='/path/to/scores',
            ...     )

            Works when path is build directory:

            >>> build.build
            Path*('/path/to/scores/my_score/my_score/builds/letter-score')

            Works when path is _segments directory:

            >>> (build / '_segments').build
            Path('/path/to/scores/my_score/my_score/builds/letter-score')

            Works when path is _assets directory:

            >>> (build / '_assets').build
            Path('/path/to/scores/my_score/my_score/builds/letter-score')

            Works when path is parts directory:

            >>> parts = abjad.Path(
            ...     '/path/to/scores/my_score/my_score/builds/letter-parts',
            ...     scores='/path/to/scores',
            ...     )

            >>> parts.build
            Path*('/path/to/scores/my_score/my_score/builds/letter-parts')

            Works when path is part directory:

            >>> (parts / 'bass-clarinet-part').build
            Path*('/path/to/scores/my_score/my_score/builds/letter-parts/bass-clarinet-part')

            Works when path is file in part directory:

            >>> (parts / 'bass-clarinet-part' / 'layout.ly').build
            Path('/path/to/scores/my_score/my_score/builds/letter-parts/bass-clarinet-part')

        """
        if self.is_build():
            return self
        elif self.parent.is_build():
            return self.parent
        else:
            return None

    @property
    def builds(self) -> typing.Optional['Path']:
        """
        Gets builds directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.builds
            Path*('/path/to/scores/my_score/my_score/builds')
            >>> path.builds('letter')
            Path*('/path/to/scores/my_score/my_score/builds/letter')

        """
        if self.contents:
            return self.contents('builds')
        else:
            return None

    @property
    def contents(self):
        """
        Gets contents directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.contents
            Path*('/path/to/scores/my_score/my_score')
            >>> path.contents('etc', 'notes.txt')
            Path*('/path/to/scores/my_score/my_score/etc/notes.txt')

        """
        scores = self.scores
        if not scores:
            return None
        parts = self.relative_to(scores).parts
        if not parts:
            return None
        result = scores(parts[0], parts[0])
        result._scores = getattr(self, '_scores', None)
        return result

    @property
    def distribution(self) -> typing.Optional['Path']:
        """
        Gets distribution directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.distribution
            Path*('/path/to/scores/my_score/my_score/distribution')
            >>> path.distribution('score.pdf')
            Path*('/path/to/scores/my_score/my_score/distribution/score.pdf')

        """
        if self.contents:
            return self.contents('distribution')
        else:
            return None

    @property
    def etc(self) -> typing.Optional['Path']:
        """
        Gets etc directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.etc
            Path*('/path/to/scores/my_score/my_score/etc')
            >>> path.etc('notes.txt')
            Path*('/path/to/scores/my_score/my_score/etc/notes.txt')

        """
        if self.contents:
            return self.contents('etc')
        else:
            return None

    @property
    def materials(self) -> typing.Optional['Path']:
        """
        Gets materials directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.materials
            Path*('/path/to/scores/my_score/my_score/materials')
            >>> path.materials('instruments')
            Path*('/path/to/scores/my_score/my_score/materials/instruments')

        """
        if self.contents:
            return self.contents('materials')
        else:
            return None

    @property
    def scores(self) -> typing.Optional['Path']:
        """
        Gets scores directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.scores
            Path*('/path/to/scores')
            >>> path.scores('red_score', 'red_score')
            Path*('/path/to/scores/red_score/red_score')

        """
        import abjad
        configuration = abjad.abjad_configuration
        if getattr(self, '_scores', None) is not None:
            result = getattr(self, '_scores')
            result._scores = result
            return result
        directory = configuration.composer_scores_directory
        if str(self).startswith(str(directory)):
            return type(self)(directory)
        else:
            return None

    @property
    def segments(self) -> typing.Optional['Path']:
        """
        Gets segments directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.segments
            Path*('/path/to/scores/my_score/my_score/segments')
            >>> path.segments('segment_01')
            Path*('/path/to/scores/my_score/my_score/segments/segment_01')

        """
        if self.contents:
            return self.contents('segments')
        else:
            return None

    @property
    def stylesheets(self) -> typing.Optional['Path']:
        """
        Gets stylesheets directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.stylesheets
            Path*('/path/to/scores/my_score/my_score/stylesheets')
            >>> path.stylesheets('stylesheet.ily')
            Path*('/path/to/scores/my_score/my_score/stylesheets/stylesheet.ily')

        """
        if self.contents:
            return self.contents('stylesheets')
        else:
            return None

    @property
    def test(self) -> typing.Optional['Path']:
        """
        Gets test directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.test
            Path*('/path/to/scores/my_score/my_score/test')
            >>> path.test('test_materials.py')
            Path*('/path/to/scores/my_score/my_score/test/test_materials.py')

        """
        if self.contents:
            return self.contents('test')
        else:
            return None

    @property
    def tools(self) -> typing.Optional['Path']:
        """
        Gets tools directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.tools
            Path*('/path/to/scores/my_score/my_score/tools')
            >>> path.tools('SegmentMaker.py')
            Path*('/path/to/scores/my_score/my_score/tools/SegmentMaker.py')

        """
        if self.contents:
            return self.contents('tools')
        else:
            return None

    @property
    def wrapper(self) -> typing.Optional['Path']:
        """
        Gets wrapper directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.wrapper
            Path*('/path/to/scores/my_score')
            >>> path.wrapper('my_score', 'etc')
            Path*('/path/to/scores/my_score/my_score/etc')

        """
        if self.contents:
            result = type(self)(self.contents()).parent
            _scores = getattr(self, '_scores', None)
            setattr(result, '_scores', _scores)
            return result
        else:
            return None

    ### PUBLIC METHODS ###

    def activate(
        self,
        tag: typing.Union[str, typing.Callable],
        indent: int = 0,
        message_zero: bool = False,
        name: str = None,
        undo: bool = False,
        ) -> typing.Tuple[int, int, typing.List[String]]:
        """
        Activates ``tag`` in path.

        Case 0: path is a non-LilyPond file. Method does nothing.

        Case 1: path is a LilyPond (.ily, .ly) file starting with
        ``illustration``, ``layout`` or ``segment``. Method activates ``tag``
        in file.

        Case 2: path is a directory. Method descends directory recursively and
        activates ``tag`` in LilyPond files given in case 1.

        Returns triple.
        
        First item in triple is count of deactivated tags activated by method.
        
        Second item in pair is count of already-active tags skipped by method.

        Third item in pair is list of canonical string messages that explain
        what happened.
        """
        assert isinstance(indent, int), repr(indent)
        if self.is_file():
            if self.suffix not in ('.ily', '.ly'):
                count, skipped = 0, 0
            else:
                text = self.read_text()
                if undo:
                    text, count, skipped = deactivate(text, tag, skipped=True)
                else:
                    text, count, skipped = activate(text, tag, skipped=True)
                self.write_text(text)
        else:
            assert self.is_dir()
            count, skipped = 0, 0
            for path in sorted(self.glob('**/*')):
                path = Path(path)
                if not path.suffix in ('.ily', '.ly'):
                    continue
                if not (path.name.startswith('illustration') or
                    path.name.startswith('layout') or
                    path.name.startswith('segment')):
                    continue
                count_, skipped_, _ = path.activate(tag, undo=undo)
                count += count_
                skipped += skipped_
        if name is None:
            name = str(tag)
        if undo:
            adjective = 'inactive'
            antonym = 'active'
            gerund = 'deactivating'
            infinitive = 'deactivate'
        else:
            adjective = 'active'
            antonym = 'inactivate'
            gerund = 'activating'
            infinitive = 'activate'
        messages = []
        total = count + skipped
        if total == 0 and message_zero:
            messages.append(f'found no {name} tags')
        if 0 < total:
            tags = String('tag').pluralize(total)
            messages.append(f'found {total} {name} {tags}')
            if 0 < count:
                tags = String('tag').pluralize(count)
                message = f'{gerund} {count} {name} {tags}'
                messages.append(message)
            if 0 < skipped:
                tags = String('tag').pluralize(skipped)
                message = f'skipping {skipped} ({adjective}) {name} {tags}'
                messages.append(message)
        whitespace = indent * ' '
        messages_ = [
            String(whitespace + String(_).capitalize_start() + ' ...')
            for _ in messages
            ]
        return count, skipped, messages_

    def add_buildspace_metadatum(
        self,
        name,
        value,
        document_name: str = None,
        ) -> None:
        """
        Adds metadatum with ``name`` and ``value`` into buildspace metadata
        with optional ``document_name``.
        """
        assert self.is_buildspace(), repr(self)
        if self.is_parts():
            if document_name is not None:
                part_dictionary = self.get_metadatum(
                    document_name,
                    OrderedDict(),
                    )
            else:
                part_dictionary = OrderedDict()
            part_dictionary[name] = value
            assert String(document_name).is_shout_case()
            self.add_metadatum(document_name, part_dictionary)
        else:
            self.add_metadatum(name, value)

    def add_metadatum(self, name, value) -> None:
        """
        Adds metadatum.
        """
        assert ' ' not in name, repr(name)
        metadata = self.get_metadata()
        metadata[name] = value
        self.write_metadata_py(metadata)

    def coerce(self, name, suffix=None):
        """
        Coerces asset ``name``.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

        ..  container:: example

            In build directory:

            >>> path.builds('letter').coerce('back cover.tex')
            'back cover.tex'
            >>> path.builds('letter').coerce('Back Cover.tex')
            'Back Cover.tex'
            >>> path.builds('letter').coerce('BACK_COVER.tex')
            'BACK_COVER.tex'

            >>> path.builds('letter').coerce('new music.ly')
            'new music.ly'
            >>> path.builds('letter').coerce('New Music.ly')
            'New Music.ly'
            >>> path.builds('letter').coerce('NEW_MUSIC.ly')
            'NEW_MUSIC.ly'

            >>> path.builds('letter').coerce('page_layout.py')
            'page_layout.py'
            >>> path.builds('letter').coerce('Page Layout.py')
            'Page Layout.py'
            >>> path.builds('letter').coerce('PAGE_LAYOUT.py')
            'PAGE_LAYOUT.py'

        ..  container:: example

            In builds directory:

            >>> path.builds.coerce('letter_landscape')
            'letter-landscape'
            >>> path.builds.coerce('letter landscape')
            'letter-landscape'
            >>> path.builds.coerce('Letter Landscape')
            'letter-landscape'

        ..  container:: example

            In contents directory:

            >>> path.contents.coerce('ETC')
            'etc'

        ..  container:: example

            In distribution directory:

            >>> path.distribution.coerce('program notes.txt')
            'program-notes.txt'
            >>> path.distribution.coerce('Program Notes.txt')
            'program-notes.txt'
            >>> path.distribution.coerce('PROGRAM_NOTES.txt')
            'program-notes.txt'

        ..  container:: example

            In etc directory:

            >>> path.etc.coerce('material sketches.md')
            'material-sketches.md'
            >>> path.etc.coerce('Material Sketches.md')
            'material-sketches.md'
            >>> path.etc.coerce('MATERIAL_SKETCHES.md')
            'material-sketches.md'

        ..  container:: example

            In scores directory:

            >>> path.scores.coerce('Green Score')
            'green_score'

        ..  container:: example

            In segment directory:

            >>> path.segments.coerce('_')
            '_'
            >>> path.segments.coerce('A')
            'A'
            >>> path.segments.coerce('A1')
            'A1'
            >>> path.segments.coerce('A99')
            'A99'

            >>> path.segments.coerce('segment_01')
            'segment_01'
            >>> path.segments.coerce('segment 01')
            'segment_01'
            >>> path.segments.coerce('Segment 01')
            'segment_01'
            >>> path.segments.coerce('SEGMENT 01')
            'segment_01'

        ..  container:: example

            In stylesheets directory:

            >>> path.stylesheets.coerce('segment stylesheet')
            'segment-stylesheet.ily'
            >>> path.stylesheets.coerce('Segment Stylesheet')
            'segment-stylesheet.ily'
            >>> path.stylesheets.coerce('SEGMENT_STYLESHEET')
            'segment-stylesheet.ily'

        ..  container:: example

            Does not coerce in unknown directory:

            >>> path = abjad.Path(
            ...     '/unknown/path',
            ...     )

            >>> path.coerce('custom-script')
            'custom-script'
            >>> path.coerce('custom_script')
            'custom_script'
            >>> path.coerce('CUSTOM_SCRIPT')
            'CUSTOM_SCRIPT'

        Returns string.
        """
        name = String(name).strip_diacritics()
        assert os.path.sep not in name, repr(name)
        suffix = suffix or type(self)(name).suffix
        stem = String(type(self)(name).stem)
        if self.is_scores():
            name = stem.to_snake_case()
        elif self.is_external():
            pass
        elif self.is__assets():
            pass
        elif self.is__segments():
            pass
        elif self.is_build():
            pass
        elif self.is_builds():
            name = stem.to_dash_case()
        elif self.is_contents():
            name = stem.to_snake_case()
        elif self.is_distribution():
            name = stem.to_dash_case() + suffix
        elif self.is_etc():
            name = stem.to_dash_case() + suffix
        elif self.is_material():
            name = stem.to_snake_case() + '.py'
        elif self.is_materials():
            name = stem.to_snake_case()
        elif self.is_segment():
            name = stem.to_snake_case() + '.py'
        elif self.is_segments():
            if stem.is_segment_name():
                name = stem
            else:
                name = stem.to_snake_case()
        elif self.is_stylesheets():
            name = stem.to_dash_case() + '.ily'
        elif self.is_test():
            name = stem.to_snake_case() + '.py'
        elif self.is_tools() and name[0].isupper():
            name = stem.to_upper_camel_case() + '.py'
        elif self.is_tools() and name[0].islower():
            name = stem.to_snake_case() + '.py'
        elif self.is_wrapper():
            pass
        elif self.is_external():
            pass
        return name

    def count(
        self,
        tag: typing.Union[str, typing.Callable],
        ) -> typing.Tuple[typing.Tuple[int, int], typing.Tuple[int, int]]:
        """
        Counts ``tag`` in path.

        Returns two pairs.

        Pair 1 gives (active tags, activate lines).

        Pair 2 gives (deactivated tags, deactivated lines).
        """
        assert isinstance(tag, str) or callable(tag), repr(tag)
        assert self.is_file(), repr(self)
        active_tags, active_lines = 0, 0
        deactivated_tags, deactivated_lines = 0, 0
        with open(self) as pointer:
            last_line_had_tag = False
            for line_ in pointer.readlines():
                line = Line(line_)
                if line.match(tag):
                    if line.is_active():
                        active_lines += 1
                        if not last_line_had_tag:
                            active_tags += 1
                    else:
                        deactivated_lines += 1
                        if not last_line_had_tag:
                            deactivated_tags += 1
                    last_line_had_tag = True
                else:
                    last_line_had_tag = False
        pair_1 = (active_tags, active_lines)
        pair_2 = (deactivated_tags, deactivated_lines)
        return pair_1, pair_2

    def deactivate(
        self,
        tag: typing.Union[str, typing.Callable],
        indent: int = 0,
        message_zero: bool = False,
        name: str = None,
        ) -> typing.Tuple[int, int, typing.List[String]]:
        """
        Deactivates ``tag`` in path.
        """
        return self.activate(
            tag,
            name=name,
            indent=indent,
            message_zero=message_zero,
            undo=True,
            )

    def extern(
        self,
        include_path: 'Path' = None,
        score_path: 'Path' = None,
        ) -> None:
        """
        Externalizes LilyPond file parsable chunks.

        Produces skeleton score file and include file.

        Overwrites path with skeleton score when ``score_path`` is none.

        Writes include file to path with ``.ily`` suffix when ``include_path``
        is none.
        """
        if not self.suffix == '.ly':
            raise Exception(f'must be lilypond file: {self}.')
        if include_path is None:
            include_path = self.with_suffix('.ily')
        assert isinstance(include_path, type(self)), repr(include_path)
        if score_path is None:
            score_path = self
        assert isinstance(score_path, type(self)), repr(score_path)
        preamble_lines, score_lines = [], []
        stack, finished_variables = OrderedDict(), OrderedDict()
        found_score = False
        with open(self) as pointer:
            for line in pointer.readlines():
                if (line.startswith(r'\score {') or
                    line.startswith(r'\context Score') or
                    line.startswith('{')):
                    found_score = True
                if not found_score:
                    preamble_lines.append(line)
                elif ' %*% ' in line:
                    words = line.split()
                    name = words[-1]
                    # first line in expression:
                    if name not in stack:
                        stack[name] = []
                        stack[name].append(line)
                    # last line in expression
                    else:
                        stack[name].append(line)
                        finished_variables[name] = stack[name]
                        del(stack[name])
                        count = len(line) - len(line.lstrip())
                        indent = count * ' '
                        dereference = indent + fr'\{name}' + '\n'
                        if bool(stack):
                            items = list(stack.items())
                            items[-1][-1].append(dereference)
                        else:
                            score_lines.append(dereference)
                elif bool(stack):
                    items = list(stack.items())
                    items[-1][-1].append(line)
                else:
                    score_lines.append(line)
        lines = []
        if preamble_lines:
            assert preamble_lines[-1].isspace(), repr(preamble_lines[-1])
            preamble_lines.pop()
        if include_path.parent == self.parent:
            include_name = include_path.name
        else:
            include_name = str(include_path)
        preamble_lines.append(f'\\include "{include_name}"\n')
        preamble_lines.append('\n')
        preamble_lines.append('\n')
        lines.extend(preamble_lines)
        lines.extend(score_lines)
        text = ''.join(lines)
        score_path.write_text(text)
        lines = []
        items = list(finished_variables.items())
        total = len(items)
        for i, item in enumerate(items):
            name, variable_lines = item
            first_line = variable_lines[0]
            count = len(first_line) - len(first_line.lstrip())
            first_line = first_line[count:]
            first_line = f'{name} = {first_line}'
            words = first_line.split()
            assert words[-2] == '%*%', repr(words)
            first_line = ' '.join(words[:-2]) + '\n'
            lines.append(first_line)
            for variable_line in variable_lines[1:]:
                assert variable_line[:count].isspace(), repr(line)
                variable_line = variable_line[count:]
                lines.append(variable_line)
            last_line = lines[-1]
            words = last_line.split()
            assert words[-2] == '%*%', repr(words)
            last_line = ' '.join(words[:-2]) + '\n'
            lines[-1] = last_line
            if i < total - 1:
                lines.append('\n')
                lines.append('\n')
        text = ''.join(lines)
        include_path.write_text(text)

    def get_asset_type(self) -> str:
        """
        Gets asset identifier.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.builds.get_asset_type()
            'directory'

            >>> path.contents.get_asset_type()
            'directory'

            >>> path.distribution.get_asset_type()
            'file'

            >>> path.etc.get_asset_type()
            'file'

            >>> path.materials.get_asset_type()
            'package'

            >>> path.scores.get_asset_type()
            'package'

            >>> path.segments.get_asset_type()
            'package'

            >>> path.stylesheets.get_asset_type()
            'file'

            >>> path.test.get_asset_type()
            'file'

            >>> path.tools.get_asset_type()
            'file'

            >>> path.wrapper.get_asset_type()
            'asset'

        ..  container:: example

            With external path:

            >>> abjad.Path('/path/to/external').get_asset_type()
            'asset'

        """
        if self.is_scores():
            return 'package'
        elif self.is_wrapper():
            return 'asset'
        elif self.is_contents():
            return 'directory'
        elif self.is_builds():
            return 'directory'
        elif self.is_materials_or_segments():
            return 'package'
        elif self.is_score_package_path((
            '_assets',
            '_segments',
            'build',
            'distribution',
            'etc',
            'tools',
            'material',
            'segment',
            'stylesheets',
            'test',
            )):
            return 'file'
        else:
            return 'asset'

    def get_files_ending_with(self, name) -> typing.List['Path']:
        """
        Gets files in path ending with ``name``.
        """
        paths = []
        for path in self.list_paths():
            if path.name.endswith(name):
                paths.append(path)
        return paths

    def get_identifier(self) -> str:
        """
        Gets identifier.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.contents.get_identifier()
            '(untitled score)'

            >>> path.materials('tempi').get_identifier()
            'tempi'

            >>> path.materials().get_identifier()
            'materials'

            >>> path.segments('segment_01').get_identifier()
            'segment_01'

            >>> path.segments().get_identifier()
            'segments'

            >>> path.wrapper().get_identifier()
            '(untitled score)'

        Returns title when path is contents directory.

        Returns name metadatum when name metadatum exists.

        Returns path name otherwise.
        """
        if self.is_wrapper():
            result = self.contents().get_title()
        elif self.is_contents():
            result = self.get_title()
        elif self.is_dir():
            result = self.get_metadatum('name', self.name)
        else:
            result = self.name
        return String(result)

    def get_measure_profile_metadata(self) -> typing.Tuple[int, int, list]:
        """
        Gets measure profile metadata.

        Reads segment metadata when path is segment.

        Reads score metadata when path is not segment.

        Returns triple of three metadata: first measure number; measure count;
        list of fermata measure numbers.
        """
        if self.parent.is_segment():
            string = 'first_measure_number'
            first_measure_number = self.parent.get_metadatum(string)
            time_signatures = self.parent.get_metadatum('time_signatures')
            if bool(time_signatures):
                measure_count = len(time_signatures)
            else:
                measure_count = 0
            string = 'fermata_measure_numbers'
            fermata_measure_numbers = self.parent.get_metadatum(string)
        else:
            first_measure_number = 1
            dictionary = self.contents.get_metadatum('time_signatures')
            dictionary = dictionary or OrderedDict()
            measure_count = 0
            for segment, time_signatures in dictionary.items():
                measure_count += len(time_signatures)
            string = 'fermata_measure_numbers'
            dictionary = self.contents.get_metadatum(string)
            dictionary = dictionary or OrderedDict()
            fermata_measure_numbers = []
            for segment, fermata_measure_numbers_ in dictionary.items():
                fermata_measure_numbers.extend(fermata_measure_numbers_)
        return first_measure_number, measure_count, fermata_measure_numbers

    def get_metadata(self) -> OrderedDict:
        """
        Gets __metadata__.py file in path.
        """
        metadata_py_path = self('__metadata__.py')
        metadata = None
        if metadata_py_path.is_file():
            file_contents_string = metadata_py_path.read_text()
            try:
                result = IOManager.execute_string(
                    file_contents_string,
                    attribute_names=('metadata',),
                    )
            except NameError as e:
                raise Exception(repr(metadata_py_path), e)
            if result:
                metadata = result[0]
            else:
                metadata = None
        return OrderedDict(metadata)

    def get_metadatum(
        self,
        metadatum_name: str,
        default: typing.Any = None,
        ) -> typing.Any:
        """
        Gets metadatum.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.contents.get_metadatum('foo') is None
            True

        """
        metadata = self.get_metadata()
        metadatum = metadata.get(metadatum_name)
        if not metadatum:
            metadatum = default
        return metadatum

    def get_name_predicate(self) -> typing.Optional[typing.Callable]:
        """
        Gets name predicate.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.builds.get_name_predicate()
            <function String.is_build_directory_name at ...>

            >>> path.contents.get_name_predicate()
            <function String.is_package_name at ...>

            >>> path.materials.get_name_predicate()
            <function String.is_package_name at ...>

            >>> path.materials('tempi').get_name_predicate()
            <function String.is_lowercase_file_name at ...>

            >>> path.scores.get_name_predicate()
            <function String.is_package_name at ...>

            >>> path.segments.get_name_predicate()
            <function String.is_segment_name at ...>

            >>> path.segments('segment_01').get_name_predicate()
            <function String.is_lowercase_file_name at ...>

            >>> path.wrapper.get_name_predicate() is None
            True

        """
        if self.is_scores():
            return String.is_package_name
        elif self.is_external():
            return None
        elif self.is_wrapper():
            return None
        elif self.is_build():
            return None
        elif self.is_builds():
            return String.is_build_directory_name
        elif self.is_contents():
            return String.is_package_name
        elif self.is_distribution():
            return String.is_dash_case_file_name
        elif self.is_etc():
            return String.is_dash_case_file_name
        elif self.is_material():
            return String.is_lowercase_file_name
        elif self.is_materials():
            return String.is_package_name
        elif self.is_scores():
            return String.is_package_name
        elif self.is_segment():
            return String.is_lowercase_file_name
        elif self.is_segments():
            return String.is_segment_name
        elif self.is_tools():
            return String.is_tools_file_name
        elif self.is_stylesheets():
            return String.is_stylesheet_name
        elif self.is_test():
            return String.is_module_file_name
        elif self.is_wrapper():
            return None
        else:
            return None

    def get_next_package(
        self,
        cyclic: bool = False,
        ) -> typing.Optional['Path']:
        """
        Gets next package.

        ..  container:: example

                >>> path = abjad.Path(
                ...     '/path/to/scores/my_score/my_score',
                ...     scores='/path/to/scores',
                ...     )

            >>> path.get_next_package() is None
            True

        """
        if not self.is_dir():
            return None
        path: typing.Optional[Path] = None
        if self.is_material():
            if self.materials is not None:
                paths = self.materials.list_paths()
            else:
                paths = []
            if self == paths[-1] and not cyclic:
                path = self
            else:
                index = paths.index(self)
                paths = CyclicTuple(paths)
                path = paths[index + 1]
        elif self.is_materials():
            paths = self.list_paths()
            path = paths[0]
        elif self.is_segment():
            if self.segments is not None:
                paths = self.segments.list_paths()
            else:
                paths = []
            if self == paths[-1] and not cyclic:
                path = None
            else:
                index = paths.index(self)
                paths = CyclicTuple(paths)
                path = paths[index + 1]
        elif self.is_segments():
            paths = self.list_paths()
            path = paths[0]
        else:
            raise ValueError(self)
        return path

    def get_next_score(
        self,
        cyclic: bool = False,
        ) -> typing.Optional['Path']:
        """
        Gets next score.

        ..  container:: example

                >>> path = abjad.Path(
                ...     '/path/to/scores/my_score/my_score',
                ...     scores='/path/to/scores',
                ...     )

            >>> path.get_next_score() is None
            True

        """
        if not self.is_dir():
            return None
        if not (self.is_score_package_path() or self.is_scores()):
            return None
        if self.is_scores():
            wrappers = self.list_paths()
            if wrappers:
                return wrappers[0]
        if self.scores is not None:
            wrappers = self.scores.list_paths()
        else:
            wrappers = []
        if not wrappers:
            return None
        wrapper = self.wrapper
        if wrapper == wrappers[-1] and not cyclic:
            return None
        index = wrappers.index(wrapper)
        wrappers = CyclicTuple(wrappers)
        return wrappers[index + 1]

    def get_part_identifier(self) -> typing.Optional[str]:
        """
        Gets part identifier in layout.py only.
        """
        if not self.name.endswith('layout.py'):
            return None
        for line in self.read_text().split('\n'):
            if line.startswith('part_identifier ='):
                globals_ = globals()
                exec(line, globals_)
                part_identifier = globals_['part_identifier']
                return part_identifier
        return None

    def get_preamble_partial_score(
        self,
        ) -> bool:
        """
        Gets preamble time signatures.
        """
        assert self.is_file(), repr(self)
        prefix = '% partial_score ='
        with open(self) as pointer:
            for line in pointer.readlines():
                if line.startswith(prefix):
                    line = line[len(prefix):]
                    partial_score = eval(line)
                    return partial_score
        return False

    def get_preamble_time_signatures(
        self,
        ) -> typing.Optional[typing.List[str]]:
        """
        Gets preamble time signatures.
        """
        assert self.is_file(), repr(self)
        prefix = '% time_signatures ='
        with open(self) as pointer:
            for line in pointer.readlines():
                if line.startswith(prefix):
                    line = line[len(prefix):]
                    time_signatures = eval(line)
                    return time_signatures
        return None

    def get_previous_package(
        self,
        cyclic: bool = False,
        ) -> typing.Optional['Path']:
        """
        Gets previous package.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.get_previous_package() is None
            True

        """
        if not self.is_dir():
            return None
        if self.is_material():
            if self.materials is not None:
                paths = self.materials.list_paths()
            else:
                paths = []
            if self == paths[0] and not cyclic:
                path = None
            else:
                index = paths.index(self)
                paths = CyclicTuple(paths)
                path = paths[index - 1]
        elif self.is_materials():
            paths = self.list_paths()
            path = paths[-1]
        elif self.is_segment():
            if self.segments is not None:
                paths = self.segments.list_paths()
            else:
                paths = []
            if self == paths[0] and not cyclic:
                path = None
            else:
                index = paths.index(self)
                paths = CyclicTuple(paths)
                path = paths[index - 1]
        elif self.is_segments():
            paths = self.list_paths()
            path = paths[-1]
        else:
            raise ValueError(self)
        return path

    def get_previous_score(
        self,
        cyclic: bool = False,
        ) -> typing.Optional['Path']:
        """
        Gets previous score.

        ..  container:: example

                >>> path = abjad.Path(
                ...     '/path/to/scores/my_score/my_score',
                ...     scores='/path/to/scores',
                ...     )

            >>> path.get_previous_score() is None
            True

        """
        if not self.is_dir():
            return None
        if not (self.is_score_package_path() or self.is_scores()):
            return None
        if self.is_scores():
            wrappers = self.list_paths()
            if wrappers:
                return wrappers[-1]
        if self.scores is not None:
            wrappers = self.scores.list_paths()
        else:
            wrappers = []
        if not wrappers:
            return None
        wrapper = self.wrapper
        if wrapper == wrappers[0] and not cyclic:
            return None
        index = wrappers.index(wrapper)
        wrappers = CyclicTuple(wrappers)
        return wrappers[index - 1]

    def get_time_signature_metadata(self) -> typing.List[TimeSignature]:
        """
        Gets time signature metadata for buildspace directory.
        """
        if self.is_segment():
            time_signatures = self.get_metadatum('time_signatures', [])
            time_signatures = [
                TimeSignature.from_string(_) for _ in time_signatures
                ]
            return time_signatures
        time_signatures = self.contents.get_metadatum('time_signatures')
        if time_signatures is None:
            return []
        assert isinstance(time_signatures, OrderedDict)
        time_signatures_ = []
        for segment_name, strings in time_signatures.items():
            for string in strings:
                time_signature = TimeSignature.from_string(string)
                time_signatures_.append(time_signature)
        return time_signatures_

    def get_title(self, year=True):
        """
        Gets score title.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.get_title()
            '(untitled score)'
        
        Returns string.
        """
        if year and self.get_metadatum('year'):
            title = self.get_title(year=False)
            year = self.get_metadatum('year')
            result = '{} ({})'.format(title, year)
            return result
        else:
            result = self.get_metadatum('title')
            result = result or '(untitled score)'
            return result

    @staticmethod
    def global_rest_identifier(segment_name: str) -> String:
        """
        Gets global rest identifier.

        ..  container:: example

            >>> abjad.Path.global_rest_identifier('_')
            'i_GlobalRests'

            >>> abjad.Path.global_rest_identifier('_1')
            'i_a_GlobalRests'

            >>> abjad.Path.global_rest_identifier('_2')
            'i_b_GlobalRests'

            >>> abjad.Path.global_rest_identifier('A')
            'A_GlobalRests'

            >>> abjad.Path.global_rest_identifier('A1')
            'A_a_GlobalRests'

            >>> abjad.Path.global_rest_identifier('A2')
            'A_b_GlobalRests'

        """
        identifier = String(segment_name).to_segment_lilypond_identifier()
        identifier = String(f'{identifier}_GlobalRests')
        return identifier

    def global_rest_identifiers(self) -> typing.List[String]:
        """
        Gets global rest identifiers.
        """
        assert not self.is_external(), repr(self);
        identifiers = []
        if self.segments is not None:
            paths = self.segments.list_paths()
        else:
            paths = []
        for segment in paths:
            identifier = String(segment.name).to_segment_lilypond_identifier()
            identifier = String(f'{identifier}_GlobalRests')
            identifiers.append(identifier)
        return identifiers

    def global_skip_identifiers(self) -> typing.List[String]:
        """
        Gets global skip identifiers.
        """
        assert not self.is_external(), repr(self);
        identifiers = []
        if self.segments is not None:
            paths = self.segments.list_paths()
        else:
            paths = []
        for segment in paths:
            identifier = String(segment.name).to_segment_lilypond_identifier()
            identifier = String(f'{identifier}_GlobalSkips')
            identifiers.append(identifier)
        return identifiers

    def instrument_to_staff_identifiers(self, instrument: str) -> OrderedDict: 
        """
        Changes ``instrument`` to staff identifiers dictionary.
        """
        assert not self.is_external(), repr(self)
        alive_during_segment = OrderedDict()
        if self.segments is not None:
            paths = self.segments.list_paths()
        else:
            paths = []
        for segment in paths:
            dictionary = segment.get_metadatum('alive_during_segment', [])
            alive_during_segment[segment.name] = dictionary
        staves_in_score: typing.List[String] = []
        for segment_name, contexts in alive_during_segment.items():
            for context in contexts:
                if context.startswith(instrument):
                    words = String(context).delimit_words()
                    if words[-2] == 'Staff' and String(words[-1]).is_roman():
                        if context not in staves_in_score:
                           staves_in_score.append(context) 
        staves_in_score = String.sort_roman(staves_in_score)
        dictionary = OrderedDict()
        for staff in staves_in_score:
            dictionary[staff] = identifiers = []
            for segment_name, contexts in alive_during_segment.items():
                identifier = String(segment_name)
                identifier = identifier.to_segment_lilypond_identifier()
                if staff in contexts:
                    identifier_ = f'{identifier}_{staff}'
                else:
                    identifier_ =  f'{identifier}_GlobalRests'
                identifier = String(identifier_)
                identifiers.append(identifier)
        return dictionary

    def is__assets(self) -> bool:
        """
        Is true when path is _assets directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path = path('build', '_assets')
            >>> path.is__assets()
            True

        """
        return self.name == '_assets'

    def is__segments(self) -> bool:
        """
        Is true when path is _segments directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score/builds/letter/_segments',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.is__segments()
            True

        """
        return self.name == '_segments'

    def is_build(self) -> bool:
        """
        Is true when path is build directory.

        ..  container:: example

                >>> path = abjad.Path(
                ...     '/path/to/scores/my_score/my_score',
                ...     scores='/path/to/scores',
                ...     )
                >>> path.builds('letter').is_build()
                True

        """
        if self.name in ('_assets', '_segments'):
            return False
        if self.parent.name == 'builds':
            return True
        if self.parent.parent.name == 'builds' and self.suffix == '':
            return True
        return False

    def is_builds(self) -> bool:
        """
        Is true when path is builds directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.builds.is_builds()
            True

        """
        return self.name == 'builds'

    def is_buildspace(self) -> bool:
        """
        Is true when path is buildspace.

            * build
            * builds
            * segment
            * segments
            * _segments

        """
        if self.is_build() or self.is_builds():
            return True
        if self.is__segments() or self.is_segment() or self.is_segments():
            return True
        return False

    def is_contents(self) -> bool:
        """
        Is true when path is contents directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.contents.is_contents()
            True

        """
        if self.scores is not None:
            return self.scores / self.name / self.name == self
        else:
            return False

    def is_distribution(self) -> bool:
        """
        Is true when path is distribution directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.distribution.is_distribution()
            True

        """
        return self.name == 'distribution'

    def is_etc(self) -> bool:
        """
        Is true when path is etc directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.etc.is_etc()
            True

        """
        return self.name == 'etc'

    def is_external(self) -> bool:
        """
        Is true when path is not a score package path.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.builds.is_external()
            False
            >>> path.contents.is_external()
            False
            >>> path.wrapper.is_external()
            False

            >>> path.scores.is_external()
            True

        ..  container:: example

            >>> abjad.Path('/path/to/location').is_external()
            True

        """
        import abjad
        configuration = abjad.abjad_configuration
        directory = configuration.composer_scores_directory
        if str(self) == str(directory):
            return True
        if (not self.name[0].isalpha() and
            not self.name == '_assets' and
            not self.name == '_segments' and
            not self.parent.name == 'segments'):
            return True
        if str(self).startswith(str(directory)):
            return False
        directory = getattr(self, '_scores', None)
        if str(self) == str(directory):
            return True
        if directory and str(self).startswith(str(directory)):
            return False
        return True

    def is_illustrationspace(self) -> bool:
        """
        Is true when path is any of material, materials, segment or
        segments directories.

        Returns true or false.
        """
        if self.is_material():
            return True
        if self.is_materials():
            return True
        if self.is_segment():
            return True
        if self.is_segments():
            return True
        return False

    def is_introduction_segment(self) -> bool:
        """
        Is true when path is segment with name like _, _1, _2, ....

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.segments('_').is_introduction_segment()
            True

            >>> path.segments('_1').is_introduction_segment()
            True

            >>> path.segments('_99').is_introduction_segment()
            True

            >>> path.segments('_1A').is_introduction_segment()
            False

            >>> path.segments('1').is_introduction_segment()
            False

            >>> path.segments('A').is_introduction_segment()
            False

        """
        if not self.is_segment():
            return False
        if String(self.name).is_introduction_segment_name():
            return True
        return False

    def is_library(self) -> bool:
        """
        Is true when path is composer library tools directory.
        """
        import abjad
        configuration = abjad.abjad_configuration
        if configuration.composer_library_tools:
            return str(self) == configuration.composer_library_tools
        return False

    def is_material(self) -> bool:
        """
        Is true when path is material directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.materials('tempi').is_material()
            True

        """
        return self.parent.name == 'materials'

    def is_material_or_segment(self) -> bool:
        """
        Is true when path is material directory or segment directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.materials.is_material_or_segment()
            False

            >>> path.materials('tempi').is_material_or_segment()
            True

            >>> path.segments.is_material_or_segment()
            False

            >>> path.segments('A').is_material_or_segment()
            True

        """
        return self.parent.name in ('materials', 'segments')

    def is_materials(self) -> bool:
        """
        Is true when path is materials directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.materials.is_materials()
            True

        """
        return self.name == 'materials'

    def is_materials_or_segments(self) -> bool:
        """
        Is true when path is materials directory or segments directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.materials.is_materials_or_segments()
            True

            >>> path.materials('tempi').is_materials_or_segments()
            False

            >>> path.segments.is_materials_or_segments()
            True

            >>> path.segments('A').is_materials_or_segments()
            False

        """
        return self.name in ('materials', 'segments')

    def is_part(self) -> bool:
        """
        Is true when directory is part directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.builds.is_part()
            False

            >>> path.builds('arch-a-parts').is_part()
            False

        """
        return self.parent.is_parts()

    def is_parts(self) -> bool:
        """
        Is true when directory is parts directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.builds.is_parts()
            False

            >>> path.builds('arch-a-score').is_parts()
            False

        """
        if self.is_build():
            if self.name.endswith('-parts'):
                return True
            else:
                return self.get_metadatum('parts_directory') is True
        else:
            return False

    def is_score_build(self) -> bool:
        """
        Is true when directory is score build directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.builds.is_score_build()
            False

            >>> path.builds('arch-a-score').is_score_build()
            True

        """
        if self.is_build():
            if self.name.endswith('-parts'):
                return False
            if self.name.endswith('-part'):
                return False
            if self.get_metadatum('parts_directory') is True:
                return False
            if self.parent.get_metadatum('parts_directory') is True:
                return False
            return True
        else:
            return False

    def is_score_package_path(self, prototype=()) -> bool:
        """
        Is true when path is package path.

        ..  container:: example

            External path returns false:

            >>> abjad.Path('/path/to/location').is_score_package_path()
            False

        ..  container:: example

            Scores directory returns false:

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.scores.is_score_package_path()
            False

        ..  container:: example

            Package paths return true:

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.wrapper.is_score_package_path()
            True

            >>> path.contents.is_score_package_path()
            True

            >>> path.stylesheets.is_score_package_path()
            True

            >>> path('build', '_assets').is_score_package_path()
            True

        """
        if self.is_external():
            return False
        if self.is_scores():
            return False
        if not self.scores:
            return False
        if (not self.name[0].isalpha() and
            not (self.is_segment() or
                self.is__assets() or
                self.is__segments())):
            return False
        if not prototype:
            return True
        if isinstance(prototype, str):
            prototype = (prototype,)
        assert isinstance(prototype, tuple), repr(prototype)
        assert all(isinstance(_, str) for _ in prototype)
        if 'scores' in prototype:
            raise Exception(self, prototype)
        if self.name in prototype:
            return True
        if 'build' in prototype and self.is_build():
            return True
        if 'buildspace' in prototype:
            if self.is_buildspace():
                return True
        if 'contents' in prototype and self.is_contents():
            return True
        if 'illustrationspace' in prototype:
            if self.is_illustrationspace():
                return True
        if 'material' in prototype and self.is_material():
            return True
        if 'part' in prototype and self.is_part():
            return True
        if 'parts' in prototype and self.is_parts():
            return True
        if 'segment' in prototype and self.is_segment():
            return True
        if 'wrapper' in prototype and self.is_wrapper():
            return True
        return False

    def is_scores(self) -> bool:
        """
        Is true when path is scores directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.scores.is_scores()
            True

        """
        return self == self.scores

    def is_segment(self) -> bool:
        """
        Is true when path is segment directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.segments('segment_01').is_segment()
            True

        ..  container:: example

            REGRESSION. Abjad segments directory is excluded:

            >>> path = abjad.Path(
            ...     '/path/to/abjad/abjad/segments',
            ...     )
            >>> path /= 'segment_01'
            >>> path.is_segment()
            False

        """
        if self.name[0] == '.':
            return False
        return (self.parent.name == 'segments' and
            self.parent.parent.name != 'abjad')

    @staticmethod
    def is_segment_name(string) -> bool:
        """
        Is true when ``string`` is canonical segment name.

        ..  container:: example

            >>> abjad.Path.is_segment_name('_')
            True

            >>> abjad.Path.is_segment_name('_1')
            True

            >>> abjad.Path.is_segment_name('_2')
            True

            >>> abjad.Path.is_segment_name('_99')
            True

            >>> abjad.Path.is_segment_name('A')
            True

            >>> abjad.Path.is_segment_name('A1')
            True

            >>> abjad.Path.is_segment_name('A2')
            True

            >>> abjad.Path.is_segment_name('A99')
            True

            >>> abjad.Path.is_segment_name('B')
            True

            >>> abjad.Path.is_segment_name('B1')
            True

            >>> abjad.Path.is_segment_name('B2')
            True

            >>> abjad.Path.is_segment_name('B99')
            True

            >>> abjad.Path.is_segment_name('AA')
            True

            >>> abjad.Path.is_segment_name('AA1')
            True

            >>> abjad.Path.is_segment_name('AA2')
            True

            >>> abjad.Path.is_segment_name('AA99')
            True

            >>> abjad.Path.is_segment_name('AB')
            True

            >>> abjad.Path.is_segment_name('AB1')
            True

            >>> abjad.Path.is_segment_name('AB2')
            True

            >>> abjad.Path.is_segment_name('AB99')
            True

            >>> abjad.Path.is_segment_name('__')
            False

            >>> abjad.Path.is_segment_name('1')
            False

            >>> abjad.Path.is_segment_name('a')
            False

            >>> abjad.Path.is_segment_name('b')
            False

            >>> abjad.Path.is_segment_name('aa')
            False

            >>> abjad.Path.is_segment_name('ab')
            False

            >>> abjad.Path.is_segment_name('AAA')
            False

        """
        if not isinstance(string, str):
            return False
        if not bool(string):
            return False
        if not (string[0].isupper() or string[0] == '_'):
            return False
        if len(string) == 1:
            return True
        if not (string[1].isupper() or string[1].isdigit()):
            return False
        if len(string) == 2:
            return True
        return string[2:].isnumeric()

    def is_segments(self) -> bool:
        """
        Is true when path is segments directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.segments.is_segments()
            True

            Excludes Abjad segments directory:

            >>> path = abjad.Path(
            ...     '/path/to/abjad/abjad/segments',
            ...     )
            >>> path.is_segments()
            False

        """
        return self.name == 'segments' and self.parent.name != 'abjad'

    def is_stylesheets(self) -> bool:
        """
        Is true when path is stylesheets directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.stylesheets.is_stylesheets()
            True

        """
        return self.name == 'stylesheets'

    def is_test(self) -> bool:
        """
        Is true when path is test directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.test.is_test()
            True

        """
        return self.name == 'test'

    def is_tools(self) -> bool:
        """
        Is true when path is tools directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.tools.is_tools()
            True

        """
        return self.name == 'tools'

    def is_wrapper(self) -> bool:
        """
        Is true when path is wrapper directory

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.wrapper.is_wrapper()
            True

        """
        if self.scores is not None:
            return self.scores / self.name == self
        else:
            return False

    def list_paths(self):
        """
        Lists paths ordered by view (if any).

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.list_paths()
            []

        Returns list.
        """
        paths = self._list_paths()
        paths = self._filter_by_view(paths)
        if self.is_scores() and self.get_metadatum('view') is None:
            paths = self._sort_by_identifier(paths)
        return paths

    def list_secondary_paths(self):
        """
        Lists secondary paths.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.list_secondary_paths()
            []

        Returns list.
        """
        paths = []
        for path in sorted(self.glob('*')):
            if path.name in sorted(self._secondary_names):
                if path.name == 'stylesheet.ily' and self.is_stylesheets():
                    continue
                paths.append(path)
        return paths

    def part_to_identifiers(
        self,
        part: Part,
        container_to_part_assignment: OrderedDict,
        ) -> typing.Union[str, typing.List[str]]:
        """
        Changes ``part`` to (part container) identifiers (using
        ``container_to_part_assignment`` dictionary).
        """
        assert not self.is_external(), repr(self)
        if not isinstance(part, Part):
            raise TypeError(f'must be part (not {part!r}).')
        identifiers = []
        default_clef = self._part_name_to_default_clef(part.name)
        clef_string = format(default_clef, 'lilypond')
        assert clef_string.startswith('\\'), repr(clef_string)
        clef_string = clef_string[1:]
        identifiers.append(clef_string)
        dictionary = container_to_part_assignment
        if not dictionary:
            message = 'empty container-to-part-assignment dictionary'
            return message
        for i, (segment_name, dictionary_) in enumerate(dictionary.items()):
            if i == 0:
                first_segment = True
            else:
                first_segment = False
            pairs = []
            for identifier, (part_assignment, timespan) in dictionary_.items():
                if part in part_assignment:
                    pairs.append((identifier, timespan))
            if pairs:
                pairs.sort(key=lambda pair: pair[1])
                identifiers_ = [_[0] for _ in pairs]
                identifiers.extend(identifiers_)
            else:
                identifier = self.global_rest_identifier(segment_name)
                identifiers.append(identifier)
        return identifiers

    def remove(self):
        """
        Removes path if it exists.

        Returns none.
        """
        if self.is_file():
            self.unlink()
        elif self.is_dir():
            shutil.rmtree(str(self))

    def remove_metadatum(self, name):
        """
        Removes metadatum.

        Returns none.
        """
        assert ' ' not in name, repr(name)
        metadata = self.get_metadata()
        try:
            metadata.pop(name)
        except KeyError:
            pass
        self.write_metadata_py(metadata)

    def score_skeleton(self) -> typing.Optional[Score]:
        """
        Makes score skeleton.

        Only works when score template defines ``skeleton()`` method.
        """
        assert not self.is_external(), repr(self)
        score_template = self._import_score_template()
        if not hasattr(score_template, 'skeleton'):
            return None
        skeleton = score_template.skeleton()
        indent = 4 * ' '
        context = skeleton['GlobalSkips']
        identifiers = self.global_skip_identifiers()
        strings = ['\\' + _ for _ in identifiers]
        literal = LilyPondLiteral(strings)
        attach(literal, context)
        context = skeleton['GlobalRests']
        identifiers = self.global_rest_identifiers()
        strings = ['\\' + _ for _ in identifiers]
        literal = LilyPondLiteral(strings)
        attach(literal, context)
        module = self._import_score_package()
        instruments = getattr(module, 'instruments', None)
        for staff_group in iterate(skeleton).components(StaffGroup):
            if staff_group:
                continue
            assert len(staff_group) == 0, repr(staff_group)
            instrument = staff_group.name
            words = String(staff_group.name).delimit_words()
            if words[-3:] == ['Square', 'Staff', 'Group']:
                words = words[:-3]
            elif words[-2:] == ['Piano', 'Staff']:
                words = words[:-2]
            elif words == ['Percussion', 'Staff', 'Group']:
                words = [String('Percussion')]
            else:
                raise ValueError(staff_group)
            instrument = ''.join(words)
            dictionary = self.instrument_to_staff_identifiers(instrument)
            if instrument in ('FirstViolin', 'SecondViolin'):
                key = 'Violin'
            else:
                key = instrument
            abjad_instrument = instruments.get(key, None)
            if not abjad_instrument:
                raise Exception(f'can not find {key!r}.')
            clef = Clef(abjad_instrument.allowable_clefs[0])
            clef_string = format(clef, 'lilypond')
            strings = []
            method = self._context_name_to_first_appearance_margin_markup
            for staff_name, identifiers in dictionary.items():
                strings.append('{')
                for i, identifier in enumerate(identifiers):
                    string = indent + rf'\context Staff = "{staff_name}"'
                    strings.append(string)
                    if i == 0:
                        margin_markup_strings = method(staff_name)
                        for string_ in margin_markup_strings:
                            strings.append(indent + string_)
                        strings.append(indent + clef_string)
                    string = indent + '\\' + identifier
                    strings.append(string)
                strings.append('}')
            literal = LilyPondLiteral(strings)
            attach(literal, staff_group)
        return skeleton

    def segment_number_to_path(self, number):
        """
        Changes segment number to path.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.segment_number_to_path(1)

        Returns path.
        """
        for path in sorted(self.segments().glob('*')):
            if not path.is_dir():
                continue
            if not path.name.startswith('segment_'):
                continue
            body = path.name[8:]
            try:
                body = int(body)
            except ValueError:
                continue
            if body == number:
                return path

    def to_part(self) -> Part:
        """
        Changes path to part.
        """
        assert self.parent.is_part(), repr(self)
        words = self.parent.name.split('-')
        part_manifest = self._get_part_manifest()
        if not part_manifest:
            raise Exception(f'no part manifest: {self}.')
        assert isinstance(part_manifest, PartManifest), repr(part_manifest)
        words = [String(_).capitalize_start() for _ in words]
        part_name = ''.join(words)
        for part in part_manifest:
            if part.name == part_name:
                return part
        raise Exception(f'can not find {part_name!r} in part manifest.')

    def trim(self) -> str:
        """
        Trims path.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.contents.trim()
            '/path/to/scores/my_score/my_score'

            >>> path.segments.trim()
            'my_score/segments'

            >>> path.segments('segment_01').trim()
            'my_score/segments/segment_01'

            >>> path.materials.trim()
            'my_score/materials'

            >>> path.materials('tempi').trim()
            'my_score/materials/tempi'

        """
        import abjad
        configuration = abjad.abjad_configuration
        if self.scores is None or self.is_wrapper() or self.is_contents():
            home_directory = Path(configuration.home_directory)
            if str(self).startswith(str(home_directory)):
                return '../' + str(self.relative_to(home_directory))
            return str(self)
        count = len(self.scores.parts) + 1
        parts = self.parts
        parts = parts[count:]
        path = pathlib.Path(*parts)
        if str(path) == '.':
            return str(self)
        return str(path)

    def update_order_dependent_segment_metadata(self):
        """
        Updates order-dependent segment metadata.

        Returns none.
        """
        paths = self.segments().list_paths()
        if not paths:
            return
        segment_count = len(paths)
        for segment_index, path in enumerate(paths):
            segment_number = segment_index + 1
            path.add_metadatum('segment_number', segment_number)
            path.add_metadatum('segment_count', segment_count)
        path = paths[0]
        first_bar_number = 1
        path.add_metadatum('first_bar_number', first_bar_number)
        measure_count = path.get_metadatum('measure_count')
        if not measure_count:
            return
        next_bar_number = first_bar_number + measure_count
        for path in paths[1:]:
            first_bar_number = next_bar_number
            path.add_metadatum('first_bar_number', next_bar_number)
            measure_count = path.get_metadatum('measure_count')
            if not measure_count:
                return
            next_bar_number = first_bar_number + measure_count

    def with_name(self, name):
        """
        Gets path with ``name``.

        Returns path.
        """
        return self.parent / name

    def with_parent(self, name):
        """
        Gets path with parent ``name``.

        Returns path.
        """
        return self.parent.parent / name / self.name

    def with_score(self, name):
        """
        Gets path with score ``name``.

        Returns path.
        """
        if not self.is_score_package_path():
            return
        if self.is_wrapper():
            return self.with_name(name)
        if self.is_contents():
            return self.scores(name, name)
        path = self.scores(name, name)
        for part in self.parts[len(self.scores.parts) + 2:]:
            path /= part
        return path

    def write_metadata_py(self, metadata):
        """
        Writes ``metadata`` to ``__metadata__.py`` in current directory.

        Returns none.
        """
        import abjad
        metadata_py_path = self('__metadata__.py')
        lines = []
        lines.append('import abjad')
        lines.append('')
        lines.append('')
        metadata = abjad.OrderedDict(metadata)
        items = list(metadata.items())
        items.sort()
        metadata = abjad.OrderedDict(items)
        if metadata:
            line = format(metadata, 'storage')
            line = 'metadata = {}'.format(line)
            lines.append(line)
        else:
            lines.append('metadata = abjad.OrderedDict()')
        lines.append('')
        text = '\n'.join(lines)
        metadata_py_path.write_text(text)
