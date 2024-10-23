import sys

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt6.QtWidgets import QPushButton, QLabel
from PyQt6.QtWidgets import QRadioButton


class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.player = 'X'
        self.game_started = False
        self.win = False

    def initUI(self):
        self.button_grid = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        self.cordinate_win = (
            # Горизонтальные линии
            ([0, 0], [0, 1], [0, 2]), ([1, 0], [1, 1], [1, 2]), ([2, 0], [2, 1], [2, 2]),
            # Вертикальные линии
            ([0, 0], [1, 0], [2, 0]), ([0, 1], [1, 1], [2, 1]), ([0, 2], [1, 2], [2, 2]),
            # Диагонали
            ([0, 0], [1, 1], [2, 2]), ([0, 2], [1, 1], [2, 0])
        )

        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle('Крестики-нолики')

        # --------------------------------------------------------------------
        # Создаем радиокнопки
        self.x_radio = QRadioButton('X', self)
        self.o_radio = QRadioButton('O', self)
        self.x_radio.setChecked(True)

        # Горизонтальный макет для радиокнопок
        self.button_group = QHBoxLayout()

        self.button_group.addStretch()  # Растяжка слева для центровки по горизонтали
        self.button_group.addWidget(self.x_radio)
        self.button_group.addSpacing(20)  # Отступ между кнопками
        self.button_group.addWidget(self.o_radio)
        self.button_group.addStretch()  # Растяжка справа для центровки по горизонтали

        # Основной вертикальный макет
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(self.button_group)  # Добавляем кнопки на самый верх
        main_layout.addStretch()  # Растягиваем оставшееся пространство снизу

        # Устанавливаем основной макет для виджета
        self.setLayout(main_layout)

        self.x_radio.toggled.connect(self.reset_game)
        self.o_radio.toggled.connect(self.reset_game)
        # ------------------------------------------------------------------------

        grid_layout = QGridLayout()

        for row in range(3):
            for col in range(3):
                button = QPushButton('', self)  # Изначально пустые кнопки
                button.setFixedSize(50, 50)  # Устанавливаем фиксированный размер 50x50
                button.clicked.connect(
                    lambda checked, b=button: self.handler_click(b))  # Привязываем обработчик нажатия
                self.button_grid[row][col] = button  # Сохраняем кнопку в сетке
                grid_layout.addWidget(button, row, col)

        # Устанавливаем отступы и границы сетки
        grid_layout.setHorizontalSpacing(10)
        grid_layout.setVerticalSpacing(10)
        grid_layout.setContentsMargins(150, 100, 150, 200)  # Устанавливаем внешние границы сетки

        # Добавляем сеточный макет в основной макет
        main_layout.addLayout(grid_layout)

        # ---------------------------------------------------------

        self.new_game_button = QPushButton('Новая игра', self)
        self.new_game_button.clicked.connect(self.reset_game)
        self.new_game_button.setGeometry(200, 400, 100, 20)

        self.result = QLabel('', self)
        self.result.move(215, 350)

    def switch_player(self):
        self.player = 'X' if self.x_radio.isChecked() else 'O'

    def update_player(self):
        self.player = 'O' if self.player == 'X' else 'X'

    def disable_all_buttons(self):
        # Блокируем все кнопки на поле
        for row in range(3):
            for col in range(3):
                self.button_grid[row][col].setEnabled(False)

    def enabled_all_buttons(self):
        for row in range(3):
            for col in range(3):
                self.button_grid[row][col].setEnabled(True)

    def handler_click(self, button):
        if not self.game_started:
            # Если игра не начата, устанавливаем игрока и начинаем чередование
            self.switch_player()
            self.game_started = True

        # Обработчик нажатия на кнопку
        if button.text() == '':  # Проверяем, нажата ли пустая кнопка
            button.setText(self.player)  # Устанавливаем текст кнопки
            self.check_win()  # Проверяем победу
            if self.win:
                self.disable_all_buttons()
            else:
                self.check_draw()
                self.update_player()  # Переключаем игрока, если нет победы

    def check_win(self):
        # Проверка выигрышных комбинаций
        for win_cord in self.cordinate_win:
            values = [self.button_grid[spisok][value].text() for spisok, value in win_cord]
            if len(set(values)) == 1 and values[0] != '':  # Все три значения одинаковы и не пусты
                self.win = True
                self.show_winner_message(values[0])  # Выводим победителя
                return

    def show_winner_message(self, winner):
        if winner != 'draw':
            self.result.setText(f'Выиграл {winner}!')
        else:
            self.result.setText(f'Ничья!')

    def check_draw(self, message='draw'):
        all_filled = all(self.button_grid[row][col].text() != '' for row in range(3) for col in range(3))
        if all_filled and not self.win:
            self.show_winner_message(message)

            # Функция для сброса игры

    def reset_game(self):
        for row in range(3):
            for col in range(3):
                self.button_grid[row][col].setText('')  # Очищаем все кнопки

        self.enabled_all_buttons()
        self.switch_player()  # Устанавливаем начального игрока
        self.game_started = False
        self.win = False  # Сбрасываем статус победы
        self.result.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    class_ = TicTacToe()
    class_.show()
    sys.exit(app.exec())
