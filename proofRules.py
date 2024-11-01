class ProofRules:
    def __init__(self,proof_steps):
        self.proof_steps = proof_steps  # Store the current proof steps
    
    def check_rule_syntax(self, rule_applied):
         # Allow "None" as a valid input for rule_applied, indicating no rule is applied
        if rule_applied.strip().lower() == "none":
            return True, "No rule applied."
        
        # Split the rule_applied string into the numeric part and the rule abbreviation
        parts = rule_applied.split(" ")
        if len(parts) != 2:
            return False, "Incorrect format. Expected format: '1,2 ∧I or None'"

        line_refs, rule = parts
        # Check if line references are valid (either a single number or multiple numbers separated by commas)
        if not all(ref.isdigit() for ref in line_refs.split(",")):
            return False, "Line references must be numbers separated by commas."

        # Check if the rule abbreviation is valid (you might want to expand this check based on your available rules)
        valid_rules = {"∧I", "∧E", "∨I", "∨E", "→I", "→E", "¬I", "¬E"}  # Add all your rule abbreviations here
        if rule not in valid_rules:
            return False, f"Invalid rule. Expected one of {', '.join(valid_rules)}"

        # If everything checks out, return True
        return True, "Rule syntax is valid."
    
    
    def and_introduction(self, proof_step, rule_applied):
        # Split the rule_applied string to get line references and the rule abbreviation
        try:
            line_refs_str, rule = rule_applied.split(" ")
            if rule != "∧I":
                return False, "The rule applied is not and introduction (∧I)."
        except ValueError:
            return False, "Rule applied format is incorrect. Expected format: '1,2 ∧I'."

        # Convert line references from string to list of integers
        try:
            line_refs = [int(ref) for ref in line_refs_str.split(",")] 
            if len(line_refs) != 2:
                return False, "And introduction (∧I) requires exactly two line reference."
        except ValueError:
            return False, "Line references must be integers."

        # Retrieve the propositions from the referenced lines
        try:
            line_props = [self.proof_steps[line_ref]['step'] for line_ref in line_refs]
        except KeyError as e:
            return False, f"Referenced line number {e.args[0]} does not exist in proof steps."
        
        # Construct the expected proof step based on the ∧I rule
        expected_proof_step = [
        f"({line_props[0]}) ∧ ({line_props[1]})", f"{line_props[0]} ∧ {line_props[1]}", f"({line_props[0]}) ∧ {line_props[1]}", f"{line_props[0]} ∧ ({line_props[1]})", f"({line_props[1]}) ∧ ({line_props[0]})",f"{line_props[1]} ∧ {line_props[0]}", f"({line_props[1]}) ∧ {line_props[0]}", f"{line_props[1]} ∧ ({line_props[0]})"   
        ]
        
        # Check if the constructed proof step matches the user's proof step
        if proof_step in expected_proof_step:
            return True, "∧I rule applied correctly."
        else:
            return False, f"∧I rule not applied correctly."


    def and_elimination(self, proof_step, rule_applied):
        # Split the rule_applied string to get the line reference and the rule abbreviation
        try:
            line_ref_str, rule = rule_applied.split(" ")
            if rule != "∧E":
                return False, "The rule applied is not and elimination (∧E)."
        except ValueError:
            return False, "Rule applied format is incorrect. Expected format: '1 ∧E'."

        # Convert line reference from string to integer
        try:
            line_ref = int(line_ref_str)
        except ValueError:
            return False, "Line reference must be an integer."
        
        # Retrieve the proposition from the referenced line
        try:
            line_prop = self.proof_steps[line_ref]['step']
        except KeyError as e:
            return False, f"Referenced line number {e.args[0]} does not exist in proof steps."
        
        # Remove brackets for comparison, if present
        line_prop = line_prop.strip("()")

        # Check if the referenced line's proposition is a conjunction
        if '∧' not in line_prop:
            return False, "The referenced line's proposition is not a conjunction."

        # Split the conjunction to get the individual propositions
        conjuncts = line_prop.split('∧')
        # Trim whitespace around the conjuncts
        conjuncts = [conjunct.strip() for conjunct in conjuncts]

        # Check if the proof step matches either of the conjuncts
        if proof_step.strip() in conjuncts:
            return True, "∧E rule applied correctly."
        else:
            return False, "∧E rule not applied correctly. The proof step must match one of the conjuncts in the referenced line's proposition."


    def or_introduction(self, proof_step, rule_applied):
        # Split the rule_applied string to get line references and the rule abbreviation
        try:
            line_refs_str, rule = rule_applied.split(" ")
            if rule != "∨I":
                return False, "The rule applied is not or introduction (∨I)."
        except ValueError:
            return False, "Rule applied format is incorrect. Expected format: '1 ∨I'."

        # Convert line references from string to list of integers
        try:
            line_refs = [int(ref) for ref in line_refs_str.split(",")]
            if len(line_refs) != 1:
                return False, "Or introduction (∨I) requires exactly one line reference."
        except ValueError:
            return False, "Line references must be integers."

        # Retrieve the proposition from the referenced line
        try:
            line_prop = self.proof_steps[line_refs[0]]['step']
        except KeyError as e:
            return False, f"Referenced line number {e.args[0]} does not exist in proof steps."
        
        # Remove outer brackets from proof_step for comparison, if present
        proof_step_normalized = proof_step.strip("()")

       # Check if the proof_step is in the form "line_prop ∨ something" or "something ∨ line_prop"
        if proof_step_normalized.startswith(line_prop + " ∨") or proof_step_normalized.endswith("∨ " + line_prop):
            return True, "∨I rule applied correctly."
        else:
            return False, "∨I rule not applied correctly. The proof step must include the proposition from the referenced line followed by '∨' and any other proposition."

    def or_elimination(self, proof_step, rule_applied):
        # Split the rule_applied string to get the line references and the rule abbreviation
        try:
            line_refs_str, rule = rule_applied.split(" ")
            if rule != "∨E":
                return False, "The rule applied is not or elimination (∨E)."
            disjunction_ref, assumption1_ref, conclusion1_ref, assumption2_ref, conclusion2_ref = map(int, line_refs_str.split(","))
        except ValueError:
            return False, "Rule applied format is incorrect. Expected format: '1,2,5,6,11 ∨E'."

        # Retrieve and check the disjunction
        try:
            disjunction = self.proof_steps[disjunction_ref]['step']
        except KeyError:
            return False, f"Referenced disjunction line number {disjunction_ref} does not exist in proof steps."
        if '∨' not in disjunction:
            return False, "The referenced line's proposition is not a disjunction."

        # Check the assumptions
        try:
            assumption1 = self.proof_steps[assumption1_ref]['step']
            assumption2 = self.proof_steps[assumption2_ref]['step']
        except KeyError as e:
            return False, f"Referenced assumption line number {e.args[0]} does not exist in proof steps."

        # Retrieve and check the conclusions derived from the assumptions
        try:
            conclusion1 = self.proof_steps[conclusion1_ref]['step']
            conclusion2 = self.proof_steps[conclusion2_ref]['step']
        except KeyError as e:
            return False, f"Referenced conclusion line number {e.args[0]} does not exist in proof steps."

        # Check if the conclusions match the proof step
        if conclusion1 != proof_step or conclusion2 != proof_step:
            return False, "The conclusions derived from the assumptions do not match the proof step."

        # Check if the disjunction matches the assumptions
        if assumption1 not in disjunction or assumption2 not in disjunction:
            return False, "The assumptions do not match the disjunction."

        return True, "∨E rule applied correctly."


    def implies_introduction(self, proof_step, rule_applied):
        try:
            # Split the rule_applied string to get line references and the rule abbreviation
            line_refs_str, rule = rule_applied.split(" ")
            if rule != "→I":
                return False, "The rule applied is not implies introduction (→I)."
        except ValueError:
            return False, "Rule applied format is incorrect. Expected format: '3,5 →I'."

        # Attempt to extract start and end lines of the subproof
        try:
            start_line, end_line = [int(ref) for ref in line_refs_str.split(",")]
        except ValueError:
            return False, "Line references for →I must specify the start and end lines of the subproof, e.g., '3,5'."

        # Validate that start_line is before end_line
        if start_line >= end_line:
            return False, "In the rule application, the start line must precede the end line."
        
            # Check if the start line is marked as a temporary assumption
        try:
            if 'Premise' not in self.proof_steps[start_line]['line_dep']:
                return False, "The start line is not marked as a assumption."
        except KeyError:
            return False, f"Referenced start line number {start_line} does not exist in proof steps."

        # Check if the end_line's proof step matches the desired conclusion B
        try:
            conclusion = self.proof_steps[end_line]['step']
        except KeyError:
            return False, f"Referenced end line number {end_line} does not exist in proof steps."

        # Assuming the start line contains the temporary assumption A
        try:
            assumption = self.proof_steps[start_line]['step']
        except KeyError:
            return False, f"Referenced start line number {start_line} does not exist in proof steps."

        # Construct the expected proof step based on the →I rule
        expected_proof_step = f"{assumption} → {conclusion}"
        
        # Check if the constructed proof step matches the user's proof step
        if proof_step == expected_proof_step:
            return True, "→I rule applied correctly."
        else:
            return False, f"→I rule not applied correctly."



    def implies_elimination(self, proof_step, rule_applied):
        # Split the rule_applied string to get the line references and the rule abbreviation (Modus Ponens)
        try:
            line_refs_str, rule = rule_applied.split(" ")
            if rule != "→E":
                return False, "The rule applied is not implies elimination (→E)."
            line_refs = list(map(int, line_refs_str.split(",")))
            if len(line_refs) != 2:
                return False, "Expected two line references for →E rule."
        except ValueError:
            return False, "Rule applied format is incorrect. Expected format: '1,2 →E', where 1 is the line with A → B and 2 is the line with A, or vice versa."

        # Retrieve propositions from the referenced lines
        try:
            proposition1 = self.proof_steps[line_refs[0]]['step']
            proposition2 = self.proof_steps[line_refs[1]]['step']
        except KeyError as e:
            return False, f"Referenced line number {e.args[0]} does not exist in proof steps."

        # Determine which proposition is the implication and which is the antecedent
        if '→' in proposition1:
            implication, antecedent = proposition1, proposition2
        elif '→' in proposition2:
            implication, antecedent = proposition2, proposition1
        else:
            return False, "Neither of the referenced lines contains an implication."

        # Split the implication to get A and B
        parts = implication.split('→')
        if len(parts) != 2:
            return False, "Invalid implication format."
        antecedent_part, consequent_part = parts

        # Check if the antecedent from the proof matches A from the implication
        if antecedent.strip() != antecedent_part.strip():
            return False, "The antecedent from the proof does not match the antecedent in the implication."

        # Check if the conclusion B is the proof step
        if consequent_part.strip() != proof_step.strip():
            return False, "The proof step does not match the consequent of the implication." 

        return True, "→E rule applied correctly."

    
    def is_contradiction(self, start_line, end_line):
        try:
            # Retrieve the propositions from the specified lines
            start_proposition = self.proof_steps[start_line]['step']
            end_proposition = self.proof_steps[end_line]['step']

            # Check for direct contradiction between start and end lines
            if start_proposition == f"¬{end_proposition}" or end_proposition == f"¬{start_proposition}":
                return True  # Direct contradiction found

            # Check for inherent contradiction within the end_line proposition (e.g., "P ∧ ¬P")
            # This simple check splits the end proposition by '∧' and looks for complementary pairs (P and ¬P)
            if "∧" in end_proposition:
                parts = [part.strip() for part in end_proposition.split("∧")]
                for part in parts:
                    # Check if the negation of this part is also present in the parts list
                    if (f"¬{part}" in parts) or (part.startswith("¬") and part[1:] in parts):
                        return True  # Inherent contradiction found within the end_line proposition

            return False  # No contradiction found
        except KeyError as e:
            # Handle cases where the specified line numbers do not exist in proof_steps
            print(f"Line number {e.args[0]} does not exist in proof steps.")
            return False



    def not_introduction(self, proof_step, rule_applied):
        # Split the rule_applied string to get line references and the rule abbreviation
        try:
            line_refs_str, rule = rule_applied.split(" ")
            if rule != "¬I":
                return False, "The rule applied is not not introduction (¬I)."
        except ValueError:
            return False, "Rule applied format is incorrect. Expected format: '1,4 ¬I'."

        # Extract start and end lines of the subproof where A leads to a contradiction
        try:
            start_line, end_line = [int(ref) for ref in line_refs_str.split(",")]
        except ValueError:
            return False, "Line references for ¬I must specify the start and end lines of the subproof, e.g., '1,4'."

        # Ensure the start line is before the end line
        if start_line >= end_line:
            return False, "In the rule application, the start line must precede the end line."

        # Verify the assumption at the start line (A)
        try:
            assumption = self.proof_steps[start_line]['step']
        except KeyError:
            return False, f"Referenced start line number {start_line} does not exist in proof steps."

         # Check for a contradiction between the start line and the end line, or within the end line itself
        if not self.is_contradiction(start_line, end_line):
            return False, "The proof does not demonstrate a contradiction between the assumption and derived statement, or within the derived statement itself."

        # Check if the proof step is the negation of the assumption at the start line
        try:
            assumption = self.proof_steps[start_line]['step']
            expected_proof_step = f"¬({assumption})" or f"¬{assumption}"
            if proof_step != expected_proof_step:
                return False, f"¬I rule not applied correctly. Expected step: {expected_proof_step}"
        except KeyError:
            return False, f"Referenced line number {start_line} does not exist in proof steps."

        return True, "¬I rule applied correctly."
    

    def not_elimination(self, proof_step, rule_applied):
        # Split the rule_applied string to get the line reference and the rule abbreviation
        try:
            line_ref_str, rule = rule_applied.split(" ")
            if rule != "¬E":
                return False, "The rule applied is not negation elimination (¬E)."
            negation_line_ref = int(line_ref_str)
        except ValueError:
            return False, "Rule applied format is incorrect. Expected format: '1 ¬E', where 1 is the line with ¬¬A or ¬(¬A)."

        # Retrieve and check the negation or potential double negation
        try:
            negation = self.proof_steps[negation_line_ref]['step']
        except KeyError:
            return False, f"Referenced negation line number {negation_line_ref} does not exist in proof steps."

        # Check for double negation ¬¬A and simplify to A
        if negation.startswith("¬¬"):
            simplified = negation[2:]  # Remove the first two characters '¬¬' to get A
        elif negation.startswith("¬(¬"):
            if negation.endswith(")"):
                simplified = negation[3:-1]  # Remove '¬(¬' from the start and ')' from the end to get A
            else:
                return False, "The negation format is incorrect. Expected ¬(¬A)."
        else:
            return False, "¬E rule is not applicable or the statement does not involve a negation pattern that can be eliminated."

        # Compare the simplified statement to the proof_step
        if simplified.strip() == proof_step.strip():
            return True, "¬E rule applied correctly for double negation elimination."
        else:
            return False, "The proof step does not match the statement obtained by removing double negation."



    def iff_introduction(self, proof_step):
        # Implement the logic for checking if the iff-introduction (if and only if) rule is correctly applied in proof_step
        pass

    def iff_elimination(self, proof_step):
        # Implement the logic for checking if the iff-elimination (if and only if) rule is correctly applied in proof_step
        pass

    # Add additional methods for any other rules you need to support

