import os
import shutil
import random
from pathlib import Path

def create_train_test_split(source_dir, target_dir, test_ratio):
    """
    Rozdelí dataset obrázkov na trénovaciu a testovaciu sadu
    
    Args:
        source_dir (str): Cesta k zdrojovému datasetu (obsahuje priečinky s triedami)
        target_dir (str): Cesta kde sa majú vytvoriť train/test priečinky
        test_ratio (float): Pomer testovacích dát (0.2 = 20%)
        random_seed (int): Seed pre reprodukovateľnosť
    """
    
    # Nastavenie random seed pre reprodukovateľnosť, ak treba..
    # random.seed(random_seed)
    
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    # Vytvorenie štruktúry priečinkov
    train_dir = target_path / "train"
    test_dir = target_path / "test"
    
    # Získanie všetkých tried (priečinkov s obrázkami)
    classes = [d for d in source_path.iterdir() if d.is_dir()]
    
    print(f"Našiel som {len(classes)} tried: {[c.name for c in classes]}")
    
    train_idx = 1
    all_train_counts = 0
    splits = {}

    for class_dir in classes:
        class_name = class_dir.name
        
        # Vytvorenie priečinkov pre danú triedu
        train_class_dir = train_dir / class_name
        test_class_dir = test_dir / class_name
        
        train_class_dir.mkdir(parents=True, exist_ok=True)
        test_class_dir.mkdir(parents=True, exist_ok=True)
        
        # Získanie všetkých obrázkov v danej triede
        image_files = list(class_dir.glob("*"))
        image_files = [f for f in image_files if f.is_file()]
        
        # Zamiešanie súborov
        random.shuffle(image_files)
        
        # Výpočet počtu testovacích súborov
        test_count = int(len(image_files) * test_ratio)
        train_count = len(image_files) - test_count
        
        print(f"Trieda {class_name}: {len(image_files)} obrázkov -> {train_count} train, {test_count} test")
        
        # Rozdelenie súborov
        test_files = image_files[:test_count]
        train_files = image_files[test_count:]

        splits[class_name] = (train_files, test_files)
        all_train_counts += train_count

    start_test_index = ((all_train_counts // 100) + 1) * 100 + 1
    test_idx = start_test_index

    for class_name in sorted(splits.keys()):
        train_files, test_files = splits[class_name]
        
        train_class_dir = train_dir / class_name
        for f in train_files:
            new_name = f"{train_idx:03d}.jpg"
            shutil.copy2(f, train_class_dir / new_name)
            train_idx += 1

        test_class_dir = test_dir / class_name
        for f in test_files:
            new_name = f"{test_idx:03d}.jpg"
            shutil.copy2(f, test_class_dir / new_name)
            test_idx += 1   
    
    print(f"\nRozdelenie dokončené!")
    print(f"Trénovacie dáta: {train_dir}")
    print(f"Testovacie dáta: {test_dir}")

# Použitie:
if __name__ == "__main__":
    # Cesty k vašim dátam (GitHub repo: oskarklima/M7DataSP)
    source_directory = "dataset"  # Tu máte bird, car, fish, flower priečinky
    target_directory = "dataset_split"  # Tu sa vytvoria train/test priečinky

    random.seed(0)
    
    # Rozdelenie na 75% train, 25% test
    create_train_test_split(
        source_dir=source_directory,
        target_dir=target_directory,
        test_ratio=0.25,
    )
    
    # Overenie výsledku
    print("\n=== ŠTATISTIKY ===")
    for split in ['train', 'test']:
        split_dir = Path(target_directory) / split
        if split_dir.exists():
            print(f"\n{split.upper()}:")
            for class_dir in split_dir.iterdir():
                if class_dir.is_dir():
                    count = len(list(class_dir.glob("*")))
                    print(f"  {class_dir.name}: {count} obrázkov")
