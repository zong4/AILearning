from logic import Symbol, And, Or, Not, Implication, model_check

rain = Symbol("rain") # It's raining.
hagrid = Symbol("hagrid") # Zong will visit hagrid.
dumbledore = Symbol("dumbledore") # Zong will visit dumbledore.

symbols = [rain, hagrid, dumbledore]

knowledge = And(
    Implication(rain, hagrid), # If it's raining, then Zong will visit Hagrid.
    Or(hagrid, dumbledore), # Zong will visit Hagrid or Zong will visit Dumbledore.
    Not(And(hagrid, dumbledore)), # Zong will not visit both Hagrid and Dumbledore.
    hagrid, # Zong will visit Hagrid.
)

inference = rain

print(knowledge.formula()) # Should be (rain => hagrid) ∧ (hagrid ∨ dumbledore) ∧ ¬(hagrid ∧ dumbledore) ∧ hagrid

for symbol in symbols:
    if model_check(knowledge, symbol):
        print(f"{symbol}: Yes")
    else:
        prosibilities = symbol.true / (symbol.true + symbol.false)
        if prosibilities == 0:
            print(f"{symbol}: No")
        else:
            print(f"{symbol}: {prosibilities * 100:.2f}%")