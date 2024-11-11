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

def parse_nuspec_for_dependencies(nuspec_content):
    # Загружаем XML с учетом пространства имен
    namespaces = {'ns': 'http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd'}
    root = ET.fromstring(nuspec_content)

    dependencies = []

    # Ищем все группы зависимостей в <ns0:dependencies>
    for group in root.findall('.//ns:dependencies/ns:group', namespaces):
        target_framework = group.get('targetFramework')
        for dep in group.findall('ns:dependency', namespaces):
            dep_id = dep.get('id')
            dep_version = dep.get('version')
            dependencies.append({
                'target_framework': target_framework,
                'dependency_id': dep_id,
                'version': dep_version
            })

    return dependencies
