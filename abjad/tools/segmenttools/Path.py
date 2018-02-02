import os
import pathlib
import shutil
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Union
from typing import Tuple
from .Line import Line
from abjad.tools.datastructuretools.CyclicTuple import CyclicTuple
from abjad.tools.datastructuretools.OrderedDict import OrderedDict
from abjad.tools.datastructuretools.String import String
from abjad.tools.systemtools.IOManager import IOManager
from abjad.tools.topleveltools.activate import activate
from abjad.tools.topleveltools.deactivate import deactivate


class Path(pathlib.PosixPath):
    r'''Path in an Abjad score package.

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

    '''

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
        '__init__.py',
        '__make_pdf__.py',
        '__make_midi__.py',
        '__metadata__.py',
        '_assets',
        '_segments',
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
        r'''Calls path on `names`.
        '''
        path = self
        for name in names:
            path /= name
        return path

    def __repr__(self) -> str:
        r'''Gets interpreter representation of path.
        '''
        if bool(getattr(self, '_scores', None)):
            return "Path*('{}')".format(self)
        else:
            return "Path('{}')".format(self)

    def __rtruediv__(self, argument):
        r'''Joins path to `argument`.

        Returns new path.
        '''
        result = super(Path, self).__rtruediv__(argument)
        result._scores = getattr(self, '_scores', None)
        return result

    def __truediv__(self, argument):
        r'''Joins `argument` to path.

        Returns new path.
        '''
        result = super(Path, self).__truediv__(argument)
        result._scores = getattr(self, '_scores', None)
        return result

    ### PRIVATE PROPERTIES ###

    @property
    def _assets(self):
        '''Gets _assets directory.

        Returns path.
        '''
        if self.is_builds():
            return self('_assets')
        if self.is_build():
            return self('_assets')

    @property
    def _segments(self):
        '''Gets _segments directory.

        Returns path.
        '''
        if self.is__segments():
            return self
        if self.is_build():
            return self('_segments')

    ### PRIVATE METHODS ###

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

    def _get_score_pdf(self):
        path = self.distribution._get_file_path_ending_with('score.pdf')
        if not path:
            path = self.builds._get_file_path_ending_with('score.pdf')
        return path

    def _list_paths(self):
        paths = []
        if not self.exists():
            return paths
        predicate = self.get_name_predicate()
        is_external = self.is_external()
        is_scores = self.is_scores()
        is_segments = self.is_segments()
        introduction_segments = []
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
            path = self(name)
            try:
                path.relative_to(self)
            except ValueError:
                continue
            if path.is_introduction_segment():
                introduction_segments.append(path)
            else:
                paths.append(path)
        paths = introduction_segments + paths
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
    def build(self) -> Optional['Path']:
        r'''Gets build directory (if directory is already build or is _segments
        directory).

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score/builds/letter-score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path
            Path*('/path/to/scores/my_score/my_score/builds/letter-score')

            >>> path.build
            Path*('/path/to/scores/my_score/my_score/builds/letter-score')

            >>> path = path / '_segments'
            >>> path
            Path*('/path/to/scores/my_score/my_score/builds/letter-score/_segments')

            >>> path.build
            Path*('/path/to/scores/my_score/my_score/builds/letter-score')

        '''
        if self.is_build():
            return self
        elif self.is__segments():
            return self.contents.builds(self.parent.name)
        elif self.parent.is_build():
            return self.parent
        else:
            return None

    @property
    def builds(self) -> Optional['Path']:
        r'''Gets builds directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.builds
            Path*('/path/to/scores/my_score/my_score/builds')
            >>> path.builds('letter')
            Path*('/path/to/scores/my_score/my_score/builds/letter')

        '''
        if self.contents:
            return self.contents('builds')
        else:
            return None

    @property
    def contents(self):
        r'''Gets contents directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.contents
            Path*('/path/to/scores/my_score/my_score')
            >>> path.contents('etc', 'notes.txt')
            Path*('/path/to/scores/my_score/my_score/etc/notes.txt')

        '''
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
    def distribution(self) -> Optional['Path']:
        r'''Gets distribution directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.distribution
            Path*('/path/to/scores/my_score/my_score/distribution')
            >>> path.distribution('score.pdf')
            Path*('/path/to/scores/my_score/my_score/distribution/score.pdf')

        '''
        if self.contents:
            return self.contents('distribution')
        else:
            return None

    @property
    def etc(self) -> Optional['Path']:
        r'''Gets etc directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.etc
            Path*('/path/to/scores/my_score/my_score/etc')
            >>> path.etc('notes.txt')
            Path*('/path/to/scores/my_score/my_score/etc/notes.txt')

        '''
        if self.contents:
            return self.contents('etc')
        else:
            return None

    @property
    def materials(self) -> Optional['Path']:
        r'''Gets materials directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.materials
            Path*('/path/to/scores/my_score/my_score/materials')
            >>> path.materials('instruments')
            Path*('/path/to/scores/my_score/my_score/materials/instruments')

        '''
        if self.contents:
            return self.contents('materials')
        else:
            return None

    @property
    def scores(self) -> Optional['Path']:
        r'''Gets scores directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.scores
            Path*('/path/to/scores')
            >>> path.scores('red_score', 'red_score')
            Path*('/path/to/scores/red_score/red_score')

        '''
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
    def segments(self) -> Optional['Path']:
        r'''Gets segments directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.segments
            Path*('/path/to/scores/my_score/my_score/segments')
            >>> path.segments('segment_01')
            Path*('/path/to/scores/my_score/my_score/segments/segment_01')

        '''
        if self.contents:
            return self.contents('segments')
        else:
            return None

    @property
    def stylesheets(self) -> Optional['Path']:
        r'''Gets stylesheets directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.stylesheets
            Path*('/path/to/scores/my_score/my_score/stylesheets')
            >>> path.stylesheets('stylesheet.ily')
            Path*('/path/to/scores/my_score/my_score/stylesheets/stylesheet.ily')

        '''
        if self.contents:
            return self.contents('stylesheets')
        else:
            return None

    @property
    def test(self) -> Optional['Path']:
        r'''Gets test directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.test
            Path*('/path/to/scores/my_score/my_score/test')
            >>> path.test('test_materials.py')
            Path*('/path/to/scores/my_score/my_score/test/test_materials.py')

        '''
        if self.contents:
            return self.contents('test')
        else:
            return None

    @property
    def tools(self) -> Optional['Path']:
        r'''Gets tools directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.tools
            Path*('/path/to/scores/my_score/my_score/tools')
            >>> path.tools('SegmentMaker.py')
            Path*('/path/to/scores/my_score/my_score/tools/SegmentMaker.py')

        '''
        if self.contents:
            return self.contents('tools')
        else:
            return None

    @property
    def wrapper(self) -> Optional['Path']:
        r'''Gets wrapper directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.wrapper
            Path*('/path/to/scores/my_score')
            >>> path.wrapper('my_score', 'etc')
            Path*('/path/to/scores/my_score/my_score/etc')

        '''
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
        tag: Union[str, Callable],
        indent: int = 0,
        message_zero: bool = False,
        name: str = None,
        undo: bool = False,
        ) -> Tuple[int, int, List[str]]:
        r'''Activates `tag` in path.

        Four cases:

        Case 1: path is a file. Method activates `tag` in file.

        Case 2: path is a segment directory. Method activates `tag` in
        the segment's illustration.ly file.

        Case 3: path is segments directory. Method activates `tag` in the
        illustration.ly file in each segment.

        Case 4: path is a build directory, method activates `tag` in every ly
        file in the build's _segments directory.

        Returns triple.
        
        First item in triple is count of deactivated tags activated by method.
        
        Second item in pair is count of already-active tags skipped by method.

        Third item in pair is list of canonical string messages that explain
        what happened.
        '''
        assert isinstance(indent, int), repr(indent)
        if self.is_file():
            text = self.read_text()
            if undo:
                text, count, skipped = deactivate(text, tag, skipped=True)
            else:
                text, count, skipped = activate(text, tag, skipped=True)
            self.write_text(text)
        elif self.is_segment():
            illustration_ly = self('illustration.ly')
            assert illustration_ly.is_file()
            count, skipped, _ = illustration_ly.activate(tag, undo=undo)
            layout_ly = self('layout.ly')
            if layout_ly.is_file():
                count_, skipped_, _ = layout_ly.activate(tag, undo=undo)
                count += count_
                skipped += skipped_
        elif self.is_segments():
            count, skipped = 0, 0
            for segment in self.list_paths():
                count_, skipped_, _ = segment.activate(tag, undo=undo)
                count += count_
                skipped += skipped_
        elif self.is_build() or self.is__segments():
            count, skipped = 0, 0
            for segment_ly in self.build._segments.list_paths():
                count_, skipped_, _ = segment_ly.activate(tag, undo=undo)
                count += count_
                skipped += skipped_
        else:
            raise ValueError(self)
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
        messages = [
            whitespace + String(_).capitalize_start() + ' ...'
            for _ in messages
            ]
        return count, skipped, messages

    def add_buildspace_metadatum(
        self,
        name,
        value,
        document_name: str = None,
        ) -> None:
        r'''Adds metadatum with `name` and `value` into buildspace metadata
        with optional `document_name`.
        '''
        assert self.is_buildspace(), repr(self)
        if self.is_parts():
            part_dictionary = self.get_metadatum(
                document_name,
                OrderedDict(),
                )
            part_dictionary[name] = value
            assert String(document_name).is_shout_case()
            self.add_metadatum(document_name, part_dictionary)
        else:
            self.add_metadatum(name, value)

    def add_metadatum(self, name, value) -> None:
        r'''Adds metadatum.
        '''
        assert ' ' not in name, repr(name)
        metadata = self.get_metadata()
        metadata[name] = value
        self.write_metadata_py(metadata)

    def coerce(self, name, suffix=None):
        r'''Coerces asset `name`.

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

        Returns string.
        '''
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
        else:
            raise ValueError(self)
        return name

    def count(
        self,
        tag: Union[str, Callable],
        ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        r'''Counts `tag` in path.

        Returns two pairs.

        Pair 1 gives (active tags, activate lines).

        Pair 2 gives (deactivated tags, deactivated lines).
        '''
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
        tag: Union[str, Callable],
        indent: int = 0,
        message_zero: bool = False,
        name: str = None,
        ) -> Tuple[int, int, List[str]]:
        r'''Deactivates `tag` in path.
        '''
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
        r'''Externalizes LilyPond file parsable chunks.

        Produces skeleton score file and include file.

        Overwrites path with skeleton score when ``score_path`` is none.

        Writes include file to path with ``.ily`` suffix when ``include_path``
        is none.
        '''
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
                    line.startswith(r'\context Score')):
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
        r'''Gets asset identifier.

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

        '''
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

    def get_files_ending_with(self, name) -> List['Path']:
        r'''Gets files in path ending with `name`.
        '''
        paths = []
        for path in self.list_paths():
            if path.name.endswith(name):
                paths.append(path)
        return paths

    def get_identifier(self) -> str:
        r'''Gets identifier.

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
        '''
        if self.is_wrapper():
            result = self.contents().get_title()
        elif self.is_contents():
            result = self.get_title()
        elif self.is_dir():
            result = self.get_metadatum('name', self.name)
        else:
            result = self.name
        return String(result)

    def get_measure_count_pair(self) -> Tuple[int, int]:
        r'''Gets measure count pair.

        Reads segment metadata when path is segment.

        Reads score metadata when path is not segment.

        Returns pair of first measure number / measure count.
        '''
        if self.parent.is_segment():
            string = 'first_measure_number'
            first_measure_number = self.parent.get_metadatum(string)
            time_signatures = self.parent.get_metadatum('time_signatures')
            measure_count = len(time_signatures)
        else:
            first_measure_number = 1
            dictionary = self.contents.get_metadatum('time_signatures')
            dictionary = dictionary or OrderedDict()
            measure_count = 0
            for segment, time_signatures in dictionary.items():
                measure_count += len(time_signatures)
        return first_measure_number, measure_count

    def get_metadata(self) -> OrderedDict:
        r'''Gets __metadata__.py file in path.
        '''
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
        default: Any = None,
        ) -> Any:
        r'''Gets metadatum.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.contents.get_metadatum('foo') is None
            True

        '''
        metadata = self.get_metadata()
        metadatum = metadata.get(metadatum_name)
        if not metadatum:
            metadatum = default
        return metadatum

    def get_name_predicate(self) -> Callable:
        r'''Gets name predicate.

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

        '''
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

    def get_next_package(self, cyclic: bool = False) -> Optional['Path']:
        r'''Gets next package.

        ..  container:: example

                >>> path = abjad.Path(
                ...     '/path/to/scores/my_score/my_score',
                ...     scores='/path/to/scores',
                ...     )

            >>> path.get_next_package() is None
            True

        '''
        if not self.is_dir():
            return None
        if self.is_material():
            paths = self.materials().list_paths()
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
            paths = self.segments().list_paths()
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

    def get_next_score(self, cyclic: bool = False) -> Optional['Path']:
        r'''Gets next score.

        ..  container:: example

                >>> path = abjad.Path(
                ...     '/path/to/scores/my_score/my_score',
                ...     scores='/path/to/scores',
                ...     )

            >>> path.get_next_score() is None
            True

        '''
        if not self.is_dir():
            return None
        if not (self.is_score_package_path() or self.is_scores()):
            return None
        if self.is_scores():
            wrappers = self.list_paths()
            if wrappers:
                return wrappers[0]
        wrappers = self.scores.list_paths()
        if not wrappers:
            return None
        wrapper = self.wrapper()
        if wrapper == wrappers[-1] and not cyclic:
            return None
        index = wrappers.index(wrapper)
        wrappers = CyclicTuple(wrappers)
        return wrappers[index + 1]

    def get_part_abbreviation(self) -> Optional[str]:
        r'''Gets part abbreviation in layout.py only.
        '''
        if not self.name.endswith('layout.py'):
            return None
        for line in self.read_text().split('\n'):
            if line.startswith('part_abbreviation ='):
                globals_ = globals()
                exec(line, globals_)
                part_abbreviation = globals_['part_abbreviation']
                return part_abbreviation
        return None

    def get_previous_package(self, cyclic: bool = False) -> Optional['Path']:
        r'''Gets previous package.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.get_previous_package() is None
            True

        '''
        if not self.is_dir():
            return None
        if self.is_material():
            paths = self.materials().list_paths()
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
            paths = self.segments().list_paths()
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

    def get_previous_score(self, cyclic: bool = False) -> Optional['Path']:
        r'''Gets previous score.

        ..  container:: example

                >>> path = abjad.Path(
                ...     '/path/to/scores/my_score/my_score',
                ...     scores='/path/to/scores',
                ...     )

            >>> path.get_previous_score() is None
            True

        '''
        if not self.is_dir():
            return None
        if not (self.is_score_package_path() or self.is_scores()):
            return None
        if self.is_scores():
            wrappers = self.list_paths()
            if wrappers:
                return wrappers[-1]
        wrappers = self.scores.list_paths()
        if not wrappers:
            return None
        wrapper = self.wrapper()
        if wrapper == wrappers[0] and not cyclic:
            return None
        index = wrappers.index(wrapper)
        wrappers = CyclicTuple(wrappers)
        return wrappers[index - 1]

    def get_time_signature_metadata(self):
        r'''Gets time signature metadata for buildspace directory.

        Returns list or time signatures.
        '''
        import abjad
        if self.is_segment():
            time_signatures = self.get_metadatum('time_signatures', [])
            time_signatures = [
                abjad.TimeSignature.from_string(_) for _ in time_signatures
                ]
            return time_signatures
        time_signatures = self.contents.get_metadatum('time_signatures')
        if time_signatures is None:
            return []
        assert isinstance(time_signatures, abjad.OrderedDict)
        time_signatures_ = []
        for segment_name, strings in time_signatures.items():
            for string in strings:
                time_signature = abjad.TimeSignature.from_string(string)
                time_signatures_.append(time_signature)
        return time_signatures_

    def get_title(self, year=True):
        r'''Gets score title.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.get_title()
            '(untitled score)'
        
        Returns string.
        '''
        if year and self.get_metadatum('year'):
            title = self.get_title(year=False)
            year = self.get_metadatum('year')
            result = '{} ({})'.format(title, year)
            return result
        else:
            result = self.get_metadatum('title')
            result = result or '(untitled score)'
            return result

    def global_skip_identifiers(self) -> List[String]:
        r'''Gets global skip identifiers.
        '''
        assert not self.is_external(), repr(self);
        identifiers = []
        for segment in self.segments.list_paths():
            identifier = String(segment.name).to_segment_lilypond_identifier()
            identifier = String(f'{identifier}_GlobalSkips')
            identifiers.append(identifier)
        return identifiers

    def is__assets(self) -> bool:
        r'''Is true when path is _assets directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path = path('build', '_assets')
            >>> path.is__assets()
            True

        '''
        return self.name == '_assets'

    def is__segments(self) -> bool:
        r'''Is true when path is _segments directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score/builds/letter/_segments',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.is__segments()
            True

        '''
        return self.name == '_segments'

    def is_build(self) -> bool:
        '''Is true when path is build directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.builds('letter').is_build()
            True

        '''
        return (self.parent.name == 'builds' and
            self.name != '_segments' and
            self.name != '_assets')

    def is_builds(self) -> bool:
        r'''Is true when path is builds directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.builds.is_builds()
            True

        '''
        return self.name == 'builds'

    def is_buildspace(self) -> bool:
        r'''Is true when path is any of _segments, build, builds, segment or
        segments directories.

        Returns true or false.
        '''
        if self.is_build() or self.is_builds():
            return True
        if self.is__segments() or self.is_segment() or self.is_segments():
            return True
        return False

    def is_contents(self) -> bool:
        r'''Is true when path is contents directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.contents.is_contents()
            True

        '''
        return bool(self.scores) and self.scores(self.name, self.name) == self

    def is_distribution(self) -> bool:
        r'''Is true when path is distribution directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.distribution.is_distribution()
            True

        '''
        return self.name == 'distribution'

    def is_etc(self) -> bool:
        r'''Is true when path is etc directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.etc.is_etc()
            True

        '''
        return self.name == 'etc'

    def is_external(self) -> bool:
        r'''Is true when path is not a score package path.

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

        '''
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
        r'''Is true when path is any of material, materials, segment or
        segments directories.

        Returns true or false.
        '''
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
        r'''Is true when path is segment with name like _, _1, _2, ....

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

        '''
        if self.is_segment():
            if self.name == '_':
                return True
            if self.name[0] == '_' and self.name[1:].isnumeric():
                return True
        return False

    def is_library(self) -> bool:
        r'''Is true when path is composer library tools directory.
        '''
        import abjad
        configuration = abjad.abjad_configuration
        if configuration.composer_library_tools:
            return str(self) == configuration.composer_library_tools
        return False

    def is_material(self) -> bool:
        r'''Is true when path is material directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.materials('tempi').is_material()
            True

        '''
        return self.parent.name == 'materials'

    def is_material_or_segment(self) -> bool:
        r'''Is true when path is material directory or segment directory.

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

        '''
        return self.parent.name in ('materials', 'segments')

    def is_materials(self) -> bool:
        r'''Is true when path is materials directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.materials.is_materials()
            True

        '''
        return self.name == 'materials'

    def is_materials_or_segments(self) -> bool:
        r'''Is true when path is materials directory or segments directory.

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

        '''
        return self.name in ('materials', 'segments')

    def is_parts(self) -> bool:
        r'''Is true when directory is parts directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.builds.is_parts()
            False

            >>> path.builds('arch-a-score').is_parts()
            False

        '''
        if self.is_build():
            return self.get_metadatum('parts_directory') is True
        else:
            return False

    def is_score_build(self) -> bool:
        r'''Is true when directory is score build directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.builds.is_score_build()
            False

            >>> path.builds('arch-a-score').is_score_build()
            True

        '''
        if self.is_build():
            if self.get_metadatum('parts_directory') is True:
                return False
            return True
        else:
            return False

    def is_score_package_path(self, prototype=()) -> bool:
        r'''Is true when path is package path.

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

        '''
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
        if 'parts' in prototype and self.is_parts():
            return True
        if 'segment' in prototype and self.is_segment():
            return True
        if 'wrapper' in prototype and self.is_wrapper():
            return True
        return False

    def is_scores(self) -> bool:
        r'''Is true when path is scores directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.scores.is_scores()
            True

        '''
        return self == self.scores

    def is_segment(self) -> bool:
        r'''Is true when path is segment directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.segments('segment_01').is_segment()
            True

        '''
        return self.parent.name == 'segments'

    @staticmethod
    def is_segment_name(string) -> bool:
        r'''Is true when `string` is canonical segment name.

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

        '''
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
        r'''Is true when path is segments directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.segments.is_segments()
            True

        '''
        return self.name == 'segments'

    def is_stylesheets(self) -> bool:
        r'''Is true when path is stylesheets directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.stylesheets.is_stylesheets()
            True

        '''
        return self.name == 'stylesheets'

    def is_test(self) -> bool:
        r'''Is true when path is test directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.test.is_test()
            True

        '''
        return self.name == 'test'

    def is_tools(self) -> bool:
        r'''Is true when path is tools directory.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.tools.is_tools()
            True

        '''
        return self.name == 'tools'

    def is_wrapper(self) -> bool:
        r'''Is true when path is wrapper directory

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )
            >>> path.wrapper.is_wrapper()
            True

        '''
        return bool(self.scores) and self.scores(self.name) == self

    def list_paths(self):
        r'''Lists paths ordered by view (if any).

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.list_paths()
            []

        Returns list.
        '''
        paths = self._list_paths()
        paths = self._filter_by_view(paths)
        if self.is_scores() and self.get_metadatum('view') is None:
            paths = self._sort_by_identifier(paths)
        return paths

    def list_secondary_paths(self):
        r'''Lists secondary paths.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.list_secondary_paths()
            []

        Returns list.
        '''
        paths = []
        for path in sorted(self.glob('*')):
            if path.name in sorted(self._secondary_names):
                paths.append(path)
        return paths

    def part_name_to_identifiers(self, part_name) -> List[str]:
        r'''Changes ``part_name`` to (part container) identifiers.
        '''
        assert not self.is_external(), repr(self)
        identifiers = []
        dictionary = self.contents.get_metadatum('container_to_part')
        if not dictionary:
            raise Exception(f'missing container-to-part dictionary.')
        for segment_name, dictionary_ in dictionary.items():
            pairs = []
            for identifier, (part, timespan) in dictionary_.items():
                if part_name in part:
                    pairs.append((identifier, timespan))
            pairs.sort(key=lambda pair: pair[1])
            identifiers_ = [_[0] for _ in pairs]
            identifiers.extend(identifiers_)
        return identifiers

    def remove(self):
        r'''Removes path if it exists.

        Returns none.
        '''
        if self.is_file():
            self.unlink()
        elif self.is_dir():
            shutil.rmtree(str(self))

    def remove_metadatum(self, name):
        r'''Removes metadatum.

        Returns none.
        '''
        assert ' ' not in name, repr(name)
        metadata = self.get_metadata()
        try:
            metadata.pop(name)
        except KeyError:
            pass
        self.write_metadata_py(metadata)

    def segment_number_to_path(self, number):
        r'''Changes segment number to path.

        ..  container:: example

            >>> path = abjad.Path(
            ...     '/path/to/scores/my_score/my_score',
            ...     scores='/path/to/scores',
            ...     )

            >>> path.segment_number_to_path(1)

        Returns path.
        '''
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

    def trim(self) -> str:
        r'''Trims path.

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

        '''
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
        r'''Updates order-dependent segment metadata.

        Returns none.
        '''
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
        '''Gets path with `name`.

        Returns path.
        '''
        return self.parent / name

    def with_parent(self, name):
        '''Gets path with parent `name`.

        Returns path.
        '''
        return self.parent.parent / name / self.name

    def with_score(self, name):
        '''Gets path with score `name`.

        Returns path.
        '''
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
        r'''Writes `metadata` to `__metadata__.py` in current directory.

        Returns none.
        '''
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
