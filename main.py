import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt


class AutoSudoku(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        self.cells = [[QLineEdit(self) for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                grid.addWidget(self.cells[i][j], i, j)
                self.cells[i][j].setFixedSize(40, 40)
                self.cells[i][j].setAlignment(Qt.AlignCenter)
        solve_button = QPushButton('Решить судоку', self)
        solve_button.clicked.connect(self.solve)
        grid.addWidget(solve_button, 10, 0, 1, 9)
        self.setWindowTitle('AutoSudoku')
        self.setGeometry(300, 300, 400, 400)

    def solve(self):
        board = np.zeros((9, 9), int)
        for i in range(9):
            for j in range(9):
                text = self.cells[i][j].text().strip()
                if text.isdigit():
                    board[i][j] = int(text)

        if solve_sudoku(board):
            for i in range(9):
                for j in range(9):
                    self.cells[i][j].setText(str(board[i][j]))
            QMessageBox.information(self, 'Message', 'Судоку решено!')
        else:
            QMessageBox.warning(self, 'Message', 'Решения не существует!')

def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    if num in board[:, col]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    if num in board[start_row:start_row + 3, start_col:start_col + 3]:
        return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    solver = AutoSudoku()
    solver.show()
    sys.exit(app.exec_())
