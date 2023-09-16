from assets.general_eleana_methods import Eleana
eleana = Eleana()

class Upadte():

    def first(self,sel_first_widget):
        entries = ['None']
        for single_data in eleana.dataset:
           val: str = single_data.name
           entries.append(val)
        app.sel_first_widget.configure(values=entries)
