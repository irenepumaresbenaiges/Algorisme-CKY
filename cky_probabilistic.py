class ProbabilisticCKY:

    def __init__(self, grammar):
        """
        Inicialitza la classe.

        Paràmetres:
            grammar (list): Una llista de tuples on cada tupla és una regla amb la seva probabilitat.
                            Cada regla és de la forma ((No terminal, [Body de la regla]), probabilitat).
        """
        self.grammar = grammar  # Assigna la gramàtica proporcionada a l'atribut de la classe
        self.probabilities = self.compute_probabilities()  # Calcula les probabilitats de les regles i les assigna a l'atribut de la classe


    def compute_probabilities(self):
        '''
        Calcula la probabilitat de cada regla de la gramàtica

        Retorna:
            dict: Un diccionari amb les regles com a claus i la seva probabilitat com a valors.
        '''
        probabilities = {}                              # Crea un diccionari per emmagatzemar les probabilitats
        for rule, probability in self.grammar:          # Itera per cada regla i probabilitat de la gramàtica
            rule_tuple = (rule[0], tuple(rule[1]))
            if rule_tuple not in probabilities:
                probabilities[rule_tuple] = 0.0
            probabilities[rule_tuple] += probability    # Afegeix la probabilitat a la regla al diccionari
        return probabilities                            # Retorna el diccionari de probabilitats


    def parse(self, word):
        '''
        Comprova si una paraula pertany al llenguatge de la gramàtica.

        Paràmetres:
            word (str): La palabra a analitzar.

        Retorna:
            float: la probabilitat de la paraula si pertany a la gramàtica, False en cas que no hi pertanyi.
        '''
        n = len(word)

        # Inicialitza la taula CKY amb probabilitats
        table = [[{} for _ in range(n + 1)] for _ in range(n)] 

        # Omple la diagonal de la taula amb els símbols terminals i les seves probabilitats
        for i in range(n):
            for rule, prob in self.grammar:
                if len(rule[1]) == 1 and rule[1][0] == word[i]:
                    table[i][i + 1][rule[0]] = prob

        # Omple la resta de la taula
        for l in range(2, n + 1):
            for i in range(n - l + 1):
                j = i + l
                for k in range(i + 1, j):
                    for rule, prob in self.probabilities.items():
                        if len(rule[1]) == 2:
                            A, BC = rule
                            B, C = BC
                            if B in table[i][k] and C in table[k][j]:
                                probability = prob * table[i][k][B] * table[k][j][C]
                                if A not in table[i][j]:
                                    table[i][j][A] = 0.0
                                table[i][j][A] = max(table[i][j][A], probability)

        # Comprova si el símbol inicial té una probabilitat més gran que 0 a la casella (0, n)
        start_symbol, _ = self.grammar[0][0]
        probability = table[0][n].get(start_symbol, 0.0)
        return probability if probability > 0 else False