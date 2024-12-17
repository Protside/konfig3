import unittest

from config_parser import ConfigParser

class TestConfigParser(unittest.TestCase):
    def setUp(self):
        self.parser = ConfigParser()

    def test_web_server_config(self):
        config_lines = [
            'const server_name = "my_server";',
            'const port = 8080;',
            'const allowed_ips = ("192.168.1.1", "192.168.1.2");'
        ]
        self.parser.parse(config_lines)
        self.assertEqual(self.parser.constants['server_name'], "my_server")
        self.assertEqual(self.parser.constants['port'], 8080)
        self.assertEqual(self.parser.constants['allowed_ips'], ["192.168.1.1", "192.168.1.2"])

    def test_database_config(self):
        config_lines = [
            'const db_name = "my_database";',
            'const db_user = "admin";',
            'const db_password = "secret";',
            'const db_hosts = ("localhost", "192.168.1.10");'
        ]
        self.parser.parse(config_lines)
        self.assertEqual(self.parser.constants['db_name'], "my_database")
        self.assertEqual(self.parser.constants['db_user'], "admin")
        self.assertEqual(self.parser.constants['db_password'], "secret")
        self.assertEqual(self.parser.constants['db_hosts'], ["localhost", "192.168.1.10"])

    def test_application_config(self):
        config_lines = [
            'const app_name = "MyApp";',
            'const version = "1.0.0";',
            'const features = ("feature1", "feature2", "feature3");'
        ]
        self.parser.parse(config_lines)
        self.assertEqual(self.parser.constants['app_name'], "MyApp")
        self.assertEqual(self.parser.constants['version'], "1.0.0")
        self.assertEqual(self.parser.constants['features'], ["feature1", "feature2", "feature3"])

    def test_syntax_error(self):
        with self.assertRaises(SyntaxError):
            self.parser.parse(['const name "John";'])  # Ошибка синтаксиса

    def test_name_error(self):
        self.parser.parse(['const name = "John";'])
        with self.assertRaises(NameError):
            self.parser._parse_constant_expression('.(undefined_name).')  # Необъявленная константа

    def test_value_error(self):
        with self.assertRaises(ValueError):
            self.parser.parse(['const invalid = {1, 2, 3};'])  # Неизвестное значение

if __name__ == '__main__':
    unittest.main()