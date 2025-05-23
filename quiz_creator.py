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

        correct_answer = ""
        while correct_answer not in ["a", "b", "c", "d"]:
            correct_answer = input("What letter is the correct answer (a/b/c/d)? ").lower()
            if correct_answer not in ["a", "b", "c", "d"]:
                print("Invalid input. Please enter a, b, c, or d.")

        return QuizQuestion(question_text, options, correct_answer)
    
class QuizManager:
    def __init__(self, data_file="quiz_data.json"):
        self.data_file = data_file
        self.questions = self.load_questions()
        
    def load_questions(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                loaded_data = json.load(file)
                return [
                    QuizQuestion(question["question"], question["options"], question["answer"])
                    for question in loaded_data
                ]
        return []

    def save_questions(self):
        with open(self.data_file, "w") as file:
            json.dump([question.to_dict() for question in self.questions], file, indent=4)

    def add_question(self, quiz_question):
        self.questions.append(quiz_question)
        self.save_questions()
        print("Your question was saved!")

def main():
    quiz_manager = QuizManager()

    while True:
        new_question = QuizQuestion.create_from_input()
        if new_question is None:
            break

        quiz_manager.add_question(new_question)

        continue_input = input("\nDo you want to add another question? (yes/no): ").lower()
        if continue_input != "yes":
            break

    print(f"\nAll questions are saved to {quiz_manager.data_file}")


if __name__ == "__main__":
    main()