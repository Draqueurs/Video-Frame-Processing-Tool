import os
import argparse

def rename_files_with_pattern(folder_path):
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print(f"Le dossier spécifié n'existe pas : {folder_path}")
        return

    file_list = os.listdir(folder_path)
    index = 1

    for filename in file_list:
        new_filename = f'{index}_'+'_'.join(filename.split('_')[1:])    
        source_path = os.path.join(folder_path, filename)
        destination_path = os.path.join(folder_path, new_filename)
        os.rename(source_path, destination_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Renomme tous les fichiers d'un dossier avec un pattern donné.")
    parser.add_argument("dossier", help="Chemin vers le dossier contenant les fichiers à renommer.")
    args = parser.parse_args()

    # Appel de la fonction de renommage des fichiers
    rename_files_with_pattern(args.dossier)
