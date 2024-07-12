class MainApp:
    def __init__(self):
        self.zmienna = 1

    def metoda(self):
        print(metoda)

    def metoda2(self):

        zmienna = inst1.metoda_inst(self.zmienna)
        print(zmienna)

class Printer:
    def __init__(self):
        self.skladowwa = 2
    def metoda_inst(self, zmienna):
        wynik = zmienna + self.skladowwa
        return wynik

app = MainApp()
inst1 = Printer()

app.metoda2()
