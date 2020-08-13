import argparse
import logging
import math
import mmap
import os
import re
import string


def main():
    parser = argparse.ArgumentParser(
        description='Generate a box score for your Draft Day Sports 2020 game.')
    parser.add_argument('-t', '--teams', nargs=2, required=True,
                        help='The teams that played in the game you\'re looking for.')
    parser.add_argument('-f', '--file', nargs=1, required=True,
                        help='The filepath to the .cbb file associated with your saved game.')
    parser.add_argument('-to', '--text-out', nargs=1,
                        help='The filepath to the directory where text output will be written.')
    parser.add_argument('-v', '--verbose')

    args = parser.parse_args()
    # verify args
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    path_to_data = args.file[0]
    if not os.path.exists(path_to_data):
        logging.getLogger(__name__).critical(
            'Must declare a valid .cbb filepath. %s does not exist', path_to_data)
    _, ext = os.path.splitext(path_to_data)
    if ext != '.cbb':
        logging.getLogger(__name__).critical(
            'Must declare a valid .cbb filepath. %s isn\'t a .cbb file.', path_to_data)
        return

    teams = args.teams

    logging.getLogger(__name__).info('\nParsing .cbb file...\n')
    file_parser = FileParser(path_to_data, teams)
    team_players_dict = file_parser.parse()

    for team in teams:
        processors = []
        total_tracker = TotalTracker()
        processors.append(total_tracker)
        printer = PrettyPrinter(len(team_players_dict[team]), total_tracker)

        if args.text_out is not None:
            if os.path.exists(args.text_out[0]) == False:
                logging.getLogger(__name__).critical(
                    'Out text directory is not a valid directory. %s does not exist.', args.text_out[0])
                processors.append(ConsoleWriter(printer))
            else:
                processors.append(FileWriter(printer, teams, args.text_out[0]))
        else:
            processors.append(ConsoleWriter(printer))

        logging.getLogger(__name__).info('\nProcessing output for %s\n', team)
        processorManager = ProcessorManager(
            team_players_dict[team], processors)
        processorManager.process()

    logging.getLogger(__name__).info('\n--- Finished ---\n')
    return


class PlayerStatIterator:
    def __init__(self, mm, index):
        self._mm = mm
        self._index = index

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= self._mm.size():
            raise StopIteration
        stat = int.from_bytes(
            self._mm[self._index:self._index + 1], 'little', signed=True)
        self._index += 2
        return str(stat)


class FileParser:
    def __init__(self, path, teams):
        self._path = path
        self._teams = teams

    def open_file(self):
        inFile = None
        try:
            inFile = os.open(self._path, os.O_RDONLY)
        except IOError:
            logging.getLogger(__name__).critical(
                'Unable to open %s, does it exist?', self._path)
            return []
        mm = mmap.mmap(inFile, 0, access=mmap.ACCESS_READ)
        return [mm, inFile]

    def close_file(self, resources):
        for resource in resources:
            if isinstance(resource, mmap.mmap):
                resource.close()
            else:
                os.close(resource)

    def locate_player(self, re_pattern, mm, span):
        result = re_pattern.search(mm, span[0], span[1])
        if result is None:
            return None
        return (result.start(), result.end())

    def reverse_not_in_set_search(self, mm, index, search_set):
        hit = True
        while hit and index > 0:
            if mm[index] not in search_set:
                hit = False
            index -= 1
        return index

    def parse_player_name(self, mm, span):
        # each player has a XX.png in the data following his name
        pattern = re.compile(rb'png')
        # regex from furthest to closest match
        # we have to add extra padding because the file grows
        # with each game played
        first_name = ''
        last_name = ''
        search_span = (max(span[0] - 4000, 0), span[0])
        while True:
            result = pattern.search(mm, search_span[0], search_span[1])
            if result is None:
                break
            search_span = (result.end(), search_span[1])
        # .png is 4 bytes, plus the name of the file
        # then we hit non-ascii bytes, then we're finally at the
        # player's name
        index = search_span[0] - 4
        ascii_set = set(bytes(string.printable, 'ascii'))
        index = self.reverse_not_in_set_search(mm, index, ascii_set)
        # once we hit non-ascii bytes then we know to jump back 2
        # and that's where the last-name ends (exclusive)
        index -= 1
        last_name_end = index + 1
        index = self.reverse_not_in_set_search(mm, index, ascii_set)
        # this time a non-ascii indicates we've found the byte before the
        # first letter of the last name
        last_name = mm[index + 2:last_name_end]
        last_name = last_name.decode('utf-8')

        # next previous byte is the byte after the last character of the
        # first name
        index -= 1
        first_name_end = index + 1
        # seek backwards to the beginning of the first name
        index = self.reverse_not_in_set_search(mm, index, ascii_set)
        first_name = mm[index + 2:first_name_end]
        first_name = first_name.decode('utf-8')
        return first_name + ' ' + last_name

    def parse_player(self, mm, span):
        name = self.parse_player_name(mm, span)
        player_iter = PlayerStatIterator(mm, span[1] + 15)

        def get_starting_position(player_iter):
            _ = next(player_iter)  # garbage value
            pos = next(player_iter)  # position, but might be 0
            if pos == 0:
                return None
            return pos
        return Player(name, next(player_iter), next(player_iter), next(player_iter), next(player_iter), next(player_iter), next(player_iter), next(player_iter), next(player_iter), next(player_iter), next(player_iter), next(player_iter), next(player_iter), next(player_iter), next(player_iter), next(player_iter), next(player_iter), next(player_iter), next(player_iter), get_starting_position(player_iter))

    def parse_players(self, mm, regex_str, players):
        pattern = re.compile(regex_str, re.DOTALL)
        # loop while span is not None
        span = (0, 0)
        while True:
            span = self.locate_player(
                pattern, mm, (span[1], mm.size() - span[0]))
            if span is None:
                break
            players.append(self.parse_player(mm, span))

    def parse(self):
        team_players_dict = {
            self._teams[0]: [],
            self._teams[1]: []
        }
        resources = self.open_file()
        if (len(resources)):
            mm = resources[0]
            pattern = self._teams[0] + '..' + self._teams[1]
            self.parse_players(mm, pattern.encode('utf-8'),
                               team_players_dict[self._teams[0]])
            pattern = self._teams[1] + '..' + self._teams[0]
            self.parse_players(mm, pattern.encode('utf-8'),
                               team_players_dict[self._teams[1]])
        self.close_file(resources)
        return team_players_dict


