from functions import *
import faiss
import os


def find_similar(image_path, top_k=3):
    """Wyszukiwanie najbardziej podobnych obrazów"""
    query_vector = extract_features(image_path).reshape(1, -1)  # Pobranie cech obrazu do wyszukania
    distances, indices = index.search(query_vector, top_k)  # Szukamy w bazie

    print("\nNajbardziej podobne obrazy:")
    for i in range(top_k):
        print(f"{i+1}. {image_paths[indices[0][i]]} (odległość: {distances[0][i]:.4f})")

# Testujemy na jednym obrazie
#vector = extract_features("Database/Cats/9ac9f273-0cdc-4656-ae08-23291247971d.jpg")
#print(f"Rozmiar wektora cech: {vector.shape}")  # Powinno zwrócić (1280,)

# Tworzymy pustą bazę FAISS (indeks)
dimension = 1280  # MobileNetV2 zwraca wektory o długości 1280
index = faiss.IndexFlatL2(dimension)  # Używamy metryki L2 (odległość euklidesowa)

# Ścieżka do folderu z bazą obrazów
database_folder = "Database/Cats"
#database_folder = "Database/Dogs"
# Wczytujemy i dodajemy obrazy do FAISS
image_paths = []
features_list = []

for file_name in os.listdir(database_folder):
    img_path = os.path.join(database_folder, file_name)
    features = extract_features(img_path)

    index.add(np.array([features], dtype=np.float32))  # Dodajemy wektor do FAISS
    image_paths.append(img_path)  # Zapisujemy ścieżkę do obrazu
    features_list.append(features)

print(f"Dodano {len(features_list)} obrazów do bazy!")

# Testujemy na nowym zdjęciu
find_similar("Database/44c07aa1-ba8f-4ffd-988a-bed519494df8.jpg")