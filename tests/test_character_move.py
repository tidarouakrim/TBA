import pytest
from unittest.mock import patch

from room import Room
from character import Character
from game import Game
from actions import Actions


def test_move_stays_when_choice_false():
    r1 = Room('r1', '')
    r2 = Room('r2', '')
    r1.exits = {'N': r2}
    r2.exits = {'S': r1}
    char = Character('Test', 'desc', r1, ['hi'])

    with patch('random.choice', return_value=False):
        assert char.move() is False
        assert char.current_room is r1


def test_move_no_exits_returns_false():
    r1 = Room('r1', '')
    r1.exits = {'N': None, 'E': None, 'S': None, 'O': None, 'U': None, 'D': None}
    char = Character('Test', 'desc', r1, ['hi'])

    with patch('random.choice', return_value=True):
        assert char.move() is False
        assert char.current_room is r1


def test_move_moves_to_adjacent_when_choice_true():
    r1 = Room('r1', '')
    r2 = Room('r2', '')
    r1.exits = {'N': r2}
    r2.exits = {'S': r1}
    char = Character('Test', 'desc', r1, ['hi'])

    # random.choice called twice: first for True/False, then to pick the room
    with patch('random.choice', side_effect=[True, r2]):
        assert char.move() is True
        assert char.current_room is r2


def test_actions_go_moves_characters():
    with patch('builtins.input', return_value='Tester'):
        g = Game()
        g.setup()

    with patch.object(Character, 'move') as mocked_move:
        result = Actions.go(g, ['go', 'E'], 1)
        assert result is True
        mocked_move.assert_called()


def test_actions_back_moves_characters():
    with patch('builtins.input', return_value='Tester'):
        g = Game()
        g.setup()

    # Move player to create history
    Actions.go(g, ['go', 'E'], 1)

    with patch.object(Character, 'move') as mocked_move:
        result = Actions.back(g, ['back'], 0)
        assert result is True
        mocked_move.assert_called()


def test_process_command_look_does_not_move_characters():
    with patch('builtins.input', return_value='Tester'):
        g = Game()
        g.setup()

    with patch.object(Character, 'move') as mocked_move:
        g.process_command('look')
        mocked_move.assert_not_called()


def test_go_moves_each_character_once():
    with patch('builtins.input', return_value='Tester'):
        g = Game()
        g.setup()

    # Count characters before move
    total_chars = sum(len(room.characters) for room in g.rooms)

    with patch.object(Character, 'move') as mocked_move:
        result = Actions.go(g, ['go', 'E'], 1)
        assert result is True
        # Each character should be invoked exactly once
        assert mocked_move.call_count == total_chars


def test_back_moves_each_character_once():
    with patch('builtins.input', return_value='Tester'):
        g = Game()
        g.setup()

    # Move player to create history so back() will move
    Actions.go(g, ['go', 'E'], 1)

    total_chars = sum(len(room.characters) for room in g.rooms)

    with patch.object(Character, 'move') as mocked_move:
        result = Actions.back(g, ['back'], 0)
        assert result is True
        assert mocked_move.call_count == total_chars


def test_go_does_not_move_characters_when_player_cannot_move():
    with patch('builtins.input', return_value='Tester'):
        g = Game()
        g.setup()

    # Try to go where there is no exit from starting room (gare has N=None, S=None, O=None)
    with patch.object(Character, 'move') as mocked_move:
        result = Actions.go(g, ['go', 'N'], 1)
        assert result is False
        mocked_move.assert_not_called()
