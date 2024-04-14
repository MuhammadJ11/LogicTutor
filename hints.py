class Hints:
    def __init__(self, premises, conclusion):
        self.premises = premises
        self.conclusion = conclusion
        self.hint_counters = {'∧': 0, '∨': 0, '¬': 0, '→': 0, 'current': 0, 'low_level': 0, 'high_level': 0}  # Counter for each connective type
        self.connectives_found = self.identify_connectives_in_conclusion()

   
    def identify_connectives_in_conclusion(self):
        # Identify and return the list of unique connectives found in the conclusion
        return [char for char in self.conclusion if char in self.hint_counters]

    def get_low_level_hint(self):
        if not self.connectives_found:  # If no connectives are found, return a default hint
            return "Consider the relationships between your premises and conclusion."

        # Cycle through the connectives found in the conclusion, providing a hint for each
        current_hint_index = self.hint_counters['current'] % len(self.connectives_found)
        connective_for_hint = self.connectives_found[current_hint_index]

        # Update the counter for the next call
        self.hint_counters['current'] += 1
        # Increment the low-level hint counter
        self.hint_counters['low_level'] += 1

        # Dispatch to the appropriate hint method based on the connective
        return self.get_hint_for_connective(connective_for_hint)

    def get_hint_for_connective(self, connective):
        if connective == '∧':
            return self.get_conjunction_hint()
        elif connective == '∨':
            return self.get_disjunction_hint()
        elif connective == '¬':
            return self.get_negation_hint()
        elif connective == '→':
            return self.get_material_conditional_hint()
        # Implement additional clauses for other connectives...
        else:
            return "No specific hint available for this connective."


    def get_conjunction_hint(self):
        # Cycle through conjunction hints based on the current state
        hints = [
            " Your conclusion is a conjunction. Have you thought about how you might prove each part?",
            " Can you identify premises or previous steps that directly support parts of your conjunction?",
            " Have you considered how you might combine proven propositions to construct your conjunction?",
            " Your goal or premises involve a conjunction. Have you considered using Conjunction Introduction (∧I)?",
            " Check if you've proven both parts of your conjunction independently before combining them.",
            " If your proof involves a conjunction, remember you can use Conjunction Elimination (∧E) to extract individual parts. "
        ]

        # Retrieve the hint based on the current counter value
        hint = hints[self.hint_counters['∧'] % len(hints)]

        # Increment the hint counter for conjunctions after retrieving the hint
        self.hint_counters['∧'] += 1

        return hint

    
    def get_disjunction_hint(self):
        # Cycle through conjunction hints based on the current state
        hints = [
            "A disjunction suggests multiple paths. Can you prove one part to reach your conclusion?",
            "Think about weaker conditions or premises that might lead to one part of your disjunction.",
            "Is there a way to transform one of your premises into a part of the disjunction?",
            "Look for instances where introducing a disjunction could simplify your proof or connect your premises to your conclusion more directly. Remember, proving just one part of a disjunction is sufficient to introduce it."
        ]

        # Retrieve the hint based on the current counter value
        hint = hints[self.hint_counters['∨'] % len(hints)]

        # Increment the hint counter for conjunctions after retrieving the hint
        self.hint_counters['∨'] += 1

        return hint
    
    def get_negation_hint(self):
        # Cycle through conjunction hints based on the current state
        hints = [
            "Seeing a negation, have you considered what assuming the opposite implies?",
            "Could proving a contradiction from your premises or assumed conditions help?",
            "What happens if you take the negated statement as a temporary assumption?",
            "If your goal involves a negation, consider what it would mean for the negated proposition to be false. This might offer a path forward."
        ]

        # Retrieve the hint based on the current counter value
        hint = hints[self.hint_counters['¬'] % len(hints)]

        # Increment the hint counter for conjunctions after retrieving the hint
        self.hint_counters['¬'] += 1

        return hint
    
    def get_material_conditional_hint(self):
        # Cycle through conjunction hints based on the current state
        hints = [
            "An implication suggests a conditional approach. What might assuming the antecedent allow you to derive?",
            "Can you derive the consequent from your premises or a new assumption?",
            "Think about cases where the antecedent is true. How does that affect the consequent?",
            "For a material conditional 'P → Q', consider proving 'Q' assuming 'P'."
        ]

        # Retrieve the hint based on the current counter value
        hint = hints[self.hint_counters['→'] % len(hints)]

        # Increment the hint counter for conjunctions after retrieving the hint
        self.hint_counters['→'] += 1

        return hint
        
    
    def get_high_level_hint(self):
        if not self.connectives_found:  # If no connectives are found, return a default hint
            return "Reflect on the overall structure of your argument. How do your premises logically lead to your conclusion?"

        # Cycle through the connectives found in the conclusion, providing a hint for each
        current_hint_index = self.hint_counters['current'] % len(self.connectives_found)
        connective_for_hint = self.connectives_found[current_hint_index]

        # Update the counter for the next call
        self.hint_counters['current'] += 1
        # Increment the high-level hint counter
        self.hint_counters['high_level'] += 1

        # Dispatch to the appropriate hint method based on the connective
        return self.get_highLevel_hint_for_connective(connective_for_hint)
        # General strategy hint, not specific to any connective
        
    def get_highLevel_hint_for_connective(self, connective):
        if connective == '∧':
            return self.get_high_level_conjunction_hint()
        elif connective == '∨':
            return self.get_high_level_disjunction_hint()
        elif connective == '¬':
            return self.get_high_level_negation_hint()
        elif connective == '→':
            return self.get_high_level_material_conditional_hint()
        # Implement additional clauses for other connectives...
        else:
            return "No specific hint available for this connective."
        
    def get_high_level_conjunction_hint(self):
        hints = [
            "When your conclusion involves a conjunction (' ∧ '), you need to prove multiple statements are true simultaneously.",
            "In essence, your goal is not just one, but several - each component of the conjunction",
            "Remember, the beauty of conjunctions is in their flexibility - you don't have to tackle the components in any specific order. Choose the order that makes the most sense based on your premises and what seems most straightforward to prove.",
            "Once all components are established, use Conjunction Introduction ( ∧I ) to combine them into your desired conclusion.This strategy not only structures your proof but also ensures you cover all necessary grounds to solidify your argument."
        ]

        # Cycle through the hints
        current_hint_index = self.hint_counters['∧'] % len(hints)
        hint = hints[current_hint_index]

        # Update the hint counter for material conditionals
        self.hint_counters['∧'] += 1

        return hint

    def get_high_level_disjunction_hint(self):
        hints = [
            "When your conclusion involves a disjunction (' ∨ ') it means that your argument can take different paths to reach a valid conclusion.",
            "You don't need to prove each component proving just one is sufficient. This flexibility allows you to examine your premises and see if any of them directly support either component of the disjunction.",
            "Once you've successfully proven one part of the disjunction, you can introduce the disjunction into your proof using Disjunction Introduction ( ∨I ). This doesn't mean you've proven both parts, but rather that you've shown at least one part is true, which is all that's required for the disjunction to hold."
        ]

        # Cycle through the hints
        current_hint_index = self.hint_counters['∨'] % len(hints)
        hint = hints[current_hint_index]

        # Update the hint counter for material conditionals
        self.hint_counters['∨'] += 1

        return hint

       
    def get_high_level_negation_hint(self):
        hints = [
            "Your conclusion involves negating a statement. One effective strategy here is to employ 'reductio ad absurdum', a form of proof by contradiction.",
            "Begin by assuming the opposite is indeed true. Then, meticulously work through the logical implications of this assumption.",
            "Common contradictions might involve arriving at a statement and its direct negation both being true ('P' and '¬P').",
            "The moment you uncover such a contradiction, you've proven that your initial assumption (is true) must be false. Hence, the original statement you wanted to negate stands validated." 
        ]

        # Cycle through the hints
        current_hint_index = self.hint_counters['¬'] % len(hints)
        hint = hints[current_hint_index]

        self.hint_counters['¬'] += 1

        return hint
       

    def get_high_level_material_conditional_hint(self):
        hints = [
            "When dealing with the material conditional consider working backward from what you want to prove.",
            "Ask yourself: What conditions, if established, could lead to the consequent?",
            "Backward reasoning involves considering the consequent as if it were your new 'goal' and figuring out how the antecedent could be used as a 'stepping stone' toward that goal.",
            "You might find it helpful to temporarily assume the antecedent and explore how it could logically lead to the consequent. This approach can sometimes reveal a more straightforward path or a necessary intermediate step that wasn't initially apparent.",
            "Remember, proving the antecedent under this assumption and then using implication introduction (→I) can solidify the link between antecedent and consequent in your proof."
        ]

        # Cycle through the hints
        current_hint_index = self.hint_counters['→'] % len(hints)
        hint = hints[current_hint_index]

        # Update the hint counter for material conditionals
        self.hint_counters['→'] += 1

        return hint
    


