# - un ciclo inizia con un sottociclo di 2 gradi inferiore rialzista e deve
#   superare uno swing del precedente ciclo
# - un ciclo termina con un sottociclo di 3 gradi inferiori ribassista
# - nella ciclica evoluta, affinché un ciclo ribassista si reputi chiuso,
#   basta ch'esso sia sotto il minimo di partenza e non sotto il minimo più basso che abbia fatto
class CicliAnalisiDinamicaInversa:
    def __init__(self, dataset_candlestick, regole_ciclo):
        grado, tipo, soglie = regole_ciclo
        self.dataset = dataset_candlestick
        self.grado = grado
        self.tipo = tipo
        self.soglie = soglie
        self.cicli = []

    def check_closing_condition(self, index):
        # - un ciclo termina con un sottociclo di 3 gradi inferiori ribassista
        print(f"Checking closing cycle condition {self.grado} {index}")
        highs = self.dataset['High']
        current = highs[index]
        min = int(self.soglie[0]/6)
        max = int(self.soglie[2]/6)

        start_cycle_max = highs[index-max:index-1]
        max_cycle_max = start_cycle_max.max()
        start_cycle = highs[index-min:index-1]
        max_cycle = start_cycle.max()

        return current>max_cycle_max and current>max_cycle



    def check_open_condition(self, index):
        # - un ciclo inizia con un sottociclo di 2 gradi inferiore rialzista e deve
        #   superare uno swing del precedente ciclo
        #   divide seglie times 4 --> ciclo 2 gradi inferiore
        print(f"Checking opening cycle condition {self.grado} {index}")
        highs = self.dataset['High']
        current = highs[index]
        min = int(self.soglie[0]/4)
        max = int(self.soglie[2]/4)

        start_cycle_max = highs[index+1:index+max]
        min_cycle_max = start_cycle_max.max()

        start_cycle = highs[index+1:index+min]
        min_cycle = start_cycle.max()
        return current>min_cycle and current>min_cycle_max


    def verifica_ciclo(self, index):
        print(f"verifica ciclo {index}")
        return self.check_open_condition(index) and self.check_closing_condition(index)



    def trova_cicli(self):
        print(f"dataset size {len(self.dataset)}")
        print(f"trova cicli grado {self.grado} {self.tipo} {self.soglie}")
        cicli = [self.verifica_ciclo(i) for i in range(len(self.dataset))]
        #print(cicli)
        return cicli





