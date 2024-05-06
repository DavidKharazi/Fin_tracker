import os
import datetime

class FinanceTracker:
    def __init__(self, filename):
        self.filename = filename

    def display_balance(self):
        # Выводим текущий баланс, общий доход и общий расход.
        incomes, expenses = self._read_data()
        total_income = sum(float(record['Сумма']) for record in incomes)
        total_expense = sum(float(record['Сумма']) for record in expenses)
        balance = total_income - total_expense
        print(f"Общий баланс: {balance}")
        print(f"Общий доход: {total_income}")
        print(f"Общий расход: {total_expense}")

    def add_record(self):
        #Добавляем новую запись о доходе или расходе.
        category = input("Выберите категорию (Доход/Расход): ").capitalize()
        amount = float(input("Сумму: "))
        description = input("Описание: ")
        date = datetime.date.today()
        with open(self.filename, 'a', encoding='utf-8') as file:
            file.write(f"Дата: {date}\n")
            file.write(f"Категория: {category}\n")
            file.write(f"Сумма: {amount}\n")
            file.write(f"Описание: {description}\n\n")

    def edit_record(self):
        #Редактируем существующую запись о доходе или расходе.
        incomes, expenses = self._read_data()
        all_records = incomes + expenses
        if not all_records:
            print("Нет записей для редактирования.")
            return
        print("Список записей:")
        for i, record in enumerate(all_records):
            print(f"{i}. {record['Дата']} - {record['Категория']} - {record['Сумма']} - {record['Описание']}")
        index = int(input("Введите номер записи, которую хотите отредактировать: "))
        if index < 0 or index >= len(all_records):
            print("Неверный индекс.")
            return
        record_to_edit = all_records[index]
        category = input("Введите новую категорию (Доход/Расход), или нажмите Enter для оставления без изменений: ").capitalize()
        amount = input("Введите новую сумму, или нажмите Enter для оставления без изменений: ")
        description = input("Введите новое описание, или нажмите Enter для оставления без изменений: ")
        date = input("Введите новую дату (гггг-мм-дд), или нажмите Enter для оставления без изменений: ")
        if category:
            record_to_edit['Категория'] = category
        if amount:
            record_to_edit['Сумма'] = amount
        if description:
            record_to_edit['Описание'] = description
        if date:
            try:
                datetime.datetime.strptime(date, "%Y-%m-%d")
                record_to_edit['Дата'] = date
            except ValueError:
                print("Неверный формат даты.")
                return
        all_records[index] = record_to_edit
        self._rewrite_data(all_records)
        print("Запись успешно отредактирована.")

    def search_records(self):
        #Поиск записей по категории, дате или сумме.
        incomes, expenses = self._read_data()
        all_records = incomes + expenses
        if not all_records:
            print("Нет записей для поиска.")
            return
        print("Выберите критерий поиска:")
        print("1. По категории")
        print("2. По дате")
        print("3. По сумме")
        choice = input("Введите номер критерия: ")
        if choice == '1':
            category = input("Введите категорию (Доход/Расход): ").capitalize()
            found_records = [record for record in all_records if record['Категория'] == category]
        elif choice == '2':
            date_str = input("Введите дату (гггг-мм-дд): ")
            try:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                found_records = [record for record in all_records if record['Дата'] == str(date)]
            except ValueError:
                print("Неверный формат даты.")
                return
        elif choice == '3':
            amount = input("Введите сумму: ")
            found_records = [record for record in all_records if record['Сумма'] == amount]
        else:
            print("Неверный выбор.")
            return
        if found_records:
            print("Найденные записи:")
            for record in found_records:
                print(f"{record['Дата']} - {record['Категория']} - {record['Сумма']} - {record['Описание']}")
        else:
            print("Записи не найдены.")

    def _read_data(self):
        # Читаем данные из файла и возвращаем два списка: доходы и расходы.
        incomes = []
        expenses = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                record = {}
                for line in lines:
                    if line.strip() == '':
                        if record:
                            if record['Категория'] == 'Доход':
                                incomes.append(record)
                            elif record['Категория'] == 'Расход':
                                expenses.append(record)
                            record = {}
                    else:
                        key, value = line.strip().split(': ')
                        record[key] = value
                if record:  # Adding the last record if it exists
                    if record['Категория'] == 'Доход':
                        incomes.append(record)
                    elif record['Категория'] == 'Расход':
                        expenses.append(record)
        return incomes, expenses

    def _rewrite_data(self, records):
        # Перезаписываем данные в файл.
        with open(self.filename, 'w', encoding='utf-8') as file:
            for record in records:
                for key, value in record.items():
                    file.write(f"{key}: {value}\n")
                file.write('\n')

if __name__ == "__main__":
    tracker = FinanceTracker("finance_data.txt")

    while True:
        print("\n1. Показать текущий баланс")
        print("2. Добавление новой записи о доходе или расходе")
        print("3. Редактирование существующих записей о доходах и расходах")
        print("4. Поиск записей по категории, дате или сумме")
        print("5. Завершить")
        choice = input("Выберите пункт: ")

        if choice == '1':
            tracker.display_balance()
        elif choice == '2':
            tracker.add_record()
        elif choice == '3':
            tracker.edit_record()
        elif choice == '4':
            tracker.search_records()
        elif choice == '5':
            break
        else:
            print("Неверный выбор, попробуйте еще.")
