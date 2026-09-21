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
    return