def ruleChecker(proof_step, rule_applied, proof_steps):
    # Handle the "None" case early to avoid splitting and accessing a non-existent index
    if rule_applied.strip().lower() == "none":
        # Return True, indicating no rule needs to be checked, or handle it differently as needed.
        return True, "No rule needs to be checked."
    
    rules = ProofRules(proof_steps)  # Pass the current proof steps to the ProofRules instance
    syntax_valid, syntax_message = rules.check_rule_syntax(rule_applied)

    if not syntax_valid:
        return False, syntax_message

    # Safely extract the rule abbreviation from the rule_applied string
    parts = rule_applied.split(" ")
    if len(parts) > 1:
        rule = parts[1]  # Extract the rule abbreviation
    else:
        return False, "Rule abbreviation is missing."

    # Call the appropriate method based on the rule abbreviation
    if rule == "∧I":
        return rules.and_introduction(proof_step, rule_applied)
    elif rule == "∨I":
        return rules.or_introduction(proof_step,rule_applied)
    elif rule == "→I":
        return rules.implies_introduction(proof_step,rule_applied)
    elif rule == "¬I":
        return rules.not_introduction(proof_step,rule_applied)
    elif rule == "∧E":
        return rules.and_elimination(proof_step,rule_applied)
    elif rule == "∨E":
        return rules.or_elimination(proof_step,rule_applied)
    elif rule == "→E":
        return rules.implies_elimination(proof_step,rule_applied)
    elif rule == "¬E":
        return rules.not_elimination(proof_step,rule_applied)
    
    # If the rule abbreviation doesn't match any known rule, return an error message
    return False, "Unknown rule."
