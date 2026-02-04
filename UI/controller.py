import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        try:
            self._model.ruolo= str(self._view.dd_ruolo.value)   # aggiorna attr del model (str)
        except:
            self._view._alert.show_alert('selezionare un ruolo')
            return

        self._model.creagrafo() # aggiorna self.nodes, self.edges, self.grafo

        numn= self._model.getnodescollegati()
        numar= self._model.G.number_of_edges()

        self._view.list_risultato.controls.clear()
        self._view.list_risultato.controls.append(ft.Text(f"Nodi : {numn}, archi {numar}"))

        self._view.btn_classifica.disabled = False

        self._view._page.update()

    def handle_classifica(self, e):
        classifica= self._model.get_classifica_influenza()  # [(obj-artista, delta-float)]  gia ord
        self._view.list_risultato.controls.clear()
        self._view.list_risultato.controls.append(ft.Text(f"artisti in ordine decrescente di influenza:"))

        for tup in classifica:
            nome= tup[0].name
            delta = tup[1]
            self._view.list_risultato.controls.append(ft.Text(f"{nome} --> {delta}"))

        self._view.btn_cerca_percorso.disabled = False
        self._view._page.update()

    def getruoli(self):
        ruoli = self._model.getruoli()      #[ruolo-str]
        return ruoli
