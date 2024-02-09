import random
from sympy import *


class LogicProofTutor:
 
    userOperators = {'^','∨','¬','→','⊕','↔'}
    pythonOperators = {'&','|','~','>>','^'}
    user_to_python_operators = {'∧': '&', '∨': '|', '¬': '~', '→': '>>', '⊕': '^'}
    validAlpha = {"p","q"," ","(",")", "a"}   
    
    def __init__(self):
        self.problems = []
        self.user_profile = {'correct_steps': 0, 'total_steps': 0}
      
    def get_user_proposition(self):
        user_input = input("Enter a propositional statement: ")
        if (user_input):
            try:
                self.check_syntax(user_input)
                converted_user_input = self.convert_to_python_operators(user_input)
                parsed_expr = sympify(converted_user_input)
                self.problems.append(parsed_expr)
            except SympifyError:
                print("Conversion error from userOperators to pythonOperators.")
                   
                
              
                
    def convert_to_python_operators(self, user_input):
        for user_op, python_op in self.user_to_python_operators.items():
             user_input = user_input.replace(user_op, python_op)
        return user_input
     
    

    def check_syntax(self, user_input):
        stack = []
        consecutive_letters = None
        
        for char in user_input:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack or stack.pop() != '(':
                    print("Invalid Syntax. Unbalanced brackets.")
                    return False
            elif char.isalpha():
                if consecutive_letters and consecutive_letters.isalpha():
                    print("Invalid syntax. Consecutive letters are not allowed.")
                    return False
                
            consecutive_letters = char
                
                    
            if char not in self.userOperators and char not in self.validAlpha:
                print(char + " is Invalid syntax. Please enter a valid propositional statement.")
                return False
            
        if stack:
            print("Invalid syntax. Unbalanced brackets.")
            return False
            
        #consecutive_letters = any(user_input[i] == user_input[i + 1] and user_input[i] for i in range(len(user_input) - 1))
        #if consecutive_letters:
            #print("Invalid syntax. Consecutive letters are not allowed.")
            #return False

        return True
    


    def display_problem(self):
        print("Current Problem:")
        print(self.problems[0])

    def get_user_input(self):
        while True:
            user_input = input("Enter your logical proof step: ")
            if self.check_syntax(user_input):
                return user_input

    def evaluate_user_input(self, user_input):
        # Simplified evaluation logic - replace with actual proof evaluation
        if "implies" in user_input and "or" in user_input:
            print("Correct! Well done.")
            self.user_profile['correct_steps'] += 1
        else:
            print("Incorrect. Please review your proof steps.")
        self.user_profile['total_steps'] += 1

    def display_feedback(self):
        print("Feedback:")
        print(f"You have {self.user_profile['correct_steps']} correct steps out of {self.user_profile['total_steps']} total steps.")

    def display_hint(self):
        print("Hint: Consider using the logical equivalence rules.")

    def start_tutor(self):
        print("Welcome to the Logic and Proof Tutor CLI!")
        self.get_user_proposition()
        while self.problems:
            self.display_problem()
            user_input = self.get_user_input()
            self.evaluate_user_input(user_input)
            self.display_feedback()
            if self.user_profile['correct_steps'] < 2:
                self.display_hint()
            self.problems.pop(0)

        print("Congratulations! You have completed all problems in the tutor.")

if __name__ == "__main__":
    tutor = LogicProofTutor()
    tutor.start_tutor()
