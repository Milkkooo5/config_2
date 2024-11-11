import zipfile
import xml.etree.ElementTree as ET
import os
import argparse

def extract_nuspec_from_nupkg(nupkg_path):
    with zipfile.ZipFile(nupkg_path, 'r') as zip_ref:
        # Находим все файлы в пакете
        zip_contents = zip_ref.namelist()
        nuspec_file = None
        # Ищем .nuspec файл
        for file_name in zip_contents:
            if file_name.endswith('.nuspec'):
                nuspec_file = file_name
                break

        if nuspec_file is None:
            raise ValueError("Файл .nuspec не найден в пакке .nupkg")

        # Извлекаем .nuspec файл в память
        with zip_ref.open(nuspec_file) as file:
            return file.read()

