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
    
    def to_dict(self):
        return {
            "question": self.question_text,
            "options": self.options,
            "answer": self.correct_answer
        }
    
    @staticmethod
    def create_from_input():
        print("\n=== Create a New Quiz Question ===")
        question_text = input("Input your question here or type 'stop' to finish: ")
        if question_text.lower() == "stop":
            return None

        options = {}
        options["a"] = input("Input option a: ")
        options["b"] = input("Input option b: ")
        options["c"] = input("Input option c: ")
        options["d"] = input("Input option d: ")