class ProcessorManager:
    def __init__(self, players, processors):
        self._players = players
        self._processors = processors

    def process(self):
        # sort players so that we do starters by position first
        # and then in order of playing time.
        def startersorter(player):
            if int(player.get_starting_position()) == 0:
                return 6
            else:
                return int(player.get_starting_position())
        self._players = sorted(
            self._players, key=lambda obj: int(obj.get_min()), reverse=True)
        self._players = sorted(self._players, key=startersorter)
        for player in self._players:
            for processor in self._processors:
                processor.process_player(player)
        for processor in self._processors:
            processor.finalize()


class PlayerProcessor:
    # Returns the fields on `Player` that this analyzer reads.
    def get_fields(self):
        return []

    def process_player(self):
        return

    def finalize(self):
        return


class Printer(PlayerProcessor):
    # Should be called after `finalize`
    def get_lines(self):
        return []

    def get_format(self):
        return


class TotalTracker(PlayerProcessor):
    def __init__(self):
        self.total_fga = 0
        self.total_fgm = 0
        self.total_tpa = 0
        self.total_tpm = 0
        self.total_fta = 0
        self.total_ftm = 0
        self.total_oreb = 0
        self.total_dreb = 0
        self.total_ast = 0
        self.total_stl = 0
        self.total_blk = 0
        self.total_to = 0
        self.total_pf = 0
        self.total_pts = 0

    def get_fields(self):
        return [
            'fga',
            'fgm',
            'tpa',
            'tpm',
            'fta',
            'ftm',
            'oreb',
            'dreb',
            'ast',
            'stl',
            'blk',
            'to',
            'pf',
            'pts',
        ]

    def process_player(self, player):
        for field in self.get_fields():
            player_field_value = getattr(player, 'get_' + field)()
            player_field_int_value = int(player_field_value)
            self_total_field_name = 'total_' + field
            current_total_field_value = getattr(self, self_total_field_name)
            setattr(self, self_total_field_name,
                    current_total_field_value + player_field_int_value)


class FileWriter(PlayerProcessor):
    def __init__(self, printer, teams, dir_path):
        self._printer = printer
        self._teams = teams
        self._dir_path = dir_path

    def get_fields(self):
        return self._printer.get_fields()

    def process_player(self, player):
        return self._printer.process_player(player)

    def finalize(self):
        self._printer.finalize()
        filepath = os.path.join(self._dir_path, ''.join(
            [self._teams[0], ' ', self._teams[1], ' ', 'box score.', self._printer.get_format()]))
        outFile = None
        if os.path.exists(filepath):
            try:
                outFile = open(filepath, 'a')
            except IOError:
                logging.getLogger(__name__).critical(
                    'Out text directory is not a valid directory. %s does not exist.', self._dir_path)
        else:
            try:
                outFile = open(filepath, 'w+')
            except IOError:
                logging.getLogger(__name__).critical(
                    'Out text directory is not a valid directory. %s does not exist.', self._dir_path)
                return
        lines = self._printer.get_lines()
        outFile.writelines(lines)
        outFile.writelines(['\n', '\n'])
        outFile.close()
        logging.getLogger(__name__).info('Text file written to %s', filepath)
        return


class ConsoleWriter(PlayerProcessor):
    def __init__(self, printer):
        self._printer = printer

    def get_fields(self):
        return self._printer.get_fields()

    def process_player(self, player):
        return self._printer.process_player(player)

    def finalize(self):
        self._printer.finalize()
        for line in self._printer.get_lines():
            logging.getLogger(__name__).info(line + '\n')
        return


