class CNFConverter:

    def __init__(self, cfg_grammar, prob=False):
        """
        Inicialitza la classe.

        Paràmetres:
            cfg_grammar (list): Diccionari que representa la gramàtica lliure de context (CFG).
            prob (bool): Indica si la gramàtica és probabilística (per defecte és False).
        """
        self.cfg_grammar = cfg_grammar                  # Assigna la gramàtica CFG proporcionada a l'atribut de la classe.
        self.cnf_grammar = self.cfg_grammar.copy()      # Crea una còpia de la gramàtica CFG per modificar-la i convertir-la a CNF.
        self.prob = prob                                # Crea un atribut que indica si la gramàtica és probabilística o no
        self.epsilon = False                            # Crea un atribut que indica si el símbol inicial pot generar epsilon (inicialitzat a False)
        if not self.prob:                               # Comprova si pot generar epsilon, i en cas que pugui, canvia a True
            if self.cnf_grammar[0][1][0] == '':
                self.epsilon = True


    def is_cnf(self):
        '''
        Comprova si la gramàtica està en Forma Normal de Chomsky (CNF).

        Retorna:
            bool: True si la gramàtica està en CNF, False en cas contrari.
        '''

        for rule in self.cnf_grammar:
            
            # Es desempaqueta el head i body de la regla en funció de l'estructura que tingui (si és probabilístic o no)
            if self.prob:                   
                head, body = rule[0]    # Gramàtiques amb probabilitats
            else:
                head, body = rule       # Gramàtiques sense probabilitats

            if head != 'ST' and '' in body:             # Comprova que no hi ha hagi regles que generin epsilon (excepte que es tracti del símbol inicial)
                return False    
            
            if len(body) == 1 and body[0].isupper():    # Es comprova que les regles de longitud 1 són minúscules (terminals)
                return False
            
            if len(body) == 2:                          # Es comprova que les regles de longitud 2 són majúscules (no terminals)
                for elem in body:
                    if elem.islower():
                        return False
                    
            if len(body) != 1 and len(body) != 2:       # Si les regles no són de longitud 1 o 2, no es cumpleix i retorna False
                return False

        return True                                     # Si es cumpleix per a cada una de les regles, retorna True, indicant que si que està en FNC
    

    def create_start_symbol(self):
        '''
        Ajusta la gramàtica per assegurar que hi hagi un símbol únic d'inici 'ST'.

        Retorna:
            list: La gramàtica amb un símbolo de inici únic 'ST'.
        '''
        add = False         # Variable que indica si s'ha d'afegir una nova regla d'inici o no

        start = self.cnf_grammar[0][0]                                      # Obté el símbol d'inici accedint a la primera regla de la gramàtica
        for head, body in self.cnf_grammar:                                 # Verifica si el símbol apareix en el body d'alguna regla
            for elem in body:
                if start == elem:
                    add = True
                    break
            break
        if add:                                                             # En cas que apareixi, afegeix una nova regla
            self.cnf_grammar = [('ST', [start])] + self.cnf_grammar
        else:                                                               # En cas que no apareixi, es modifiquen les aparicions del nom del no terminal que correspon al símbol d'inici per 'ST'
            for idx, (head, body) in enumerate(self.cnf_grammar):
                if head == start:
                    self.cnf_grammar[idx] = ('ST', body)

        return self.cnf_grammar                    # Retorna la gramàtica modificada                    


    def remove_epsilon_productions(self):
        '''
        Elimina les epsilon (cadenenes buides) de la gramàtica.

        Retorna:
            list: La gramàtica sense les produccions epsilon.
        '''

        def stop():
            '''
            Comprova si encara queden produccions epsilon a la gramàtica.

            Retorna:
                bool: False si existeixen produccions epsilon, True en cas contrari.
            '''
            for _, body in self.cnf_grammar:
                if body == ['']:
                    return False
            return True
        
        epsilon = False                 # Variable que indica si s'han trobat produccions epsilon

        while not stop():               # Bucle fins que no quedin produccions epsilon

            epsilon = True              # Si entra al bucle, vol dir que haurà trobat alguna producció epsilon

            rules_with_epsilon = []         # Llista per a emmagatzemar les regles que generen epsilon
            rules_to_add = []               # Llista per a emmagatzemar les regles a afegir
            rules_to_remove = []            # Llista per a emmagatzemar les regles a eliminar

            for head, body in self.cnf_grammar:                # Identifica les regles que generen epsilon
                if len(body) == 1 and body[0] == '':
                    rules_with_epsilon.append((head, body))    # Les guarda a la llista corresponent

            heads = []                                     # Recull els caps de les regles que generen epsilon
            for head, body in rules_with_epsilon:
                heads.append(head)
            
            for head, body in self.cnf_grammar:            # Modifica les regles eliminant els heads que generen epsilon dels bodies
                new_body = []
                for elem in body:
                    if elem not in heads:
                        new_body.append(elem)

                if (head, new_body) not in rules_with_epsilon:
                    rules_to_add.append((head, new_body))
                rules_to_remove.append((head, body))

            
            self.cnf_grammar = [rule for rule in self.cnf_grammar if rule not in rules_to_add and rule not in rules_to_remove]      # Elimina les regles de la gramàtica corresponents

            self.cnf_grammar.extend(rules_to_add)        # Afegeix les noves regles a la gramàtica

            rules_to_modify = []                         # Identifica les regles buides per a ser modificades
            for head, body in self.cnf_grammar:
                if len(body) == 0:
                    rules_to_modify.append((head, body))

            for rule in rules_to_modify:                # Substitueix les regles buides per regles que generen epsilon (per a preparar la gramàtica per a la pròxima iteració de la funció)
                for idx, rule1 in enumerate(self.cnf_grammar):
                    if rule == rule1:
                        head, body = rule
                        body = ['']
                        self.cnf_grammar[idx] = head, body
            
        return self.cnf_grammar, epsilon       # Retorna la gramàtica modificada i la variable epsilon


    def remove_unit_productions(self):
        '''
        Elimina les regles unitàries (body amb un sol símbol no terminal) de la gramàtica.

        Retorna:
            llista: La gramàtica sense produccions unitàries.
        '''

        def stop():
            '''
            Comprova si encara queden produccions unitàries a la gramàtica.

            Retorna:
                bool: False si existeixen produccions unitàries, True en cas contrari.
            '''
            for _, body in self.cnf_grammar:
                if len(body) == 1 and not body[0].islower() and body[0] != '':
                    return False
            return True
        
        while not stop():
            unit_productions = []           # Llista per emmagatzemar les produccions unitàries (de l'estil: S -> A)
            rules_to_eliminate = []        # Llista per emmagatzemar les regles derivades de produccions unitàries a eliminar
            rules_to_add = []               # Llista per emmagatzemar les noves regles que s'han d'afegir

            for head, body in self.cnf_grammar:
                if len(body) == 1 and not body[0].islower() and body[0] != '':  # Busca una producció (body) que tingui longitud 1 i siguin majúscules (producció unitària)
                    unit_productions.append((head, body))                       # Afegeix la producció trobada a la llista de produccions unitàries
                    break

            for head, body in unit_productions:                                 # Recorre la llista creada de produccions unitàries
                for head1, body1 in self.cnf_grammar:                           # Recorre les regles de la gramàtica
                    if body[0] == head1:                                        # Busca una regla que tingui el head igual que el body de la producció unitària
                        rules_to_add.append((head, body1))                      # Afegeix la nova regla a la llista de regles per afegir a la gramàtica
                        rules_to_eliminate.append((head1, body1))               # Afegeix la regla antiga a regles per eliminar
            
            for head, body in rules_to_eliminate:                               # Recorre la llista de regles per eliminar
                for idx, (head1, body1) in enumerate(self.cnf_grammar):         # Recorre les regles de la gramàtica
                    for idx1, elem in enumerate(body1):                         # Recorre els elements del body de cada regla
                        if head == elem:                                        # Quan el head coincideix amb l'element del body d'alguna regla
                            body1[idx1] = body[0]                                          
                            self.cnf_grammar[idx] = (head1, body1)              # Es modifica la regla per una correcta

            self.cnf_grammar = [rule for rule in self.cnf_grammar if rule not in unit_productions and rule not in rules_to_eliminate]    # Elimina les regles emmagatzemades a les llsiter per eliminar
            self.cnf_grammar.extend(rules_to_add)                                                                                        # Afegeix les noves regles que substitueixen a les eliminades

        return self.cnf_grammar  # Retorna la gramàtica modificada
    

    def introduce_aux_symbols(self):
        '''
        Introdueix símbols auxiliars per a reemplaçar els símbols terminals en les regles mixtes.

        Retorna:
            list: La gramàtica modificada amb els símbols auxiliars afegits.
        '''

        def correct_symbols(body):
            '''
            Comprova si el body d'una regla conté tant símbols terminals com no terminals, o només símbols terminals.

            Paràmetres:
                body (list): El cos de la regla.

            Retorna:
                bool: True si el body conté símbols terminals i no terminals, o només terminals; False en cas contrari.
            '''
            has_terminal = any(symbol.islower() for symbol in body)         # Busca símbols terminals
            has_non_terminal = any(symbol.isupper() for symbol in body)     # Busca símbols no terminals
            return (has_terminal and has_non_terminal) or has_terminal      # Retorna True o False, depenent si es compleix o no

        rules_to_add = []  # Llista per emmagatzemar les noves regles

        for idx, (head, body) in enumerate(self.cnf_grammar):
            if len(body) > 1 and correct_symbols(body):                                         # Busca les regles que compleixen la condició (de longitud 1 o més i amb símbols mixtes o només amb terminals)
                for idx1, elem in enumerate(body):
                    if elem.islower():                                                          # Busca el símbol terminal en el body
                        new_non_terminal = str(elem.upper())                                    # Crea un nou no terminal per a substituir-lo
                        counter = 1
                        while new_non_terminal in rules_to_add or new_non_terminal in self.cnf_grammar:         # Comprova que el no terminal no existeix ja a la gramàtica,
                            new_non_terminal = str(elem.upper()) + str(counter)                                 # en cas que existeixi, li afegeix un número al nom i li va
                            counter += 1                                                                        # sumant unitats fins que no existeixi
                        rules_to_add.append((new_non_terminal, [elem]))     # Afegeix la nova regla a la llista correponent assignant probabilitat 1
                        body[idx1] = new_non_terminal
                        self.cnf_grammar[idx] = (head, body)                # Substitueix el terminal pel nou no terminal creat
                                            
        for head, body in rules_to_add:                                     # Modifica les regles de la gramàtica que han sigut afectades pel canvi (regles que contenen el símbol modificat)
            for idx, (head1, body1) in enumerate(self.cnf_grammar):
                if len(body) > 1:
                    for idx1, elem in enumerate(body1):
                        if elem == body[0]:
                            body1[idx1] = head
                            self.cnf_grammar[idx] = (head1, body1)
            if (head, body) not in self.cnf_grammar:                        # Afegeix les noves regles a la gramàtica evitant afegir regles repetides
                self.cnf_grammar.append((head, body))

        return self.cnf_grammar                                         # Retorna la gramàtica modificada


    def replace_long_productions(self):
        '''
        Reemplaça les regles llargues (més de 2 símbols) amb noves regles utilitzant símbols no terminals addicionals.

        Retorna:
            list: La gramàtica modificada amb  producciones largas reemplazadas.
        '''
        while not self.is_cnf():        # S'executa el codi tants cops com calgui fins que estigui correctament en FNC (ja que és l'últim pas)

            rules_to_add = []           # Llista per emmagatzemar les noves regles
            rules_to_modify = []        # Llista per emmagatzemar les regles que s'han de modificar
            existing_non_terminals = {rule[0] for rule in self.cnf_grammar} if not self.prob else {rule[0] for rule, _ in self.cnf_grammar} # Conjunt de símbols no terminals de la gramàtica

            for (head, body) in self.cnf_grammar:
                if len(body) > 2:                                           # Busca les regles que tenen més de 2 símbols
                    new_non_terminal = 'X'                                  # Crea un nou no terminal per substituir el body de la regla menys el primer element
                    counter = 1
                    while new_non_terminal in existing_non_terminals:       # S'assegura que el nou símbol sigui únic a la gramàtica
                        new_non_terminal = 'X' + str(counter)
                        counter += 1
                    existing_non_terminals.add(new_non_terminal)
                    new_body = body[1:]
                    rules_to_add.append((new_non_terminal, new_body))       # Afegeix la nova regla amb el nou símbol terminal com a head i la resta del body (menys el primer element), assignant una probabilitat de 1
                    body = [body[0], new_non_terminal]
                    rules_to_modify.append((head, body))                    # Afegeix la regla modificada a la llista de regles a modificar

            # Reemplaça les regles originals per les regles modificades si la gramàtica no és probabilística
            for head, new_body in rules_to_modify:
                for idx, (head1, body) in enumerate(self.cnf_grammar):
                    if head == head1 and len(body) > 2:
                        self.cnf_grammar[idx] = (head, new_body)
                        break

            self.cnf_grammar.extend(rules_to_add)               # Afegeix les noves regles a la gramàtica

        return self.cnf_grammar                                 # Retorna la gramàtica modificada


    def converter(self):
        '''
        Converteix una gramàtica CFG a CNF, cridant als mètodes necessaris per ordre.

        Retorna:
            list: La gramàtica en CNF
        '''
        self.create_start_symbol()             # Crea el símbol inicial
        
        if self.epsilon:                            # Si el símbol inicial pot generar epsilon
            first_rule = self.cnf_grammar[0]
            self.cnf_grammar.remove(first_rule)     # S'elimina de la gramàtica per evitar problemes durant la conversió

        _, epsilon = self.remove_epsilon_productions()       # Elimina els epsilon de la gramática
        self.remove_unit_productions()          # Elimina les regles unitàrias de la gramàtica
        self.introduce_aux_symbols()            # Introdueix símbols auxiliars per a reemplaçar els símbols terminals en les regles mixtes
        self.replace_long_productions()         # Reemplaça les produccions llargues per produccions de longitud

        if self.epsilon:                        # S'afegeix la regla eliminada anteriorment (en cas que s'hagi eliminat)
            self.cnf_grammar = [first_rule] + self.cnf_grammar

        if epsilon:                                     # En cas que el símbol inicial no generi epsilon i que alguna regla n'hagi generat
            if ('ST', ['']) not in self.cnf_grammar:
                self.cnf_grammar = [('ST', [''])] + self.cnf_grammar        # S'afegeix la regla que genera epsilon a partir del símbol inicial

        return self.cnf_grammar                 # Retorna la gramática en la seva forma normal de Chomsky (CNF)

