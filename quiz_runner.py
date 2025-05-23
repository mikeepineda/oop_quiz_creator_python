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

    def initialize_interface(self):
        self.setWindowTitle('Quiz Application')
        self.setGeometry(100, 100, 600, 400)

        self.main_layout = QVBoxLayout()

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(len(self.quiz_questions))
        self.progress_bar.setValue(0)
        self.main_layout.addWidget(self.progress_bar)

        self.timer_display_label = QLabel('', self)
        self.timer_display_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.timer_display_label)

        self.quiz_question_label = QLabel('', self)
        self.quiz_question_label.setWordWrap(True)
        self.quiz_question_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.quiz_question_label)

        self.answer_option_buttons = []
        for option_number in range(4):
            answer_button = QPushButton('', self)
            answer_button.clicked.connect(self.evaluate_selected_answer)
            self.main_layout.addWidget(answer_button)
            self.answer_option_buttons.append(answer_button)

        self.setLayout(self.main_layout)
        self.question_timer.timeout.connect(self.update_timer_display)

    def load_next_question(self):
        if self.current_question_index < len(self.quiz_questions):
            self.remaining_seconds = self.time_limit_seconds
            self.question_timer.start(1000)
            self.update_timer_display_text()

            current_question = self.quiz_questions[self.current_question_index]
            self.quiz_question_label.setText(
                f"Q{self.current_question_index + 1}: {current_question['question']}"
            )

            fade_animation = QPropertyAnimation(self.quiz_question_label, b"geometry")
            fade_animation.setDuration(500)
            fade_animation.setStartValue(QRect(0, 0, 600, 0))
            fade_animation.setEndValue(QRect(0, 0, 600, 100))
            fade_animation.start()

            option_pairs = list(current_question['options'].items())
            self.correct_option_key = current_question['answer']

            for button_index, (option_key, option_text) in enumerate(option_pairs):
                answer_button = self.answer_option_buttons[button_index]
                answer_button.setText(f"{option_key}. {option_text}")
                answer_button.setProperty('answer_key', option_key)
                answer_button.setEnabled(True)

            self.progress_bar.setValue(self.current_question_index)
        else:
            self.display_final_score()

    def update_timer_display(self):
        self.remaining_seconds -= 1
        self.update_timer_display_text()
        if self.remaining_seconds <= 0:
            self.question_timer.stop()
            QMessageBox.information(self, "Time's Up", "⏰ Time's up for this question!")
            self.current_question_index += 1
            self.load_next_question()

    def update_timer_display_text(self):
        self.timer_display_label.setText(f"Time left: {self.remaining_seconds} seconds")

    def evaluate_selected_answer(self):
        self.question_timer.stop()
        clicked_button = self.sender()
        selected_option_key = clicked_button.property('answer_key')
        current_question_data = self.quiz_questions[self.current_question_index]
        correct_answer_text = current_question_data['options'][self.correct_option_key]

        if selected_option_key == self.correct_option_key:
            QMessageBox.information(self, "Result", "✅ Correct!")
            self.current_score += 1
        else:
            QMessageBox.information(
                self,
                "Result",
                f"❌ Incorrect.\nCorrect answer: {self.correct_option_key}. {correct_answer_text}"
            )

        self.current_question_index += 1
        self.load_next_question()

    def display_final_score(self):
        QMessageBox.information(
            self,
            "Final Score",
            f"🎉 You scored {self.current_score} out of {len(self.quiz_questions)}"
        )
        self.close()

class QuizFileLoader:
    @staticmethod
    def load_quiz_data_from_file():
        file_dialog = QFileDialog()
        selected_file_path, selected_filter = file_dialog.getOpenFileName(
            None, "Select Quiz File", "", "JSON Files (*.json)"
        )
        if selected_file_path:
            with open(selected_file_path, 'r') as quiz_file:
                return json.load(quiz_file)
        return None


class QuizProgramRunner:
    def run(self):
        quiz_application_instance = QApplication(sys.argv)
        quiz_data = QuizFileLoader.load_quiz_data_from_file()
        if quiz_data:
            quiz_interface_window = QuizApplication(quiz_data)
            quiz_interface_window.show()
            sys.exit(quiz_application_instance.exec_())
        else:
            QMessageBox.critical(None, "Error", "Failed to load quiz file.")
            sys.exit()

if __name__ == "__main__":
    quiz_program = QuizProgramRunner()
    quiz_program.run()