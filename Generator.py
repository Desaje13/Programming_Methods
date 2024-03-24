import csv
import random


def generate_employee():
    first_names = ["Иван", "Пётр", "Алексей", "Сергей", "Михаил", "Александр"]
    last_names = ["Иванов", "Петров", "Сидоров", "Смирнов", "Кузнецов", "Волков"]
    positions = ["бухгалтер-стажёр", "помощник бухгалтера", "бухгалтер", "старший бухгалтер", "ведущий бухгалтер",
                 "главный бухгалтер"]
    department = ["линейная", "по вертикали", "комбинированная"]

    full_name = random.choice(first_names) + " " + random.choice(last_names)
    position = random.choice(positions)
    departament = random.choice(department)
    salary = random.randint(10000, 100000)

    return [full_name, position, departament, salary]


def generate_csv(filename, num_records):
    with open(filename, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Имя", "Должность", "Подразделение", "Зарплата"])

        for _ in range(num_records):
            employee_data = generate_employee()
            writer.writerow(employee_data)

    file.close()


generate_csv('Data_1.csv', 100)
generate_csv('Data_2.csv', 1000)
generate_csv('Data_3.csv', 10000)
generate_csv('Data_4.csv', 20000)
generate_csv('Data_5.csv', 30000)
generate_csv('Data_6.csv', 50000)
generate_csv('Data_7.csv', 100000)
