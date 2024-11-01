import random
from sympy import *
from proofRules import ruleChecker
from hints import Hints



class LogicProofTutor:
 
    # Set containing user-defined logical operators.
    userOperators = {'∧','∨','¬','→','⊕'} #'↔'
    # Set containing corresponding Python logical operators.
    pythonOperators = {'&','|','~','>>','^'}
    # Dictionary mapping user-defined operators to Python operators.
    user_to_python_operators = {'∧': '&', '∨': '|', '¬': '~', '→': '>>', '⊕': '^'}
    # Set containing valid alphabets and characters for propositional statements.
    validAlpha = {"p","q"," ","(",")", "a", ","}   
    # Initializing an empty string for user input.
    user_input = ""
    
    # Constructor method for initializing class instances.
    def __init__(self):
        # List to store premises.
        self.premises = [] 
        # List to store conclusions.
        self.conclusion = []
        self.proof_steps = {}
        self.hints_provider = Hints(self.premises, self.conclusion)  # Initialize Hints instance
        self.hint_count =  {'LH': 0, 'HH': 0}  # Initialize hint counts dictionary

    
    def get_user_proposition(self):
        while True:
            user_input = input("Enter propositional premise statements separated by a comma: ")
            premise_list = user_input.split(',')
            all_premises_valid = True  # Flag to track if all premises are valid

            for premise in premise_list:
                premise = premise.strip()  # Remove leading/trailing whitespace
                if not self.check_syntax(premise):
                    all_premises_valid = False
                    break  # Exit the loop as there's an invalid premise

                try:
                    self.convert_to_sympy(premise)  # Attempt to convert premise to sympy
                except (ValueError, SympifyError):
                    all_premises_valid = False
                    break  # Exit the loop as there's an invalid premise

            if all_premises_valid:
                self.premises.extend(premise_list) # All premises are valid; append them to the list
                break  # Exit the while loop as we've successfully got all valid premises
 
                
    def get_user_conclusion(self):
        while True:
            user_input = input("Enter a propositional goal statement: ").strip()
            if user_input:
                # Keep asking until a valid statement is entered
                while True:
                    try:
                        # Attempt to check syntax and convert the conclusion
                        if not self.check_syntax(user_input):
                            raise ValueError("Invalid syntax. Please enter a valid propositional goal statement.")
                        parsed_expr = self.convert_to_sympy(user_input)
                        # If successful, add to conclusions and break the loop
                        self.conclusion.append(user_input)
                        break  # Exit loop on successful conversion
                    except (ValueError, SympifyError):
                        # If either check_syntax fails or convert_to_sympy raises SympifyError, ask for input again
                        user_input = input("Enter a valid propositional goal statement: ").strip()

                return parsed_expr  # Return the valid parsed expression
                    

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
            #print(parsed_expr)
            # Returning the parsed expression.
            return parsed_expr
        except SympifyError:
                print("Conversion error. Input a valid statement.") 
                raise
    
    def check_syntax(self, user_input):
        stack = []  # Stack to track opening brackets
        last_char = None  # Variable to track last character

        for char in user_input:
            if char == '(':
                stack.append(char)  # Push opening bracket onto stack
            elif char == ')':
                if not stack or stack.pop() != '(':  # If closing bracket found but no opening bracket in stack or mismatched brackets
                    print("Invalid Syntax. Unbalanced brackets.")
                    return False
            elif char not in self.validAlpha and char not in self.userOperators:
                print(char + " is Invalid syntax. Please enter a valid propositional statement.")
                return False
            elif char.isalpha():
                if last_char and last_char.isalpha():  # If consecutive letters found
                    print("Invalid syntax. Consecutive letters are not allowed.")
                    return False


            last_char = char  # Update last character seen

        if stack:  # If stack is not empty after iteration, unbalanced brackets
            print("Invalid syntax. Unbalanced brackets.")
            return False

        return True  # Return True for valid syntax


    def display_problem(self):
        if self.premises and self.conclusion:
            print("Current Problem:")
            premises_str = " , ".join(self.premises)
            print(f"{premises_str} ⊢ {self.conclusion[0]}\n")
        else:
            print("No problem is provided yet.")
        
       
    
    def initialize_proof_with_premises(self):
        # Start with line number 1 for the first premise
        line_number = 1
        
        # Iterate over each premise in self.premises
        for premise in self.premises:
            # Add the premise to self.proof_steps with the current line number as the key
            # The value is a dictionary with details about this proof step
            self.proof_steps[line_number] = {
                'step': premise,     # The proposition for this step
                'line_dep': 'Premise',   # Indicating this step is a premise
                'rule': None         # No rule applied to premises, they are given
            }
            
            # Print the premise in a formatted way for display
            print(f"Premise/LineDep: Premise  LineNumber: ({line_number})  ProofStep: {premise} RuleApplied: Given")
            
            # Increment the line number for the next premise
            line_number += 1

            
    def validate_line_dep(self, line_dep):
        # Check if the input is exactly "Premise"
        if line_dep == "Premise":
            return True
        # Check if the input is a series of numbers, possibly separated by commas
        elif line_dep.replace(",", "").isdigit():
            # Further check if after splitting by ',', each part is a digit
            parts = line_dep.split(",")
            return all(part.isdigit() for part in parts)
        else:
            # If the input is neither "Premise" nor a series of numbers, it's invalid
            return False
    
    def get_user_input(self):
        while True:
            initial_premises_count = len(self.premises)  # Count the number of given premises at the start
            line_number = len(self.proof_steps) + 1
            print(f"LineNumber: ({line_number})")
            line_dep = input("Premise/LineDep: ").strip()

            # Validate line_dep input...
            while not self.validate_line_dep(line_dep):
                print("Invalid input for Premise/LineDep. Please enter 'Premise' or line numbers like '1' or '1,2,3'.")
                line_dep = input("Premise/LineDep: ").strip()

            proof_step_input = input("ProofStep: ").strip()
            while not proof_step_input:  # Check if proof_step_input is empty
                print("ProofStep cannot be empty. Please enter a valid propositional statement.")
                proof_step_input = input("ProofStep: ").strip()
                
            while not self.check_syntax(proof_step_input):
                print("Invalid syntax. Please enter a valid propositional statement.")
                proof_step_input = input("ProofStep: ").strip()
                
            try:
                self.convert_to_sympy(proof_step_input)
            except (ValueError, SympifyError):
                proof_step_input = input("ProofStep: ").strip()

            rule_applied = input("RuleApplied: ").strip()
            # Validate rule and apply it to the proof step...
            rule_check_result, message = ruleChecker(proof_step_input, rule_applied, self.proof_steps)

            while not rule_check_result:
                print(f"Rule application error: {message}")
                rule_applied = input("RuleApplied: ").strip()
                rule_check_result, message = ruleChecker(proof_step_input, rule_applied, self.proof_steps)

            self.proof_steps[line_number] = {
                'line_dep': line_dep,
                'step': proof_step_input,
                'rule': rule_applied
            }
            
            self.hints_provider = Hints(self.premises, self.conclusion[0])
            while True:  # Inner loop for handling hints and other commands
                check_or_continue = input("\nPress 'Enter' to add another step, 'Check' to verify the proof, 'Reset' to restart your proof, 'LH' for a next step hint, or 'HH' for a high-level hint: ").strip().lower()
                
                
                if check_or_continue == 'lh':
                    self.hint_count['LH'] += 1  # Increment LH count
                    print("Low-Level Hint:", self.hints_provider.get_low_level_hint())  
                elif check_or_continue == 'hh':
                    self.hint_count['HH'] += 1  # Increment HH count
                    print("High-Level Hint:", self.hints_provider.get_high_level_hint())
                elif check_or_continue == 'check':
                    if self.check_proof_completion():
                        print("Proof is complete and correct!")
                        return  # Exit the method after evaluating and displaying proof steps
                    else:
                        print("The proof is not yet complete. Continue adding proof steps or check again.")
                        continue  
                elif check_or_continue == 'reset':
                    print("Resetting your proof. Keeping premises only.")
                    # Reset logic here...
                    self.proof_steps = {ln: self.proof_steps[ln] for ln in range(1, initial_premises_count + 1)}
                    line_number = len(self.premises) + 1  # Reset line number to start after premises
                    break  # Break out of the inner loop to continue with proof steps
                elif check_or_continue == '':
                    break  # Break out of the inner loop to add another step

        # Additional logic here if needed after exiting the loop


    def check_proof_completion(self):
        try:
            # Retrieve the last proof step
            last_proof_step = self.proof_steps[max(self.proof_steps.keys())]['step']
            # Convert the conclusion to a Sympy expression for comparison
            conclusion_sympy = self.conclusion[0]

            # Compare the last proof step with the conclusion
            if (last_proof_step)==(conclusion_sympy):
                print("The proof successfully concludes with the given conclusion. Well done!")
                return True
            else:
                print("The proof does not conclude with the given conclusion. Please review your steps.")
                return False
        except (ValueError, KeyError) as e:
            print(f"Error checking proof: {e}")
            return False


    def evaluate_user_input(self):
        print("Evaluating your input:")
        for line_number, details in self.proof_steps.items():
            formatted_step = f"Premise/LineDep: {details['line_dep']}  LineNumber: ({line_number})  ProofStep: {details['step']} RuleApplied: {details['rule']}"
            print(formatted_step)



   
    def start_tutor(self):
        print("\nWelcome to the Logic and Proof Tutor CLI!")
        print("Propositional connectives = ∧ , ∨ , ¬ , → ")
        print("Variables allowed: p , q , a")
        print("Rules Applied: ∧I, ∧E, ∨I, ∨E, →I, →E, ¬I, ¬E\n")
        self.get_user_proposition()
        self.get_user_conclusion()
        while self.premises:
            self.display_problem()
            self.initialize_proof_with_premises()
            self.get_user_input()
            self.evaluate_user_input()
            print(f"\nNumber of Low-Level Hints (LH): {self.hint_count['LH']}")
            print(f"Number of High-Level Hints (HH): {self.hint_count['HH']}")
            return
        
        print("Congratulations! You have completed all premises in the tutor.")

if __name__ == "__main__":
    tutor = LogicProofTutor()
    tutor.start_tutor()
