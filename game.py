class Board:
    def __init__(self) -> None:
        self._cells: list[list[str]] = [[' '] * 3 for _ in range(3)]
        # self._cells = [['1', '2', '0'],
        #                ['4', '0', '6'],
        #                ['0', '8', ' ']]

    def __iter__(self):
        for row in self._cells:
            yield row
        for col in zip(*self._cells):
            yield col
        yield [self._cells[i][i] for i in range(3)]
        yield [self._cells[i][~i] for i in range(3)]

    def __str__(self) -> str:
        return '\n---------\n'.join(' | '.join(self._cells[i]) for i in range(3))

    def _fill_cell(self, cell: str, mark: str) -> None:
        if not cell.isdigit or not 1 <= int(cell) <= 9:
            raise ValueError('Input number of cell from 1 to 9...')

        cell = int(cell) - 1
        row, col = cell // 3, cell % 3
        if self._cells[row][col] != ' ':
            raise ValueError('This cell is occupied! Please, choose another...')

        self._cells[row][col] = mark

    @property
    def _is_draw(self) -> bool:
        for row in self._cells:
            if ' ' in row:
                return False
        return True

    @property
    def _is_winner(self) -> str | None:
        for line in self:
            if set(line) in ({'X'}, {'0'}):
                return line[0]


board = Board()
board._fill_cell('9', 'X')
board._fill_cell('9', 'X')
print(board)
