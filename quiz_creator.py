# For Assignment 11: Convert Assignment 9 and 10 to OOP
# 1. Upload your source code to new github repository using gitbash.
# 2. No demo needed.

import json
import os

class QuizQuestion:
    def __init__(self, question_text, options, correct_answer):
        self.question_text = question_text
        self.options = options
        self.correct_answer = correct_answer