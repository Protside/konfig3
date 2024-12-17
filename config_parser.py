import argparse
import re
import toml

class ConfigParser:
    def __init__(self):
        self.constants = {}

    def parse(self, lines):
        for line in lines:
            line = line.strip()
            if line.startswith("const"):
                self._parse_constant(line)
            elif line.startswith(".(") and line.endswith(")."):
                self._parse_constant_expression(line)
            else:
                raise SyntaxError(f"Неизвестная конструкция: {line}")

    def _parse_constant(self, line):
        match = re.match(r'const ([a-z][a-z0-9_]*) = (.+);', line)
        if not match:
            raise SyntaxError(f"Ошибка синтаксиса в строке: {line}")
        name, value = match.groups()
        self.constants[name] = self._parse_value(value)

    def _parse_constant_expression(self, line):
        match = re.match(r'\.\((.+?)\)\.', line)
        if not match:
            raise SyntaxError(f"Ошибка синтаксиса в строке: {line}")
        name = match.group(1)
        if name not in self.constants:
            raise NameError(f"Константа '{name}' не объявлена.")
        return self.constants[name]

    def _parse_value(self, value):
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        elif re.match(r'^\d+$', value):
            return int(value)
        elif value.startswith('(') and value.endswith(')'):
            return self._parse_array(value[1:-1])
        else:
            raise ValueError(f"Неизвестное значение: {value}")

    def _parse_array(self, value):
        items = [self._parse_value(item.strip()) for item in value.split(',')]
        return items

def main():
    parser = argparse.ArgumentParser(description='Конвертер конфигурационного языка в TOML.')
    parser.add_argument('input_file', help='Путь к входному файлу с конфигурацией')
    parser.add_argument('output_file', help='Путь к выходному файлу для TOML')

    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    config_parser = ConfigParser()
    try:
        config_parser.parse(lines)
        with open(args.output_file, 'w', encoding='utf-8') as outfile:
            toml.dump(config_parser.constants, outfile)
        print(f"Конфигурация успешно преобразована в {args.output_file}.")
    except (SyntaxError, NameError, ValueError) as e:
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    main()