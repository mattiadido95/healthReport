# import pandas as pd
# import matplotlib.pyplot as plt
#
#
# def plot():
#     # Carica il file CSV in un dataframe
#     df = pd.read_csv('output/Apple Watch di Mattia_ActiveEnergyBurned.csv')
#
#     # Converti le colonne startDate e endDate in formato data
#     df['startDate'] = pd.to_datetime(df['startDate'])
#     df['endDate'] = pd.to_datetime(df['endDate'])
#
#     # Seleziona solo le colonne startDate, endDate e value
#     df = df[['startDate', 'endDate', 'value']]
#
#     # Crea un nuovo dataframe con tutte le date in ordine cronologico e i valori di value associati
#     new_df = pd.DataFrame(columns=['date', 'value'])
#     for index, row in df.iterrows():
#         date_range = pd.date_range(start=row['startDate'], end=row['endDate'])
#         for date in date_range:
#             new_df = new_df.append({'date': date, 'value': row['value']}, ignore_index=True)
#
#     # Crea un grafico a linea con la data sull'asse x e il valore sull'asse y
#     plt.plot(new_df['date'], new_df['value'])
#     plt.xlabel('Data')
#     plt.ylabel('Valore')
#     plt.title('Andamento temporale dei valori')
#     plt.show()

import pandas as pd
import matplotlib.pyplot as plt


def plot():
    # carica il file CSV in un DataFrame
    df = pd.read_csv('output/Apple Watch di Mattia_ActiveEnergyBurned.csv')

    # inizializza una lista vuota
    data_list = []

    # itera su tutte le righe del DataFrame
    for _, row in df.iterrows():
        # genera la sequenza di date
        date_range = pd.date_range(start=row['startDate'], end=row['endDate'])
        # itera su tutte le date della sequenza
        for date in date_range:
            # crea un dizionario con le informazioni necessarie
            data_dict = {'date': date, 'value': row['value']}
            # aggiunge il dizionario alla lista
            data_list.append(data_dict)

    # crea il DataFrame finale a partire dalla lista di dizionari
    new_df = pd.DataFrame(data_list)

    # raggruppa i dati per data e calcola la media dei valori
    grouped_df = new_df.groupby('date').mean()

    # crea il grafico con la funzione plot di Pandas
    grouped_df.plot()

    # mostra il grafico
    plt.show()

# import pandas as pd
# import plotly.express as px
# from sklearn.decomposition import PCA
# from sklearn.preprocessing import StandardScaler
#
#
# def plot():
#     # carica il file CSV in un DataFrame
#     df = pd.read_csv('output/Apple Watch di Mattia_ActiveEnergyBurned.csv')
#
#     # elimina le righe contenenti valori mancanti
#     df.dropna(inplace=True)
#
#     # estrae i valori numerici dal DataFrame
#     X = df.iloc[:, 7:].values
#
#     # standardizza i dati
#     scaler = StandardScaler()
#     X = scaler.fit_transform(X)
#
#     # esegue la PCA
#     pca = PCA(n_components=2)
#     X_pca = pca.fit_transform(X)
#
#     # crea un nuovo DataFrame con i valori della PCA
#     pca_df = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])
#
#     # aggiunge la colonna 'value' al DataFrame
#     pca_df['value'] = df['value'].values
#
#     # crea il grafico PCA
#     fig = px.scatter(pca_df, x='PC1', y='PC2', color='value')
#
#     # salva il grafico in formato HTML
#     fig.write_html('pca_graph.html')
