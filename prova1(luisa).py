import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def execute():
    # Passo 1: Importação e separação de dados

    base = pd.read_csv(r"C:\Users\luisa\Desktop\intel_c\Prova1\imoveis.csv")
    print(base)

    previsores = base.iloc[:,0:80].values
    classe = base.iloc[:,80].values
    print("Classe: ", classe)
    print("Previsores: ", previsores)

    # Passo 2: Transformar dados categóricos em numéricos
    from sklearn.preprocessing import LabelEncoder
    LEprevisores = LabelEncoder()

    strings = [2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 35, 39, 40, 41,
          42, 53, 55, 57, 58, 60, 63, 64, 65, 72, 73, 74, 78, 79]
    for x in strings:
        previsores[:, x] = LEprevisores.fit_transform(previsores[:, x])



    # Passo 3: Dados faltantes do grupo de previsores

    from sklearn.impute import SimpleImputer

    imputer=SimpleImputer(missing_values=np.nan,strategy='mean')
    imputer=imputer.fit(previsores)
    previsores=imputer.transform(previsores)

    # Passo 4: Normalização dos Dados
    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    previsoresNormalizado = scaler.fit_transform(previsores)


    # Passo 5: Validação de dados.

    from sklearn.cluster import KMeans

    kmeans_kwargs = {
    "init": "random",
    "n_init": 10,
    "max_iter": 300,
    "random_state": 42,
    }
    sse = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(previsoresNormalizado)
        sse.append(kmeans.inertia_)

    plt.style.use("fivethirtyeight")
    plt.plot(range(1, 11), sse)
    plt.xticks(range(1, 11))
    plt.xlabel("Number of Clusters")
    plt.ylabel("SSE")
    plt.show()

    from kneed import KneeLocator
    kl = KneeLocator(range(1, 11), sse, curve= "convex", direction = "decreasing")
    print("Valor do cotovelo ou elbow: ",kl.elbow)

    from sklearn.metrics import silhouette_score

    silhouette_coefficients = []
    for k in range(2, 11):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(previsoresNormalizado)
        score = silhouette_score(previsoresNormalizado, kmeans.labels_)
        silhouette_coefficients.append(score)


    plt.style.use("fivethirtyeight")
    plt.plot(range(2, 11), silhouette_coefficients)
    plt.xticks(range(2, 11))
    plt.xlabel("Number of Clusters")
    plt.ylabel("Silhouette Coefficient")
    plt.show()

    # Passo 6: Clusterização

    df = base
    kmeans = KMeans(n_clusters=3, random_state=0)
    kmeans.fit(previsoresNormalizado)
    y = kmeans.labels_
    df["k-classes"] = y
    print("Clusters: ",y)

    # salva os arquivos

    print(df["k-classes"] .tolist())

    salva = pd.DataFrame(df["k-classes"])
    de = pd.ExcelWriter("C:\\Users\\luisa\Desktop\\intel_c\\Prova1\\y.xlsx",engine='xlsxwriter')
    salva.to_excel(de)
    de.save()

if __name__ == "__main__":
    execute()
