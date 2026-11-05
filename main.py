from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "alternatives.csv"

CRITERIA = ["Batarya", "Performans", "Kamera", "Fiyat", "Marka"]
# Önceki çalışmadan kalan kriter ağırlıkları.
KNOWN_WEIGHTS = np.array([0.25, 0.25, 0.20, 0.20, 0.10], dtype=float)
# True: yüksek değer tercih edilir. False: düşük değer tercih edilir.
BENEFIT = np.array([True, True, True, False, True])


def load_data():
    """CSV dosyasını okur ve gerekli sütunları kontrol eder."""
    data = pd.read_csv(DATA_PATH)
    required = ["Telefon", *CRITERIA]
    missing = [column for column in required if column not in data.columns]
    if missing:
        raise ValueError(f"CSV dosyasında eksik sütun(lar): {missing}")
    if data[CRITERIA].isnull().any().any():
        raise ValueError("Kriter puanlarında boş değer bulunuyor.")
    return data


def ahp_from_known_weights(weights):
    """
    Bilinen ağırlık oranlarından tutarlı bir AHP ikili karşılaştırma
    matrisi oluşturur. Bu, özgün anket matrisi değildir.
    """
    matrix = weights[:, None] / weights[None, :]
    geometric_means = np.prod(matrix, axis=1) ** (1 / len(weights))
    ahp_weights = geometric_means / geometric_means.sum()

    eigenvalues = np.linalg.eigvals(matrix)
    lambda_max = float(np.max(eigenvalues.real))
    n = len(weights)
    consistency_index = (lambda_max - n) / (n - 1)

    # Saaty rassal indeks değerleri (n=1..10)
    random_index = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
                    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
    ri = random_index[n]
    consistency_ratio = consistency_index / ri if ri else 0.0
    return matrix, ahp_weights, consistency_ratio


def normalize_smart(values, benefit):
    """SMART için 0-1 min-max normalizasyonu uygular."""
    normalized = np.zeros_like(values, dtype=float)

    for column in range(values.shape[1]):
        minimum = values[:, column].min()
        maximum = values[:, column].max()
        value_range = maximum - minimum

        if value_range == 0:
            normalized[:, column] = 1.0
        elif benefit[column]:
            normalized[:, column] = (values[:, column] - minimum) / value_range
        else:
            normalized[:, column] = (maximum - values[:, column]) / value_range

    return normalized


def smart_method(values, weights, benefit):
    normalized = normalize_smart(values, benefit)
    scores = normalized @ weights
    return scores


def topsis_method(values, weights, benefit):
    """Klasik vektör normalizasyonlu TOPSIS hesaplaması."""
    norms = np.sqrt((values ** 2).sum(axis=0))
    norms[norms == 0] = 1.0
    normalized = values / norms
    weighted = normalized * weights

    ideal_best = np.where(benefit, weighted.max(axis=0), weighted.min(axis=0))
    ideal_worst = np.where(benefit, weighted.min(axis=0), weighted.max(axis=0))

    distance_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    distance_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))
    denominator = distance_best + distance_worst
    denominator[denominator == 0] = 1.0

    return distance_worst / denominator


def print_ranking(title, names, scores):
    results = pd.DataFrame({"Telefon": names, "Skor": scores})
    results = results.sort_values("Skor", ascending=False).reset_index(drop=True)
    print(f"\n{title}")
    print("-" * 42)
    for index, row in results.iterrows():
        print(f"{index + 1}. {row['Telefon']:<22} {row['Skor']:.4f}")


def main():
    data = load_data()
    names = data["Telefon"].tolist()
    values = data[CRITERIA].to_numpy(dtype=float)

    pairwise_matrix, ahp_weights, cr = ahp_from_known_weights(KNOWN_WEIGHTS)

    print("AHP ikili karşılaştırma matrisi:")
    print(pd.DataFrame(pairwise_matrix, index=CRITERIA, columns=CRITERIA).round(3))
    print("\nAHP kriter ağırlıkları:")
    for criterion, weight in zip(CRITERIA, ahp_weights):
        print(f"{criterion:<12}: {weight:.3f}")
    print(f"Tutarlılık oranı (CR): {cr:.6f}")

    smart_scores = smart_method(values, ahp_weights, BENEFIT)
    topsis_scores = topsis_method(values, ahp_weights, BENEFIT)

    print_ranking("SMART sıralaması", names, smart_scores)
    print_ranking("TOPSIS sıralaması", names, topsis_scores)


if __name__ == "__main__":
    main()
