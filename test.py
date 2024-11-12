import unittest
from unittest.mock import patch, mock_open, MagicMock
from io import BytesIO

# Импортируем тестируемые функции из основного модуля
from mermaid import extract_nuspec_from_nupkg, parse_nuspec_for_dependencies, generate_mermaid_code


class TestNupkgDependencyVisualizer(unittest.TestCase):

    @patch('zipfile.ZipFile')
    def test_extract_nuspec_from_nupkg(self, mock_zipfile):
        # Создаем фиктивный .nuspec файл и добавляем его в архив
        fake_nuspec_content = b'<package></package>'
        mock_zipfile.return_value.__enter__.return_value.namelist.return_value = ['package.nuspec']
        mock_zipfile.return_value.__enter__.return_value.open.return_value = BytesIO(fake_nuspec_content)

        # Проверяем, что функция правильно извлекает содержимое .nuspec файла
        result = extract_nuspec_from_nupkg('test_package.nupkg')
        self.assertEqual(result, fake_nuspec_content)

    def test_parse_nuspec_for_dependencies(self):
        # Определяем содержимое XML с зависимостями
        nuspec_content = b"""
        <package xmlns="http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd">
            <metadata>
                <dependencies>
                    <group targetFramework=".NETFramework4.5">
                        <dependency id="Example.Dependency" version="1.0.0" />
                    </group>
                    <group targetFramework=".NETStandard2.0">
                        <dependency id="Another.Dependency" version="2.0.0" />
                    </group>
                </dependencies>
            </metadata>
        </package>
        """

        # Ожидаемый результат парсинга
        expected_dependencies = [
            {'target_framework': '.NETFramework4.5', 'dependency_id': 'Example.Dependency', 'version': '1.0.0'},
            {'target_framework': '.NETStandard2.0', 'dependency_id': 'Another.Dependency', 'version': '2.0.0'}
        ]

        # Проверяем, что функция правильно парсит зависимости из содержимого .nuspec файла
        result = parse_nuspec_for_dependencies(nuspec_content)
        self.assertEqual(result, expected_dependencies)

    def test_generate_mermaid_code(self):
        # Определяем зависимости для генерации графа
        dependencies = [
            {'target_framework': '.NETFramework4.5', 'dependency_id': 'Example.Dependency', 'version': '1.0.0'},
            {'target_framework': '.NETStandard2.0', 'dependency_id': 'Another.Dependency', 'version': '2.0.0'}
        ]

        # Ожидаемый результат Mermaid кода
        expected_mermaid_code = (
            "graph TD\n"
            "  .NETFramework4.5 -->|Example.Dependency v1.0.0| Example.Dependency\n"
            "  .NETStandard2.0 -->|Another.Dependency v2.0.0| Another.Dependency\n"
        )

        # Проверяем, что функция правильно генерирует код Mermaid для графа зависимостей
        result = generate_mermaid_code(dependencies)
        self.assertEqual(result.strip(), expected_mermaid_code.strip())


if __name__ == '__main__':
    unittest.main()
