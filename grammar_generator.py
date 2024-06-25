import random
from collections import defaultdict

class GenerateGrammar:

    def __init__(self):
        """
        Inicialitza la classe amb un diccionari de gramàtica buit.
        """
        self.grammar_dict = defaultdict(list)   # Diccionari on les claus són no terminals i els valors són llistes de símbols (terminals i no terminals)
        self.all_non_terminal_body = []         # Llista per emmagatzemar tots els símbols no terminals que apareguin en els bodies de les regles

    def generate_epsilon(self):
        """
        Genera l'epsilon (cadena buida) per a les regles de gramàtica.

        Retorna:
            str: Cadena buida.
        """
        return ''

    def generate_nonterminal(self):
        """
        Genera un no terminal aleatori de la forma 'N' seguit d'un número.

        Retorna:
            str: No terminal aleatori.
        """
        return f"N{random.randint(1, 10)}"

    def generate_terminal(self):
        """
        Genera un terminal aleatori (una lletra minúscula).

        Retorna:
            str: Terminal aleatori.
        """
        return chr(random.randint(97, 122))

    def generate_cnf_rules(self):
        """
        Genera una regla en forma normal de Chomsky (CNF).

        Retorna:
            tuple: Un tupla amb el head (no terminal) i el body (llista de 1 terminal/ 2 no terminals).
        """
        head = random.choice(self.all_non_terminal_body)    # Genera un head escollint un no terminal de la llista dels que ja existeixen a la gramàtica
        if random.random() < 0.5:                           # Té 50% de probabilitats de generar un terminal i 50% de probabilitats de generar 2 no terminals en el body
            body = [self.generate_terminal()]               # Genera un terminal com a body
        else:
            nt1 = self.generate_nonterminal()               # Genera dos no terminals com a body, comprovant que els creats no siguin igual que el head ni que hagin generat el head, per evitar bucles
            while nt1 == head or nt1 in self.find_generators(head):
                nt1 = self.generate_nonterminal()
            nt2 = self.generate_nonterminal()
            while nt2 == head or nt2 in self.find_generators(head):
                nt2 = self.generate_nonterminal()
            body = [nt1, nt2]

        return head, body                           # Retorna el head y el body(llista) que forma la regla

    def generate_non_cnf_rules(self):
        """
        Genera una regla que no està en forma normal de Chomsky (CNF).

        Retorna:
            tuple: Un tuple amb el head (no terminal) i el body (llista de terminals/no terminals/epsilon).
        """
        head = random.choice(self.all_non_terminal_body)         # Genera un head escollint un no terminal de la llista dels que ja existeixen a la gramàtica

        body = [random.choice([self.generate_terminal(), self.generate_nonterminal()])
                for _ in range(random.randint(1, 5))]            # Tria una d'aquestes opcions per a cada símbol del body (que serà de llargada aleatòria entre 1 i 5) i genera els símbols

        generators = self.find_generators(head)                  # Es busquen els generadors del head
        body = [elem for elem in body if elem not in generators and elem != head] # S'eliminen els símbols del body que puguin generar cicles (generadors del head) i que siguin iguals que el head

        minuscules = set()                                       # Defineix un conjunt per emmagatzemar les minuscules
        min = [symbol for symbol in body if symbol.islower()]    # Defineix una llista que conté els terminals que apareguin al body
        for terminal in min:                                     # Per cada terminal
            body.remove(terminal)                                # Elimina el terminal del body
            minuscules.add(terminal)                             # Afegeix el terminal al conjunt
        for terminal in minuscules:                              # Recorre el conjunt de minuscules (on no hi haurà repetides)
            body.append(terminal)                                # Afegeix les minúscules altre vegada al body (d'aquesta manera s'assegura que no hi hagi terminals repetits al body d'una regla)

        if not body:                                        # Després de fer totes les eliminacions, oportunes, en cas que no hi hagi body, es genera un terminal o un epsilon pel body
            body = [random.choice([self.generate_terminal(), self.generate_epsilon()])]               

        return head, body
    
    def find_generators(self, nonterminal):
        """
        Troba tots els no terminals que generen el no terminal donat,
        incloent els generadors dels generadors de manera recursiva.

        Paràmetres:
            nonterminal (str): No terminal per trobar els seus generadors.

        Retorna:
            set: Conjunt de no terminals que generen el no terminal donat.
        """
        generators = set()                    # Crea un conjunt per emmagatzemar els generadors del no terminal donat
        to_process = {nonterminal}            # Crea un conjunt inicialitzat amb el no terminal donat i contindrà els no terminals que s'han de processar.

        while to_process:                                                   # Mentres hi hagi no terminals per processar
            current = to_process.pop()                                      # Extreu un nop terminal del conjunt per processar-lo
            for head, rule_bodies in self.grammar_dict.items():             # Recorre el diccionari
                for rule_body in rule_bodies:                               # Recorre els bodies
                    if current in rule_body and head not in generators:     # Comprova si el no terminal que s'està processant coincideix amb algun símbol
                        generators.add(head)                                # Si encara no està al conjunt, l'afegeix
                        to_process.add(head)                                # L'afegeix també a to_process per seguir mirant, ja que sinó no s'eviten tots els bucles 

        return generators


    def generate_random_grammar(self, cnf=True, probabilistic=False):
        """
        Genera una gramàtica aleatòria amb opcions per ser en CNF i probabilística.

        Paràmetres:
            cnf (bool): Si la gramàtica ha de ser en forma normal de Chomsky (CNF) o no.
            probabilistic (bool): Si la gramàtica ha de tenir regles amb o sense probabilitats.

        Retorna:
            list: Llista de tuples representant la gramàtica, opcionalment amb probabilitats.
        """      
        num_rules = random.randint(5, 8)    # S'escull un número aleatori de regles entre 5 i 8

        # Genera la primera regla (s'ha decidit que contingui un epsilon o dos no terminals al body)
        if cnf:
            head = 'ST'                                     # Si es en CNF, el head s'ha d'anomenar 'ST'
        else:
            head = self.generate_nonterminal()              # En cas contrari, crea un no terminal aleatòria com a head
        
        if random.random() < 0.5:                           # Té 50% de probabilitats de generar un epsilon i 50% de probabilitats de generar 2 no terminals en el body
            body = [self.generate_epsilon()]                # Genera un epsilon com a body
        else:
            nt1 = self.generate_nonterminal()               # Crea el símbol del body
            while nt1 == head:                              # Comprova que el símbol no és igual que el head
                nt1 = self.generate_nonterminal()
            nt2 = self.generate_nonterminal()               # Igual pel segon símbol del body
            while nt2 == head:
                nt2 = self.generate_nonterminal()
            body = [nt1, nt2]
            self.all_non_terminal_body.append(nt1)          # Afegeix el primer no terminal del body a la llista de no terminals
            if nt1 != nt2:
                self.all_non_terminal_body.append(nt2)      # Afegeix el segon no terminal del body (si és igual que el primer, no s'afegirà)

        self.grammar_dict[head].append(body)                # Afegeix la regla al diccionari
        self.all_non_terminal_body.append(head)             # Afegeix el head a la llista de no terminals
    

        while len(self.grammar_dict) < num_rules:               # S'afegiran regles a la gramàtica fins que s'arribi el nombre de regles escollit aleatòriament (a més de les que s'afegeixen a posteriori)
            if cnf:                                             # Comprova si s'ha triat CNF
                head, body = self.generate_cnf_rules()          # Genera un regla en CNF
            else:                                               # En cas que no s'hagi triat CNF
                head, body = self.generate_non_cnf_rules()      # Genera un regla que no està en CNF
            
            self.grammar_dict[head].append(body)                # S'afegeix la regla al diccionari

            for symbol in body:                                 # Per cada símbol del body afegit
                if not symbol.islower() and symbol != '' and symbol:     # Comprova que el símbol sigui un no terminal i no estigui ja a la llista
                    self.all_non_terminal_body.append(symbol)   # Afegeix el símbol a la llista de no terminals
                
        for non_terminal in self.all_non_terminal_body:         # Un cop ha creat totes les regles recorre la llista de no terminals
            if non_terminal not in self.grammar_dict.keys():    # En cas que no existeixi cap regla que tingui el terminal com a head
                if cnf:
                    new_body = [self.generate_terminal()]       # Si és CNF, genera un no terminal
                else:
                    new_body = [random.choice([self.generate_terminal(), self.generate_epsilon()])]  # Si no és CNF, genera un terminal o un epsilon
                self.grammar_dict[non_terminal].append(new_body) # Afegeix una nova regla en la que el símbol sigui el head i el body un terminal o un epsilon


        grammar = []                                                            # Inicialitza una llista buida per a emmagatzemar la gramàtica que es retornarà
        seen_rules = []                                                         # Inicializa una llista per emmagatzemar les regles ja vistes

        if probabilistic:                                                       # Comprova si s'ha triat amb probabilitats
            for head, body_list in self.grammar_dict.items():                   # Recorre el diccionari de la gramàtica
                probabilities = [random.uniform(0.01, 1) for _ in body_list]    # Assigna una probabilitat random a cada body d'un head determinat
                total = sum(probabilities)                                      
                normalized_probabilities = [p / total for p in probabilities]   # Assegura que la suma de les probabilitats de les regles que tenen un mateix head sumin 1
                for body, prob in zip(body_list, normalized_probabilities):
                    prob = round(prob, 2)                                       # Guarda només dos decimals de la probabilitat
                    rule = (head, body)
                    if rule not in seen_rules:                                  # Comprova si la regla ja està present a la gramática
                        grammar.append(((head, body), prob))                    # Afegeix la regla a la gramàtica
                        seen_rules.append(rule)                                 # Afegeix la regla a la llista de regles vistes
        else:                                                                   # En cas que no s'hagi triat probabilitats --> el mateix sense afegir probabilitats
            for head, body_list in self.grammar_dict.items():                       
                for body in body_list:
                    rule = (head, body)
                    if rule not in seen_rules:
                        grammar.append(rule)
                        seen_rules.append(rule)


        return grammar                  # Retorna la gramàtica creada
