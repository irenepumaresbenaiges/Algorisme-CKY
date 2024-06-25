import random
import copy
from converter import CNFConverter
from cky import CKY
from cky_probabilistic import ProbabilisticCKY
from grammar_generator import GenerateGrammar
from word_generator import GenerateWord



def executar_experiment(cnf, probabilistic, valid):
    """
    Executa un experiment per generar una gramàtica i una paraula,
    convertir la gramàtica a CNF si cal, i verificar si la paraula pertany a la gramàtica.
    
    Paràmetres:
        cnf (bool): Indica si la gramàtica ha de ser en CNF o no.
        probabilistic (bool): Indica si la gramàtica és probabilística o no.
        pertany (bool): Indica si la paraula ha de pertànyer a la gramàtica o no.

    Retorna:
        tuple: Conté la gramàtica original, la gramàtica en CNF, la paraula generada i el resultat de la verificació.
    """
    generator = GenerateGrammar()                                           # Crea una instància de la classe GenerateGrammar
    grammar = generator.generate_random_grammar(cnf, probabilistic)         # Genera la gramàtica cridant al mètode correponent amb els paràmetres donats
    original_grammar = copy.deepcopy(grammar)

    print("Aquesta és la gramàtica original:")                              # Mostra la gramàtica original
    if probabilistic:
        for rule, probability in original_grammar:
            head, body = rule
            print(f"(({head}, {body}), {probability})")
    else:
        for head, body in original_grammar:
            print(f"({head}, {body})")

    gram = CNFConverter(grammar, prob=probabilistic)                        # Crea una instància de la classe CNFConverter
    
    if gram.is_cnf():                                                       # Si la gramàtica ja està en CNF, imprimeix un missatge indicant-ho
        cnf_grammar = grammar
        print("La gramàtica original ja està en CNF.")
    else:                                                                   # Si la gramàtica no està en CNF, crida al mètode per a converir-la i s'imprimeix la gramàtica tarnsformada
        cnf_grammar = gram.converter()
        print("S'ha convertit a CNF amb èxit!")
        print("Aquesta és la gramàtica transformada:")
        for head, body in cnf_grammar:                                      # (només en cas que no sigui probabilística)
            print(f"({head}, {body})")

    word_generator = GenerateWord(cnf_grammar, probabilistic)               # Crea una instància de la classe GenerateWord
    word = word_generator.generate_word(valid=valid)                        # Genera una paraula aleatòria cridant al mètode correponent indicant si ha de pertànyer o no a la gramàtica proporcionada
    print(f"Aquesta és la paraula que es comprova: {word}")                 # Mostra la paraula creada

    if probabilistic:                                                       # Si és probabilístic:
        cky_prob = ProbabilisticCKY(cnf_grammar)                            # Crea una instància de la classe ProbabilisticCKY
        result = cky_prob.parse(word)                                       # Crida al mètode parse per a comprovar si la paraula pertany a la gramàtica i la seva probabilitat
        if result == False:
            print("La paraula pertany al llenguatge de la gramàtica: ", result)
        else:
            print("La paraula pertany al llenguatge de la gramàtica amb una probabilitat de: ", result)     # Mostra la probabilitat o False
    else:                                                                       # Si no és probabilístic:
        cky = CKY(cnf_grammar)                                                  # Crea una instància de la calsse CKY
        result = cky.parse(word)                                                # Crida al mètode parse per a comprovar si la paraula pertany a la gramàtica
        print("La paraula pertany al llenguatge de la gramàtica: ", result)     # Mostra el resultat (True/False)

    return original_grammar, cnf_grammar, word, result, cnf                     # Retorna la gramàtica inicial, la gramàtica modificada, la paraula i el resultat


