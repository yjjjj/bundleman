# coding:utf-8


import sys
from PySide6.QtWidgets import (QApplication, QLabel, QVBoxLayout, QWidget,
                               QPushButton, QGraphicsOpacityEffect, QMainWindow)
from PySide6.QtCore import QTimer, QPropertyAnimation, Qt
from PySide6.QtGui import QFont, QPalette, QColor


class FadeLabel(QWidget):
    def __init__(self, message_text, message_color, parent=None):
        super().__init__(parent)
        self.message_text = message_text
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 无边框，保持在顶部
        self.setAttribute(Qt.WA_TranslucentBackground)     # 设置背景透明

        self.layout = QVBoxLayout(self)

        # 设置字体、大小和颜色
        font = QFont("Arial", 20, QFont.Bold)
        self.palette = QPalette()
        self.palette.setColor(QPalette.WindowText, QColor(message_color[0], message_color[1], message_color[2]))

        # 设置背景颜色
        self.palette.setColor(QPalette.Window, QColor("red"))

        self.label = QLabel(self.message_text, self)
        self.label.setFont(font)
        self.label.setPalette(self.palette)

        self.layout.addWidget(self.label)
        self.label.setAlignment(Qt.AlignCenter)

        self.opacity_effect = QGraphicsOpacityEffect(self.label)
        self.label.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")

        self.setLayout(self.layout)
        self.adjustSize()

    def animate_opacity(self, start_value, end_value, duration):
        self.animation.stop()
        self.animation.setDuration(duration)
        self.animation.setStartValue(start_value)
        self.animation.setEndValue(end_value)
        self.animation.start()

    def message_show(self, parent=None, warning=False):
        # Center the notification relative to the given parent.
        if parent:
            parent_center = parent.geometry().center()
            self.move(parent_center - self.rect().center())
        self.show()
        self.animate_opacity(0, 1, 1000)

        if warning:
            # 设置显示背景
            self.label.setAutoFillBackground(True)
            QTimer.singleShot(3000, self.start_fading_out)
        else:
            QTimer.singleShot(2000, self.start_fading_out)

    def start_fading_out(self):
        self.animate_opacity(1, 0, 1000)
        QTimer.singleShot(2000, self.close)  # 动画结束后关闭窗口


# self.notification = FadeLabel("Database Update Complete", (155, 125, 195))
# self.notification.message(self)  # Pass 'self' to adjust positioning

# self.notification.message(self, warning=True)
# main_window = self.sender().parent().parent()
# self.notification.message(main_window)

