import re
import itertools

class Sentence:
    def evaluate(self, model):
        raise NotImplementedError
    
    def formula(self):
        return ""
    
    def symbols(self):
        return set()
    
    @classmethod
    def validate(cls, sentence):
        if not isinstance(sentence, Sentence):
            raise TypeError("must be a logical sentence")
        
    @classmethod
    def parenthesize(cls, s):
        p = re.compile(r"\s*([()])\s*")
        return p.sub(r" \1 ", s).strip()
    
class Symbol(Sentence):
    def __init__(self, name):
        self.name = name
        self.true = 0
        self.false = 0
    
    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name
    
    def __hash__(self):
        return hash(("symbol", self.name))
    
    def __repr__(self):
        return self.name
    
    def evaluate(self, model):
        try:
            return bool(model[self.name])
        except KeyError:
            raise Exception(f"variable {self.name} not in model")
    
    def formula(self):
        return self.name
    
    def symbols(self):
        return {self.name}
    
class Not(Sentence):
    def __init__(self, operand):
        Sentence.validate(operand)
        self.operand = operand
    
    def __eq__(self, other):
        return isinstance(other, Not) and self.operand == other.operand
    
    def __hash__(self):
        return hash(("not", hash(self.operand)))
    
    def __repr__(self):
        return f"(not {self.operand})"
    
    def evaluate(self, model):
        return not self.operand.evaluate(model)
    
    def formula(self):
        return "¬" + Sentence.parenthesize(self.operand.formula())
    
    def symbols(self):
        return self.operand.symbols() 
    
class And(Sentence):
    def __init__(self, *conjuncts):
        for conjunct in conjuncts:
            Sentence.validate(conjunct)
        self.conjuncts = list(conjuncts)
    
    def __eq__(self, other):
        return isinstance(other, And) and self.conjuncts == other.conjuncts
    
    def __hash__(self):
        return hash(("and", tuple(hash(conjunct) for conjunct in self.conjuncts)))
    
    def __repr__(self):
        conjunctions = ", ".join(str(conjunct) for conjunct in self.conjuncts)
        return f"(and {conjunctions})"
    
    def evaluate(self, model):
        return all(conjunct.evaluate(model) for conjunct in self.conjuncts)
    
    def formula(self):
        conjunctions = "(" + " ∧ ".join(Sentence.parenthesize(conjunct.formula()) for conjunct in self.conjuncts) + ")"
        return Sentence.parenthesize(conjunctions)
    
    def symbols(self):
        return set().union(*(conjunct.symbols() for conjunct in self.conjuncts))
    
class Or(Sentence):
    def __init__(self, *disjuncts):
        for disjunct in disjuncts:
            Sentence.validate(disjunct)
        self.disjuncts = list(disjuncts)
    
    def __eq__(self, other):
        return isinstance(other, Or) and self.disjuncts == other.disjuncts
    
    def __hash__(self):
        return hash(("or", tuple(hash(disjunct) for disjunct in self.disjuncts)))
    
    def __repr__(self):
        disjunctions = ", ".join(str(disjunct) for disjunct in self.disjuncts)
        return f"(or {disjunctions})"
    
    def evaluate(self, model):
        return any(disjunct.evaluate(model) for disjunct in self.disjuncts)
    
    def formula(self):
        disjunctions = "(" + " ∨ ".join(Sentence.parenthesize(disjunct.formula()) for disjunct in self.disjuncts) + ")"
        return Sentence.parenthesize(disjunctions)
    
    def symbols(self):
        return set().union(*(disjunct.symbols() for disjunct in self.disjuncts))
    
class Implication(Sentence):
    def __init__(self, antecedent, consequent):
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent
    
    def __eq__(self, other):
        return isinstance(other, Implication) and self.antecedent == other.antecedent and self.consequent == other.consequent
    
    def __hash__(self):
        return hash(("implies", hash(self.antecedent), hash(self.consequent)))
    
    def __repr__(self):
        return f"(if {self.antecedent} then {self.consequent})"
    
    def evaluate(self, model):
        return not self.antecedent.evaluate(model) or self.consequent.evaluate(model)
    
    def formula(self):
        antecedent = Sentence.parenthesize(self.antecedent.formula())
        consequent = Sentence.parenthesize(self.consequent.formula())
        return f"{antecedent} => {consequent}"
    
    def symbols(self):
        return self.antecedent.symbols().union(self.consequent.symbols())
    
class Biconditional(Sentence):
    def __init__(self, left, right):
        Sentence.validate(left)
        Sentence.validate(right)
        self.left = left
        self.right = right
    
    def __eq__(self, other):
        return isinstance(other, Biconditional) and self.left == other.left and self.right == other.right
    
    def __hash__(self):
        return hash(("biconditional", hash(self.left), hash(self.right)))
    
    def __repr__(self):
        return f"(iff {self.left} then {self.right})"
    
    def evaluate(self, model):
        return self.left.evaluate(model) == self.right.evaluate(model)
    
    def formula(self):
        left = Sentence.parenthesize(self.left.formula())
        right = Sentence.parenthesize(self.right.formula())
        return f"{left} <=> {right}"
    
    def symbols(self):
        return self.left.symbols().union(self.right.symbols())
    
def model_check(knowledge, query):
    def check_all(knowledge, query, symbols, model):
        if not symbols:
            if knowledge.evaluate(model):
                if query.evaluate(model):
                    query.true += 1
                else:
                    query.false += 1
                return query.evaluate(model)
            return True
        
        remaining = symbols.copy()
        p = remaining.pop()
        return (check_all(knowledge, query, remaining, {**model, **{p: True}}) and
                check_all(knowledge, query, remaining, {**model, **{p: False}}))
    
    symbols = knowledge.symbols().union(query.symbols())

    return check_all(knowledge, query, symbols, model={})