if __name__ == "__main__":
    print("Benvingut a l'algorisme CKY")                                            # Mostra un missatge de benvinguda a l'usuari
    print("Tria entre les següents opcions:")                                       # Mostra les opcions de l'usuari
    print("1. Executar la gramàtica i la paraula per defecte definida al main")
    print("2. Executar un experiment personalitzat amb una gramàtica i una paraula creades aleatòriament")
    print("3. Executar el joc de proves creat per nosaltres")
    
    pregunta = input("Quina opció vols executar? (1, 2 o 3): ")                     # Demana a l'usuari que triï una opció

    while pregunta != '1' and pregunta != '2' and pregunta != '3':                  # Comprova que la resposta sigui vàlida
        print("Resposta no vàlida. Si us plau, introdueix '1', '2' o '3'.")
        pregunta = input("Quina opció vols executar? (1, 2 o 3): ")
    
    if pregunta == '1':                                                             # Si l'usuari escull l'opció 1:
        print("La gramàtica per defecte és probabilística i està en CNF.")          # S'informa sobre la gramàtica i com procedir
        print("Si la vols canviar, edita el fitxer main.py.")

        grammar = [                         # Substituir per la gramàtica que es vulgui provar
            (('ST', ['A', 'B']), 1.00),
            (('A', ['C', 'D']), 0.7),
            (('A', ['a']), 0.3),
            (('B', ['E', 'F']), 0.6),
            (('B', ['b']), 0.4),
            (('C', ['c']), 1.00),
            (('D', ['d']), 1.00),
            (('E', ['e']), 1.00),
            (('F', ['f']), 1.00)
        ]

        word = 'cdef'                       # Substituir per la paraula que es vulgui provar

        prob = False                        # Determina si la gramàtica és probabilística
        if len(grammar[0][0]) == 2:
            prob = True

        print("Aquesta és la gramàtica original:")                      # Mostra la gramàtica original
        if prob:
            for rule, probability in grammar:
                head, body = rule
                print(f"(({head}, {body}), {probability})")
        else:
            for head, body in grammar:
                print(f"({head}, {body})")

        gram = CNFConverter(grammar, prob=prob)                         # Crea una instàncai de la classe CNFConverter

        if gram.is_cnf():                                               # Si cal, transforma la gramàtica a CNF i s'imprimeix, sinó, indica a l'usuari que ja està en CNF
            cnf_grammar = grammar
            print("La gramàtica original ja està en CNF.")
        else:
            cnf_grammar = gram.converter()
            print("S'ha convertit a CNF amb èxit!")
            print("Aquesta és la gramàtica transformada:")
            if prob:
                for rule, probability in cnf_grammar:
                    head, body = rule
                    print(f"(({head}, {body}), {probability})")
            else:
                for head, body in cnf_grammar:
                    print(f"({head}, {body})")
        
        
        print(f"Aquesta és la paraula que es comprova: {word}")         # Mostra la paraula que es comprova

        if prob:                                                        # Si és probabilístic:
            cky_prob = ProbabilisticCKY(cnf_grammar)                    # Crea una instància de la classe ProbabilisticCKY
            result = cky_prob.parse(word)                               # Comprova si la paraula pertany i la seva probabilitat
            if result == False:                                         # Mostra el resultat
                print("La paraula pertany al llenguatge de la gramàtica: ", result)
            else:
                print("La paraula pertany al llenguatge de la gramàtica amb una probabilitat de: ", result)
        else:                                                           # Si no és probabilístic:
            cky = CKY(cnf_grammar)                                      # Crea una instància de la classe CKY
            result = cky.parse(word)                                    # Comprova si la paraula pertany a la gramàtica
            print("La paraula pertany al llenguatge de la gramàtica: ", result)      # Mostra el resultat   

    elif pregunta == '2':               # Si l'usuari escull l'opció 2:

        prob = input("Vols que la gramàtica sigui probabilística? (y/n): ")         # Demana si es vol que la gramàtica sigui probabilística o no
        while prob != 'y' and prob != 'n':                                          # Comprova que la resposta sigui vàlida
            print("Resposta no vàlida. Si us plau, introdueix 'y' o 'n'.")
            prob = input("Vols que la gramàtica sigui probabilística? (y/n): ")
        if prob == 'y':                                                             # Assigna la variable probabilistic segons la resposta
            probabilistic = True
        else:
            probabilistic = False

        if probabilistic == False:                                                     # Si s'ha triat no probabilístic
            format = input("Vols que la gramàtica estigui en CNF? (y/n): ")            # Demana si es vol la gramàtica en CNF o no
            while format != 'y' and format != 'n':                                     # Comprova que la resposta sigui vàlida
                print("Resposta no vàlida. Si us plau, introdueix 'y' o 'n'.")
                format = input("Vols que la gramàtica estigui en CNF? (y/n): ")
            if format == 'y':                                                          # Assigna la variable cnf segons la resposta
                cnf = True
            else:
                cnf = False
        else: 
            print('Com que has escollit una gramàtica probabilística, estarà en CNF per defecte.')      # Informa a l'usuari en cas que s'hagi escollit probabilística
            cnf = True

        pertany_word = input("Vols que la paraula que es vol comprovar pertanyi a la gramàtica o no? (y/n): ")      # Demana a l'usuari si vol que la paraula creada pertanyi o no a la gramàtica

        while pertany_word != 'y' and pertany_word != 'n':                                                          # Comprova que la resposta sigui vàlida
            print("Resposta no vàlida. Si us plau, introdueix 'y' o 'n'.")
            pertany_word = input("Vols que la paraula que es vol comprovar pertanyi a la gramàtica o no? (y/n): ")
        if pertany_word == 'y':                                                                                     # Assigna la variable valid segons la resposta
            valid = True
        else:
            valid = False

        print(f"Experiment personalitzat: CNF={cnf}, Probabilistic={probabilistic}, Pertany={valid}")
        executar_experiment(cnf, probabilistic, valid)                                                              # Executa l'experiment i imprimeix els resultats
        

    else:                          # Si l'usuari escull l'opció 3: 9876543
        random.seed(9876543)       # Fixa la llavor per reproduir els mateixos resultats

        experiments = [            # Defineix els paràmetres dels experiment a realitzar
            (True, False, True),
            (True, False, False),
            (True, True, True),
            (True, True, False),
            (False, False, True),
            (False, False, False)
        ]

        results = []                # Crea una llista per guardar els resultats

        for i, (cnf, probabilistic, valid) in enumerate(experiments):         # Executa els experiments i guarda els resultats a la llista creada
            print(f"Executant experiment {i+1}: CNF={cnf}, Probabilistic={probabilistic}, Pertany={valid}")
            original_grammar, cnf_grammar, word, result, cnf = executar_experiment(cnf, probabilistic, valid)
            results.append((original_grammar, cnf_grammar, word, result, cnf))

        with open('resultats_joc_de_proves.txt', 'w') as file:                  # Guarda els resultats en un fitxer de text
            for num, (original_grammar, cnf_grammar, word, result, cnf) in enumerate(results):
                file.write(f"Experiment {num+1}\n")
                file.write("\n")
                file.write("    Gramàtica original:\n")
                for rule in original_grammar:
                    file.write("        " + str(rule) + ",\n")
                file.write("\n")
                if cnf:
                    file.write("        La gramàtica original ja està en CNF\n")
                else:
                    file.write("    Gramàtica en CNF:\n")
                    for rule in cnf_grammar:
                        file.write("        " + str(rule) + ",\n")
                file.write("\n")
                file.write(f"    Paraula: '{word}'\n")
                file.write("\n")                
                file.write(f"    Resultat: {result}\n")
                file.write("\n")
            file.write("\n")

        print("Resultats guardats en 'resultats_joc_de_proves.txt'.")           # Informa que els resultats s'han guardat
