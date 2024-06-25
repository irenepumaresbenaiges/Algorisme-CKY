class CKY:

    def __init__(self, grammar):
        """
        Inicialitza la classe.

        Paràmetres:
            grammar (list): La gramàtica en forma de llista de tuples on cada tupla és una regla.
                            Cada regla és de la forma (No terminal, [Body de la regla]).
        """
        self.grammar = grammar  # Assigna la gramàtica proporcionada a l'atribut de la classe


    def parse(self, word):
        '''
        Comprova si una paraula pertany al llenguatge de la gramàtica.

        Paràmetres:
            word (str): La palabra a analitzar.

        Retorna:
            bool: True si la palabra es acceptada per la gramàtica, False en cas contrari.
        '''
        n = len(word)         # Longitud de la paraula

        # Inicialitza la taula CKY de mida (n+1) x (n+1)
        table = [[set() for _ in range(n+1)] for _ in range(n)] 
        
        # Omple la diagonal de la taula amb els símbols terminals
        for i in range(n):
            for rule in self.grammar:
                if len(rule[1]) == 1 and rule[1][0] == word[i]:
                    table[i][i+1].add(rule[0])
   
        # Omple la resta de la taula
        for l in range(2, n+1):
            for i in range(n-l+1):
                j = i + l
                for k in range(i+1, j):
                    for rule in self.grammar:
                        if len(rule[1]) == 2:
                            non_terminal, head, body = rule[0], rule[1][0], rule[1][1]
                            if head in table[i][k] and body in table[k][j]:
                                table[i][j].add(non_terminal)
        
        # Comprovar si el símbol inicial es troba a la casella (0, n)
        return self.grammar[0][0] in table[0][n]
    