class PrettyPrinter(Printer):
    def __init__(self, player_count, total_tracker, field_padding=2):
        self._total_tracker = total_tracker
        self._field_padding = field_padding

        self._fields = [
            'Name',
            'Min',
            'FG',
            '3PT',
            'FT',
            'OREB',
            'DREB',
            'REB',
            'AST',
            'STL',
            'BLK',
            'TO',
            'PF',
            'PTS',
            '+/-',
        ]
        self._field_values = [[''] * len(self._fields)
                              for i in range(player_count + 2)]
        self._max_value_length = [0] * len(self._fields)
        self._lines = [''] * (player_count + 2)

        # make the first row
        self._field_values[0] = self._fields
        for index in range(len(self._fields)):
            field = self._fields[index]
            self._max_value_length[index] = len(field)
        self._current_row = 1

    def get_fields(self):
        def special_to_lowercase(field):
            if (field == '+/-'):
                return 'plus_or_minus'
            else:
                return str.lower(field)

        return list(map(special_to_lowercase, self._fields))

    def process_player(self, player):
        player_fields = self.get_fields()
        for index in range(len(player_fields)):
            value = getattr(player, 'get_' + player_fields[index])()
            self._max_value_length[index] = max(
                len(value), self._max_value_length[index])
            self._field_values[self._current_row][index] = value
        self._current_row += 1

    def get_total_fields(self):
        return [
            'TEAM',  # name
            '',  # mins
            ''.join([
                str(self._total_tracker.total_fgm),
                '-',
                str(self._total_tracker.total_fga),
            ]),
            ''.join([
                str(self._total_tracker.total_tpm),
                '-',
                str(self._total_tracker.total_tpa),
            ]),
            ''.join([
                str(self._total_tracker.total_ftm),
                '-',
                str(self._total_tracker.total_fta),
            ]),
            str(self._total_tracker.total_oreb),
            str(self._total_tracker.total_dreb),
            str(self._total_tracker.total_oreb + \
                self._total_tracker.total_dreb),
            str(self._total_tracker.total_ast),
            str(self._total_tracker.total_stl),
            str(self._total_tracker.total_blk),
            str(self._total_tracker.total_to),
            str(self._total_tracker.total_pf),
            str(self._total_tracker.total_pts),
            '',  # +/-
        ]

    def include_totals(self):
        total_fields = self.get_total_fields()
        for index in range(len(total_fields)):
            value = total_fields[index]
            self._max_value_length[index] = max(
                len(value), self._max_value_length[index])
            self._field_values[-1][index] = value

    def finalize(self):
        # add the totals to the _field_values list
        self.include_totals()

        for row in range(len(self._field_values)):
            field_values = [''] * len(self._field_values)
            player_field_values = self._field_values[row]
            if player_field_values[1] == '0':  # Minutes == 0
                player_field_values = [player_field_values[0], 'DNP']
            for field_index in range(len(player_field_values)):
                field_value = player_field_values[field_index]

                # space length is difference in longest field value + padding
                space_length = self._max_value_length[field_index] - len(
                    field_value) + self._field_padding
                field_values[field_index] = field_value + (' ' * space_length)
            field_values.append('\n')
            self._lines[row] = ''.join(field_values)

    def get_lines(self):
        return self._lines

    def get_format(self):
        return 'txt'

# All member variable values should be strings.


class Player:
    def __init__(self, name, minutes, fga, fgm, fta, ftm, tpa, tpm, pts, ast, oreb, dreb, stl, blk, to, pf, plus_or_minus, rtg, started, starting_position):
        self._name = name
        self._minutes = minutes
        self._fgm = fgm
        self._fga = fga
        self._ftm = ftm
        self._fta = fta
        self._tpm = tpm
        self._tpa = tpa
        self._pts = pts
        self._ast = ast
        self._oreb = oreb
        self._dreb = dreb
        self._stl = stl
        self._blk = blk
        self._to = to
        self._pf = pf
        self._plus_or_minus = plus_or_minus
        self._rtg = rtg
        self._started = started
        self._starting_position = starting_position

    def get_name(self):
        return self._name

    def get_min(self):
        return self._minutes

    def get_fga(self):
        return self._fga

    def get_fgm(self):
        return self._fgm

    def get_fg(self):
        return ''.join([self._fgm, '-', self._fga])

    def get_tpa(self):
        return self._tpa

    def get_tpm(self):
        return self._tpm

    def get_fta(self):
        return self._fta

    def get_ftm(self):
        return self._ftm

    def get_3pt(self):
        return ''.join([self._tpm, '-', self._tpa])

    def get_ft(self):
        return ''.join([self._ftm, '-', self._fta])

    def get_oreb(self):
        return self._oreb

    def get_dreb(self):
        return self._dreb

    def get_reb(self):
        return str(int(self._oreb) + int(self._dreb))

    def get_ast(self):
        return self._ast

    def get_stl(self):
        return self._stl

    def get_blk(self):
        return self._blk

    def get_to(self):
        return self._to

    def get_pf(self):
        return self._pf

    def get_pts(self):
        return self._pts

    def get_plus_or_minus(self):
        return self._plus_or_minus

    def get_game_rating(self):
        return self._rtg

    def is_starter(self):
        return self._started

    def get_starting_position(self):
        return self._starting_position


if __name__ == '__main__':
    main()
