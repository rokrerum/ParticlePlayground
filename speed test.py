import numpy as np
import time

n = 1_000_000

# ---- Zwykła lista Pythona z pętlą ----
lista = list(range(n))

start = time.time()
for i in range(len(lista)):
    lista[i] += 1
czas_lista = time.time() - start

# ---- NumPy z pętlą for ----
tablica_petla = np.arange(n)

start = time.time()
for i in range(len(tablica_petla)):
    tablica_petla[i] += 1
czas_numpy_petla = time.time() - start

# ---- NumPy wektoryzacja (bez pętli) ----
tablica = np.arange(n)

start = time.time()
tablica += 1
czas_numpy = time.time() - start

# ---- Wyniki ----
print(f"Lista Pythona z pętlą:  {czas_lista:.4f} s")
print(f"NumPy z pętlą for:      {czas_numpy_petla:.4f} s")
print(f"NumPy wektoryzacja:     {czas_numpy:.4f} s")
print()
print(f"NumPy wektoryzacja jest {czas_lista / czas_numpy:.1f}x szybsze od listy")
print(f"NumPy wektoryzacja jest {czas_numpy_petla / czas_numpy:.1f}x szybsze od NumPy z pętlą")