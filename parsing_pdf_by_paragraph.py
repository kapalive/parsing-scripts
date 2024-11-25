import re
import pdfplumber
import csv

def parse_pdf(file_path):
    data = []
    # Шаблоны для каждого уровня
    pattern_main = re.compile(r'^[A-Z]\d{2} .+')
    pattern_sub = re.compile(r'^[A-Z]\d{2}\.\d .+')
    pattern_sub_sub = re.compile(r'^[A-Z]\d{2}\.\d{2} .+')
    pattern_sub_sub_sub = re.compile(r'^[A-Z]\d{2}\.\d{3} .+')
    pattern_sub_sub_sub_sub = re.compile(r'^[A-Z]\d{2}\.\d{4} .+')  # Новый шаблон для 6 уровня

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')

            for line in lines:
                # Определение уровня кода и сохранение соответствующего типа
                if pattern_main.match(line):
                    parts = line.split(' ', 1)
                    if len(parts) == 2:
                        code, title = parts
                        data.append((code.strip(), title.strip(), 'level_2'))

                elif pattern_sub.match(line):
                    parts = line.split(' ', 1)
                    if len(parts) == 2:
                        code, title = parts
                        data.append((code.strip(), title.strip(), 'level_3'))

                elif pattern_sub_sub.match(line):
                    parts = line.split(' ', 1)
                    if len(parts) == 2:
                        code, title = parts
                        data.append((code.strip(), title.strip(), 'level_4'))

                elif pattern_sub_sub_sub.match(line):
                    parts = line.split(' ', 1)
                    if len(parts) == 2:
                        code, title = parts
                        data.append((code.strip(), title.strip(), 'level_5'))

                elif pattern_sub_sub_sub_sub.match(line):  # Проверка на 6 уровень
                    parts = line.split(' ', 1)
                    if len(parts) == 2:
                        code, title = parts
                        data.append((code.strip(), title.strip(), 'level_6'))

    return data

# Использование функции для парсинга
file_path = '/content/icd10cm-tabular-p-2021.pdf'
data = parse_pdf(file_path)

# Сохранение всех данных в CSV
output_file = '/content/extracted_groups_and_subs.csv'
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Code", "Title", "Type"])  # Заголовки столбцов
    writer.writerows(data)

print(f"Все данные успешно сохранены в файл: {output_file}")
