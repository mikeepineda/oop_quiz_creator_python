import sys
import json
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QMessageBox, QFileDialog, QProgressBar
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect


class QuizApplication(QWidget):
    def __init__(self, quiz_questions_list):
        super().__init__()
        self.quiz_questions = random.sample(quiz_questions_list, len(quiz_questions_list))
        self.current_question_index = 0
        self.current_score = 0
        self.time_limit_seconds = 15
        self.question_timer = QTimer()
        self.remaining_seconds = self.time_limit_seconds

        self.initialize_interface()
        self.load_next_question()