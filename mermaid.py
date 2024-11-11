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
def generate_mermaid_code(dependencies):
    mermaid_code = "graph TD\n"
    for dep in dependencies:
        target_framework = dep['target_framework']
        dep_id = dep['dependency_id']
        mermaid_code += f"  {target_framework} -->|{dep_id} v{dep['version']}| {dep_id}\n"
    return mermaid_code
def main():
    # Настроим парсер командной строки
    parser = argparse.ArgumentParser(
        description="Инструмент для визуализации графа зависимостей пакета .nupkg в формате Mermaid")

    # Добавляем необходимые аргументы
    parser.add_argument('graph_tool_path', help="Путь к программе для визуализации графов.")
    parser.add_argument('package_name', help="Имя анализируемого пакета (путь к .nupkg файлу).")
    parser.add_argument('repo_url', help="URL-адрес репозитория для получения зависимостей.")

    # Парсим аргументы командной строки
    args = parser.parse_args()

    nupkg_path = args.package_name
    repo_url = args.repo_url

    # Выводим введенные параметры
    print(f"Путь к инструменту визуализации: {args.graph_tool_path}")
    print(f"Имя пакета: {nupkg_path}")
    print(f"URL-адрес репозитория: {repo_url}")

    # Извлекаем и парсим .nuspec
    try:
        nuspec_content = extract_nuspec_from_nupkg(nupkg_path)
        dependencies = parse_nuspec_for_dependencies(nuspec_content)

        if dependencies:
            print("\nЗависимости пакета:")
            for dep in dependencies:
                print(
                    f"Целевая платформа: {dep['target_framework']}, "
                    f"Зависимость: {dep['dependency_id']}, Версия: {dep['version']}")

            # Генерируем Mermaid код
            mermaid_code = generate_mermaid_code(dependencies)
            print("\nMermaid код для визуализации зависимостей:")
            print(mermaid_code)
        else:
            print("Зависимости не найдены.")

    except Exception as e:
        print(f"Ошибка при извлечении зависимостей: {e}")


if __name__ == '__main__':
    main()
