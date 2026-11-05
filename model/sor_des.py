"""Minimalny model DES SOR: lista zdarzeń (heapq), triaż FIFO, lekarze z kolejką wg koloru."""
import heapq, random, statistics as st

KOLORY = ["czerwony", "pomarańczowy", "żółty", "zielony", "niebieski"]
UDZIAL = [0.010, 0.052, 0.338, 0.549, 0.051]   # arkusz „Triaż – założenie”
KONSULT = [96, 48, 39, 31, 20]                 # min, mediana wg P26 (niebieski: założenie)
NORMA = [0, 10, 60, 120, 240]                  # min, rozporządzenie MZ
RATE = [2,1.5,1.2,1,1,1.2,2,4,6,7,7,6.5,6,5.5,5,5,5,5,4.5,4,3.5,3,2.5,2]  # pacjentów/h (~95/dobę)

def odstep_przyjazdu(t): return random.expovariate(RATE[int(t // 60) % 24] / 60)
def czas_triazu(): return random.expovariate(1 / 4)
def czas_wizyty(k): return random.lognormvariate(0, 0.5) * KONSULT[k] / 1.13

def symuluj(lekarze=3, triazysci=2, dni=30, seed=1):
    random.seed(seed)
    zdarzenia, licznik = [], 0                 # kolejka zdarzeń: (czas, nr, typ, dane)
    def planuj(t, typ, dane=None):
        nonlocal licznik; licznik += 1
        heapq.heappush(zdarzenia, (t, licznik, typ, dane))
    kol_triaz, kol_lek = [], []                # kolejki oczekujących
    wolni_t, wolni_l = triazysci, lekarze
    wyniki = [[] for _ in KOLORY]
    planuj(0, "przyjazd")
    koniec = dni * 24 * 60
    while zdarzenia:
        t, _, typ, p = heapq.heappop(zdarzenia)           # zegar skacze do następnego zdarzenia
        if t > koniec: break
        if typ == "przyjazd":
            k = random.choices(range(5), UDZIAL)[0]
            kol_triaz.append((t, k))
            planuj(t + odstep_przyjazdu(t), "przyjazd")
        elif typ == "koniec_triazu":
            wolni_t += 1
            heapq.heappush(kol_lek, (p[1], p[0]))         # priorytet = kolor, potem czas przyjazdu
        elif typ == "koniec_wizyty":
            wolni_l += 1
        while kol_triaz and wolni_t:                      # przydziel wolne zasoby
            t0, k = kol_triaz.pop(0); wolni_t -= 1
            planuj(t + czas_triazu(), "koniec_triazu", (t0, k))
        while kol_lek and wolni_l:
            k, t0 = heapq.heappop(kol_lek); wolni_l -= 1
            wyniki[k].append(t - t0)                      # czas do pierwszego kontaktu z lekarzem
            planuj(t + czas_wizyty(k), "koniec_wizyty")
    return wyniki

if __name__ == "__main__":
    POWTORZEN = 10                                       # niezależnych przebiegów po 30 dni
    for n in (3, 4):
        przebiegi = [symuluj(lekarze=n, seed=s) for s in range(POWTORZEN)]
        print(f"lekarzy: {n}")
        for k, nazwa in enumerate(KOLORY):
            sr = st.mean(st.mean(w[k]) for w in przebiegi)
            pr = st.mean(sum(x > NORMA[k] for x in w[k]) / len(w[k]) for w in przebiegi)
            print(f"  {nazwa:13s} średnia={sr:6.1f} min   >norma={pr:5.0%}" if k else f"  {nazwa:13s} średnia={sr:6.1f} min")
