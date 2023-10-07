from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generator


class TicTacToeError(Exception):
    """Общий класс ошибок игры"""


class OccupiedCellError(TicTacToeError):
    """Клетка занята"""


class WrongInputError(TicTacToeError):
    """Неверный ввод хода"""


class Mark:
    CROSS: str = 'X'
    ZERO: str = '0'


class Board:
    def __init__(self) -> None:
        self._cells: list[list[str]] = [[' '] * 3 for _ in range(3)]

    def __iter__(self) -> Generator:
        for row in self._cells:
            yield row
        for col in zip(*self._cells):
            yield col
        yield [self._cells[i][i] for i in range(3)]
        yield [self._cells[i][~i] for i in range(3)]

    def __len__(self):
        return len(self._cells)

    def __str__(self) -> str:
        return '\n---------\n'.join(' | '.join(self._cells[i]) for i in range(3))

    def __getitem__(self, item: tuple[int, int]) -> str:
        row, col = item
        return self._cells[row][col]

    def fill_cell(self, row: int, col: int, mark: str) -> None:
        if self._cells[row][col] != ' ':
            raise OccupiedCellError('This cell is occupied! Please, choose another...')

        self._cells[row][col] = mark

    @property
    def draw(self) -> bool:
        for row in self._cells:
            if ' ' in row:
                return False
        return True

    @property
    def winner(self) -> str | None:
        for line in self:
            if set(line) in ({Mark.CROSS}, {Mark.ZERO}):
                return line[0]
        return None

    def __bool__(self) -> bool:
        return self.winner is None and not self.draw

    def copy(self) -> Board:
        board_copy = self.__class__()
        board_copy._cells = [row[:] for row in self._cells]
        return board_copy


class Player(ABC):
    def __init__(self, name: str, mark: str, board: Board) -> None:
        self._name = name
        self._mark = mark
        self._board = board

    @abstractmethod
    def turn(self):
        pass

    def is_winner(self, mark: str) -> bool:
        return mark == self._mark


class Human(Player):
    def turn(self) -> None:
        try:
            row, col = self._input_move()
            self._board.fill_cell(row, col, self._mark)
        except TicTacToeError as e:
            print(e)
            self.turn()

    def _input_move(self) -> tuple[int, int]:
        move: str = input(f'{self._name}, input Your move from 1 to 9: ')
        if not move.isdigit() or not 1 <= int(move) <= 9:
            raise WrongInputError('Input number of cell from 1 to 9...')

        cell: int = int(move) - 1
        row, col = cell // 3, cell % 3
        return row, col


class AI(Player):
    def __init__(self, mark: str, board: Board) -> None:
        super().__init__('AI', mark, board)

    def turn(self) -> None:
        print('AI is thinking...')
        (row, col), _ = self._minimax(self._board)
        self._board.fill_cell(row, col, self._mark)

    def _minimax(self,
                 board: Board,
                 is_maximizing: bool = True,
                 last_move: tuple[int, int] = (-1, -1)) -> tuple[tuple[int, int], int]:
        if not board:
            score = self._rate_board(board)
            return last_move, score

        best_score: int = -11 if is_maximizing else 11
        best_move: tuple[int, int] = (-1, -1)

        size: int = len(board)
        for row in range(size):
            for col in range(size):
                if board[row, col] == ' ':
                    board_copy: Board = board.copy()

                    mark: str = self._mark if is_maximizing else Mark.CROSS if self._mark == Mark.ZERO else Mark.ZERO
                    board_copy.fill_cell(row, col, mark)

                    _, score = self._minimax(board_copy, not is_maximizing, (row, col))
                    if (is_maximizing and score > best_score) or (not is_maximizing and score < best_score):
                        best_score, best_move = score, (row, col)

        return best_move, best_score

    def _rate_board(self, board: Board) -> int:
        if winner := board.winner:
            return 10 if self.is_winner(winner) else - 10
        return 0


class Game:
    def __init__(self) -> None:
        self._board = Board()

        name: str = input('Input Your name: ').title()
        human_first: bool = input('Do You want to turn first: y? ').lower() == 'y'
        (mark_human, mark_ai) = (Mark.CROSS, Mark.ZERO) if human_first else (Mark.ZERO, Mark.CROSS)
        self._human: Human = Human(name, mark_human, self._board)
        self._ai: AI = AI(mark_ai, self._board)
        self._round: int = 1 if human_first else 0

    def start(self) -> None:
        print(self._board)
        while self._board:
            self._human.turn() if self._round % 2 else self._ai.turn()
            self._round += 1
            print(self._board)
        message: str
        if winner := self._board.winner:
            message = 'You win!!!' if winner == self._human.is_winner(winner) else 'AI win!!!'
        else:
            message = 'Draw!!!'
        print(message)


def main():
    game = Game()
    game.start()


main()
