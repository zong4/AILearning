PROBS = {
    # Unconditional probabilities for having gene
    "gene": {
        0: 0.96,
        1: 0.03,
        2: 0.01,
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}

class Node:
    def __init__(self, name, father=None, mother=None, trait=None):
        self.name = name
        self.father = father
        self.mother = mother
        self.trait = trait

    def get_genes_possibility(self):
        ren = None
        if self.father is None and self.mother is None:
            if self.trait == None:
                ren = PROBS["gene"]
            else:
                genes_0_possibility = PROBS["trait"][0][self.trait] * PROBS["gene"][0]
                genes_1_posibility = PROBS["trait"][1][self.trait] * PROBS["gene"][1]
                genes_2_possibility = PROBS["trait"][2][self.trait] * PROBS["gene"][2]

                ren = {
                    0: genes_0_possibility / (genes_0_possibility + genes_1_posibility + genes_2_possibility),
                    1: genes_1_posibility / (genes_0_possibility + genes_1_posibility + genes_2_possibility),
                    2: genes_2_possibility / (genes_0_possibility + genes_1_posibility + genes_2_possibility),
                }
        else:
            father_genes_possibility = self.father.get_genes_possibility()
            mother_genes_possibility = self.mother.get_genes_possibility()

            genes_2_possibility = father_genes_possibility[2] * (1 - PROBS["mutation"]) * mother_genes_possibility[2] * (1 - PROBS["mutation"])
            genes_2_possibility += father_genes_possibility[1] * 0.5 * mother_genes_possibility[2] * (1 - PROBS["mutation"]) * 2
            genes_2_possibility += father_genes_possibility[1] * 0.5 * mother_genes_possibility[1] * 0.5
            genes_2_possibility += father_genes_possibility[0] * PROBS["mutation"] * mother_genes_possibility[2] * (1 - PROBS["mutation"]) * 2
            genes_2_possibility += father_genes_possibility[0] * PROBS["mutation"] * mother_genes_possibility[1] * 0.5 * 2
            genes_2_possibility += father_genes_possibility[0] * PROBS["mutation"] * mother_genes_possibility[0] * PROBS["mutation"]

            genes_1_possibility = father_genes_possibility[2] * (1 - PROBS["mutation"]) * mother_genes_possibility[2] * PROBS["mutation"] * 2
            genes_1_possibility += father_genes_possibility[1] * 0.5 * mother_genes_possibility[2] * 2
            genes_1_possibility += father_genes_possibility[1] * 0.5 * mother_genes_possibility[1] * 0.5
            genes_1_possibility += father_genes_possibility[0] * mother_genes_possibility[2] * 2
            genes_1_possibility += father_genes_possibility[0] * mother_genes_possibility[1] * 0.5 * 2
            genes_1_possibility += father_genes_possibility[0] * PROBS["mutation"] * mother_genes_possibility[0] * (1 - PROBS["mutation"]) * 2

            genes_0_possibility = father_genes_possibility[2] * PROBS["mutation"] * mother_genes_possibility[2] * PROBS["mutation"]
            genes_0_possibility += father_genes_possibility[1] * 0.5 * mother_genes_possibility[2] * PROBS["mutation"] * 2
            genes_0_possibility += father_genes_possibility[1] * 0.5 * mother_genes_possibility[1] * 0.5
            genes_0_possibility += father_genes_possibility[0] * (1 - PROBS["mutation"]) * mother_genes_possibility[2] * PROBS["mutation"] * 2
            genes_0_possibility += father_genes_possibility[0] * (1 - PROBS["mutation"]) * mother_genes_possibility[1] * 0.5 * 2
            genes_0_possibility += father_genes_possibility[0] * (1 - PROBS["mutation"]) * mother_genes_possibility[0] * (1 - PROBS["mutation"])

            ren = {
                0: genes_0_possibility / (genes_0_possibility + genes_1_possibility + genes_2_possibility),
                1: genes_1_possibility / (genes_0_possibility + genes_1_possibility + genes_2_possibility),
                2: genes_2_possibility / (genes_0_possibility + genes_1_possibility + genes_2_possibility),
            }
    
        print(str(self.name) + " genes possibility: " + str(ren))
        return ren
        
    def get_trait_possibility(self):
        if self.trait != None:
            return PROBS["trait"][self.trait][True]

        genes_possibility = self.get_genes_possibility()
        trait_2_possibility = genes_possibility[2] * PROBS["trait"][2][True]
        trait_1_possibility = genes_possibility[1] * PROBS["trait"][1][True]
        trait_0_possibility = genes_possibility[0] * PROBS["trait"][0][True]

        return trait_2_possibility + trait_1_possibility + trait_0_possibility

# name,mother,father,trait
# Harry,Lily,James,
# James,,,1
# Lily,,,0
james = Node("James", None, None, True)
lily = Node("Lily", None, None, False)
harry = Node("Harry", james, lily, None)

print("Harry trait possibility: " + str(harry.get_trait_possibility()))