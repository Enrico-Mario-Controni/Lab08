from database.impianto_DAO import ImpiantoDAO
from database.consumo_DAO import ConsumoDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        # TODO
        id_impianto=[]
        for impianto in self._impianti:
            id_impianto.append(impianto.id)

        lista_consumo_medio=[]
        for el in id_impianto:
            self._consumo= ConsumoDAO.get_consumi(el)
            consumo_totale= 0
            n=0
            for consumo in self._consumo:
                if consumo.data.month == mese :
                    consumo_totale+= consumo.kwh
                    n+=1

            consumo_medio = consumo_totale / n
            result=(el, consumo_medio)
            lista_consumo_medio.append(result)

        return lista_consumo_medio




    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        # TODO
        if giorno == 8:
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = list(sequenza_parziale)
            return


        for impianto_id in consumi_settimana.keys():

            costo = costo_corrente

            costo += consumi_settimana[impianto_id][giorno - 1]

            if ultimo_impianto is not None and impianto_id != ultimo_impianto:
                costo += 5


            sequenza_parziale.append(impianto_id)
            self.__ricorsione(sequenza_parziale, giorno + 1, impianto_id, costo, consumi_settimana)
            sequenza_parziale.pop()

    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        # TODO
        dizionario = {}
        for impianto in self._impianti:
            dizionario[impianto.id] = []

        for el in dizionario:
            self._consumi= ConsumoDAO.get_consumi(el)

            for consumo in self._consumi:
                if consumo.data.month == mese and consumo.data.day in range(1, 8):
                    dizionario[consumo.id_impianto].append(consumo.kwh)


        return dizionario

