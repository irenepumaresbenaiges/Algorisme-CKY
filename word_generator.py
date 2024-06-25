import random

class GenerateWord:

    def __init__(self, grammar, probabilistic=False):
        """
        Inicialitza la classe.

        Paràmetres:
            grammar (list): Una llista de tuples on cada tupla és una regla (amb o sense probabilitat).
                            Cada regla és de la forma (No terminal, [Body de la regla]) o ((No terminal, [Body de la regla]), probabilitat).
            probabilistic (bool): Indica si la gramàtica és probabilística o no (per defecte és False).
        """
        self.grammar = grammar                  # Assigna la gramàtica proporcionada a l'atribut de la classe
        self.probabilistic = probabilistic      # Assigna el valor de 'probabilistic' a l'atribut de la classe per saber si la gramàtica és probabilística o no


    def generate_word(self, valid=True):
        """
        Genera una paraula a partir de la gramàtica, pot ser vàlida (pertany a la gramàtica) o invàlida (no pertany a la gramàtica).

        Paràmetres:
            valid (bool): Indica si la paraula generada pertany o no a la gramàtica (per defecte és True).

        Retorna:
            str: Una paraula generada segons la gramàtica.
        """
        start_symbol = 'ST'
        if valid:
            return self.generate_valid_word(start_symbol)    # Genera una paraula que pertany a la gramàtica.
        else:
            return self.generate_invalid_word(start_symbol)         # Genera una paraula que no pertany a la gramàtica.


    def generate_valid_word(self, symbol):
        """
        Genera una paraula vàlida a partir d'un símbol de la gramàtica utilitzant les regles.

        Paràmetres:
            symbol (str): El símbol a partir del qual es genera la paraula (start_symbol)

        Retorna:
            str: Una paraula generada segons la gramàtica.
        """
        if self.probabilistic:                                                                  # Amb probabilitats:
            rules = [(rule, prob) for rule, prob in self.grammar if rule[0] == symbol]          # Selecciona les regles que tenen el símbol donat com a head
            selected_rule, _ = random.choices(rules, weights=[prob for _, prob in rules])[0]    # Tria una regla aleatòria de la llista anterior segons les probabilitats
            while selected_rule[1] == ['']:                                                     # Si la regla seleccionada és la paraula buida, escull una altre
                selected_rule, _ = random.choices(rules, weights=[prob for _, prob in rules])[0]

        else:                                                                                   # Sense probabilitats:
            rules = [rule for rule in self.grammar if rule[0] == symbol]                        # Selecciona les regles que tenen el símbol donat com a head
            selected_rule = random.choice(rules)                                                # Tria una regla aleatòria de la llista anterior
            while selected_rule[1] == ['']:                                                     # Si la regla seleccionada és la paraula buida, escull una altre
                selected_rule = random.choice(rules)

        _, expansion = selected_rule                                # Obté el body de la regla seleccionada
        word = ''                                                   # Inicialitza la paraula com a buida
        for sym in expansion:                                       # Recorre els símbols del body
            if sym.islower():                                       # Si el símbol és un terminal (lletra minúscula), l'afegeix directament a la paraula
                word += sym
            else:                                                   # Si el símbol és un no terminal, genera recursivament la part corresponent de la paraula
                word += self.generate_valid_word(sym)
        return word                                                 # Retorna la paraula generada


    def generate_invalid_word(self, start_symbol):
        """
        Genera una paraula invàlida alterant una paraula vàlida generada a partir del símbol inicial.

        Paràmetres:
            start_symbol (str): El símbol inicial a partir del qual es genera la paraula.

        Retorna:
            str: Una paraula que no es pot generar segons la gramàtica.
        """
        valid_word = self.generate_valid_word(start_symbol)          # Genera una paraula vàlida.
        invalid_word = list(valid_word)                                 # Converteix la paraula vàlida en una llista de caràcters per poder-la modificar
        pos = random.randint(0, len(invalid_word) - 1)                  # Selecciona una posició aleatòria de la paraula
        invalid_char = chr(random.randint(97, 122))                     # Genera un caràcter aleatori (lletra minúscula)
        while invalid_word[pos] == invalid_char:                        # Assegura que el nou caràcter sigui diferent del caràcter original en la posició seleccionada
            invalid_char = chr(random.randint(97, 122))
        invalid_word[pos] = invalid_char                                # Substitueix el caràcter original pel nou caràcter
        return ''.join(invalid_word)                                    # Converteix la llista de caràcters en una cadena i la retorna com la paraula invàlida