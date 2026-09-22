import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

dates = pd.date_range('20190214', periods=6)
numbers = np.matrix([[ 101, 103], [105.5, 75], [102, 80.3], [100, 85], [110, 98], [109.6, 125.7 ]] )
frame = pd.DataFrame(numbers, index=dates, columns=['A','B'])


class DataFrameUzduotys:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def pirma_antra(self, idx: str | datetime.datetime) -> pd.Series:
        """
        gauti eilutę, kurios indekso data yra stringas '2019-02-18'
        gauti eilutę, kurios indekso data yra datetime.datetime(2019, 2, 18)
        """
        return self.df.loc[idx]

    def trecia(self):
        """
        gauti eilutę, kuri yra priešpaskutinė nuo galo (nenaudoti indekso)
        """
        return self.df.iloc[-2]

    def ketvirta(self):
        """
        gauti pirmas 2 eilutes ir stulpelį 'B' (nenaudoti indekso)
        """
        return self.df['B'][:2]

    def penkta(self):
        """
        išrūšiuoti df pagal 'B' stulpelį mažėjančia tvarka
        """
        return self.df.sort_values(by='B', ascending=False)

    def sesta(self):
        """
        rasti stulpelio 'A' didžiausią reikšmę
        """
        return self.df.max(axis=0)['A']

    def septinta(self):
        """
        padvigubinti stulpelio 'A' didžiausią reikšmę (randate, kuri didžiausia reikšmė ir priskiriate dvigubai didesnę naują reikšmę)
        :return:
        """
        max_val = self.df.max(axis=0)['A']
        self.df.loc[self.df['A'] == max_val, 'A'] = max_val * 2
        return

    def astunta(self):
        """
        gauti eilutes, kur stulpelio 'A' reikšmės didesnės už 105
        """
        return self.df[self.df['A'] > 105]

    def devinta(self):
        self.df.plot(y='A')
        return

    def desimta(self):
        self.df.drop(index=self.df.index[self.df['A'] < self.df['B']], inplace=True)
        return


# DATAFRAME

uzd = DataFrameUzduotys(frame)

print(f"""# 1. gauti eilutę, kurios indekso data yra stringas '2019-02-18'
Atsakymas:
{uzd.pirma_antra('2019-02-18')}
\n""")

print(f"""# 2. gauti eilutę, kurios indekso data yra datetime.datetime(2019, 2, 18)
Atsakymas:
{uzd.pirma_antra(datetime.datetime(2019, 2, 18))}
\n""")

print(f"""# 3. gauti eilutę, kuri yra priešpaskutinė nuo galo (nenaudoti indekso)
Atsakymas:
{uzd.trecia()}
\n""")

print(f"""# 4. gauti pirmas 2 eilutes ir stulpelį 'B' (nenaudoti indekso)
Atsakymas:
{uzd.ketvirta()}
\n""")

print(f"""# 5. išrūšiuoti df pagal 'B' stulpelį mažėjančia tvarka
Atsakymas:
{uzd.penkta()}
\n""")

print(f"""# 6. rasti stulpelio 'A' didžiausią reikšmę
Atsakymas:
{uzd.sesta()}
\n""")

uzd.septinta()
print(f"""# 7. padvigubinti stulpelio 'A' didžiausią reikšmę (randate, kuri didžiausia reikšmė ir priskiriate dvigubai didesnę naują reikšmę)
Atsakymas:
{uzd.df}
\n""")

print(f"""# 8. gauti eilutes, kur stulpelio 'A' reikšmės didesnės už 105
Atsakymas:
{uzd.astunta()}
\n""")

uzd.devinta()
print(f"""# 9. nupiešti (plot) stulpelio 'A' reikšmes
Atsakymas:
\n""")

uzd.desimta()
print(f"""# 10. ištrinti eilutes, kur stulpelio 'B' reikšmės yra didesnės už stulpelio 'A' reikšmes
Atsakymas:
{uzd.df}
\n""")

plt.show()

# NUMPY

def pirma():
    a = np.random.randint(low=1, high=10, size=10)
    b = np.random.randint(low=1, high=10, size=10)
    return a.sum() + b.sum()


def antra():
    a = np.random.randint(low=-10, high=10, size=10)
    a[a > 0] = 0
    return a


def trecia():
    a = np.random.randint(low=1, high=10, size=10)
    b = a[a <= 6]
    return a, b


def ketvirta():
    a = np.random.randint(low=1, high=5, size=10)
    print(a)
    return a[1:][a[1:] == a[:-1]]


def penkta():
    a = np.random.random(size=10)
    b = np.random.random(size=10)
    return a[a > b]


def sesta():
    a = np.random.randint(low=1, high=10, size=10)
    print(a)
    a[:-1] = a[1:]
    return a


def septinta():
    a = np.random.randint(low=1, high=10, size=10)
    print(a)
    return a[::-1]


def astunta():
    a = np.random.randint(low=1, high=10, size=10)
    a[1::2] = 0
    return a


def devinta():
    a = np.random.rand(10, 20)
    return np.mean(a, axis=1), np.mean(a, axis=0)


def desimta():
    a = np.random.randint(1, 10, (10, 10))
    print(a)
    return a[np.arange(10), np.arange(10)]



print(f"""# 1. suma 2 vektorių
Atsakymas:
{pirma()}
\n""")

print(f"""# 2. anuliavimas teigiamų elementų
Atsakymas:
{antra()}
\n""")

print(f"""# 3. išmetimas > 6
Atsakymas:
{trecia()}
\n""")

print(f"""# 4. dviejų vienodų šalia esančių radimas
Atsakymas:
{ketvirta()}
\n""")

print(f"""# 5. elementų, kur a elementai didesni už b elementus, radimas
Atsakymas:
{penkta()}
\n""")

print(f"""# 6. elementų perstumimas vektoriuje pakartojant paskutinį
Atsakymas:
{sesta()}
\n""")

print(f"""# 7. sukeitimas elementų eilės tvarkos
Atsakymas:
{septinta()}
\n""")

print(f"""# 8. kas antro elemento užnulinimas
Atsakymas:
{astunta()}
\n""")

print(f"""# 9. rasti matricos eiluciu vidurkius, rasti matricos stulpeliu vidurkius
Atsakymas:
{devinta()}
\n""")

print(f"""# 10. gauti matricos diagonalinius elementus - negalima panaudoti diag ir t.t.
Atsakymas:
{desimta()}
\n""")