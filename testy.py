import matplotlib.pyplot as plt

# Dane dla pierwszego wykresu
x1 = [1, 2, 3, 4, 5]
y1 = [10, 12, 5, 8, 9]

# Dane dla drugiego wykresu
x2 = [1, 2, 3, 4, 5]
y2 = [5, 8, 6, 4, 7]

# Rysowanie pierwszego wykresu (linia)
plt.plot(x1, y1, label='Wykres 1')

# Rysowanie drugiego wykresu (punkty)
plt.plot(x2, y2, label='Wykres 2', marker='o')

# Dodanie etykiet i legendy
plt.xlabel('Oś X')
plt.ylabel('Oś Y')
plt.legend()

# Wyświetlenie wykresu
plt.show()