import pandas as pd
import sqlite3

# Подключение к базе данных SQLite
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Замените 'your_excel_file.xlsx' на имя вашего Excel-файла
excel_file = '../templates/fn/upload_excel.xlsx'

# Замените 'table_name' на имя таблицы, в которую вы хотите импортировать данные
table_name = 'fn_replacement_schedule'

# Чтение данных из Excel-файла в объект DataFrame
df = pd.read_excel(excel_file)

# Создание таблицы в базе данных SQLite и импорт данных
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Закрытие соединения с базой данных
conn.close()

print(f'Data from {excel_file} imported into {table_name} in the SQLite database.')
