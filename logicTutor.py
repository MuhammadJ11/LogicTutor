import random
from sympy import *
from sympy.logic.boolalg import truth_table
from sympy.utilities.iterables import ibin
from sympy.abc import p,q



class LogicProofTutor:
 
    # Set containing user-defined logical operators.
    userOperators = {'^','∨','¬','→','⊕','↔'}
    # Set containing corresponding Python logical operators.
    pythonOperators = {'&','|','~','>>','^'}
    # Dictionary mapping user-defined operators to Python operators.
    user_to_python_operators = {'∧': '&', '∨': '|', '¬': '~', '→': '>>', '⊕': '^'}
    # Set containing valid alphabets and characters for propositional statements.
    validAlpha = {"p","q"," ","(",")", "a"}   
    # Initializing an empty string for user input.
    user_input = ""
    
    # Constructor method for initializing class instances.
    def __init__(self):
        # List to store premises.
        self.premises = [] 
        # List to store conclusions.
        self.conclusion = []
        self.user_profile = {'correct_steps': 0, 'total_steps': 0}
    
    # Method to get a propositional premise statement from the user.  
    def get_user_proposition(self):
        while True:
            # Prompting user for input.
            user_input = input("Enter a propositional statement: ").strip()
            if user_input:
                    # Checking syntax validity.
                    while not self.check_syntax(user_input):
                        # Prompting again if syntax is invalid.
                        user_input = input("Enter a valid propositional premise statement: ").strip()
                        # Converting user input to Sympy expression.
                    parsed_expr = self.convert_to_sympy(user_input)
                    # Adding the user input to the premises list.
                    self.premises.append(user_input)
                    # Returning the parsed expression.
                    return parsed_expr
                
    # Method to get a propositional goal statement from the user.
    def get_user_conclusion(self):
        while True:
            # Prompting user for input.
            user_input = input("Enter a propositional goal statement: ").strip()
            if user_input:
                    # Checking syntax validity.
                    while not self.check_syntax(user_input):
                        # Prompting again if syntax is invalid.
                        user_input = input("Enter a valid propositional goal statement: ").strip()
                    # Converting user input to Sympy expression.
                    parsed_expr = self.convert_to_sympy(user_input)
                    # Adding the user input to the conclusion list.
                    self.conclusion.append(user_input)
                    # Returning the parsed expression.
                    return parsed_expr

    # Method to convert user-defined operators to Python operators in a given statement.            
    def convert_to_python_operators(self, user_input):
        for user_op, python_op in self.user_to_python_operators.items():
            # Replacing user-defined operators with Python operators.
             user_input = user_input.replace(user_op, python_op)
        # Returning the modified input statement.
        return user_input
       
    # Method to convert a propositional statement to a Sympy expression. 
    def convert_to_sympy(self, user_input):
        try:
            # Converting user-defined operators to Python operators.
            converted_user_input = self.convert_to_python_operators(user_input)
             # Parsing the converted input using sympify.
            parsed_expr = sympify(converted_user_input)
            print(parsed_expr)
            # Returning the parsed expression.
            return parsed_expr
        except SympifyError:
                print("Conversion error from userOperators to pythonOperators.") 
                
    
    # Method to check the syntax of a propositional statement.
    def check_syntax(self, user_input):
        # Initializing a stack for checking bracket balance.
        stack = []
        # Variable to track consecutive letters.
        consecutive_letters = None
        
        # Iterating through each character in the user input.
        for char in user_input:
            # If the character is an opening bracket.
            if char == '(':
                # Pushing onto the stack.
                stack.append(char)
            # If the character is a closing bracket.
            elif char == ')':
                # If stack is empty or mismatched bracket.
                if not stack or stack.pop() != '(':
                    # Printing error message.
                    print("Invalid Syntax. Unbalanced brackets.")
                    # Returning False for invalid syntax
                    return False
            # If the character is an alphabet.
            elif char.isalpha():
                # If consecutive letters are found.
                if consecutive_letters and consecutive_letters.isalpha():
                    # Printing error message.
                    print("Invalid syntax. Consecutive letters are not allowed.")
                    return False
                # Updating consecutive letters.
                consecutive_letters = char
                
             # If character is not a valid operator or alphabet.       
            if char not in self.userOperators and char not in self.validAlpha:
                print(char + " is Invalid syntax. Please enter a valid propositional statement.")
                return False
        # If stack is not empty after iteration.   
        if stack:
            print("Invalid syntax. Unbalanced brackets.")
            return False
         # Returning True for valid syntax.
        return True
    
    
    def check_premises_to_conclusion(self, user_input):
        vars = [p,q]
        user_input = self.convert_to_sympy(self.user_input)
        values = truth_table(user_input, vars, input=True)
        values = list(values)
        print(values)



    def display_problem(self):
        if self.premises and self.conclusion:
            print("Current Problem:")
            print(self.premises[0] + " ⊢ " + self.conclusion[0])
        else:
            print("No problem is provided yet.")
        

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
        self.get_user_conclusion()
        while self.premises:
            self.display_problem()
            user_input = self.get_user_input()
            self.evaluate_user_input(user_input)
            self.display_feedback()
            if self.user_profile['correct_steps'] < 2:
                self.display_hint()
                self.premises.pop(0)
                self.conclusion.pop(0)
        
        print("Congratulations! You have completed all premises in the tutor.")

if __name__ == "__main__":
    tutor = LogicProofTutor()
    tutor.start_tutor()
