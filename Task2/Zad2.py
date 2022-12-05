""" 
Расчет зависимости эффективной площади рассеяния (ЭПР)идеально проводящей
сферы от частоты.
Построить график зависимости ЭПР от частоты.
Результат сохранить в текстовый файл формата CSV
"""

# Импортирование библиотек
import re
import matplotlib.pyplot as plt
import numpy as np
import requests
from scipy import special as sp
import csv

#Формулы и обозначения по заданию
"""
sigma = lambda**2/pi*(|Σ(((-1)**n)*(n+0.5)*(bn - an))|**2)

an = jn(kr)/hn(kr)

bn = (kr*jn-1(kr)-n*jn(kr))/(kr*hn-1(kr)-n*hn(kr))

hn(x) = jn(x) + iyn(x)

• k — волновое число.
• l — длина волны.
• r — радиус сферы.
• jn(x) и yn(x) — сферические функции Бесселя первого и второго рода
соответственно порядка n.
• i — мнимая единица.
• hn(x) — сферическая функция Бесселя третьего рода.
"""

if __name__ == '__main__':
    # Скачивание файла с исходными данными
    link = 'https://jenyay.net/uploads/Student/Modelling/task_02_02.txt'
    filename = link.split('/')[-1] # Присваиваем имя файла из его ссылки
    web = requests.get(link) # Записывает в "web" данные из файла по ссылке
    file = open(filename, 'wb').write(web.content) # Создает и записывает файл

    # Вывод нужного варианта и присвоение значений
    in_file = web.text # Присвоение текста содержащегося в файле

    file = open(filename, 'r', encoding='utf-8') # Открытие файла для прочтения
    print (file.read()) # Чтение файла

    # Паттерн для поиска по тексту файла
    reg = r"(\b6)\s+(\d+e-\d+|\d+\.\d+)\s+(\d+e\d+|\d+\.\d+e\d+)\s+(\d+e\d+)"
    matches = re.search(reg, in_file, re.MULTILINE) # Поиск по паттерну

    file.close() # Закрытие файла

    # ПРОВЕРКА !!!
    #print (matches.group(0))
    #print(D, fmin, fmax)

    # Присвоение значений из файла под нужным вариантом
    D = float(matches.group(2))
    fmin = float(matches.group(3))
    fmax = float(matches.group(4))
    
    r = D / 2
    c = 3*10**8

    # Функции для упрощения записи
    def hn(n, x):
        return (sp.jn(n, x) + 1j*sp.yn(n, x))

    def an(n, x):
        return (sp.jn(n, x) / hn(n, x))
    
    def bn(n, x):
        return ((k*r*sp.jn(n-1, x) - n*sp.jn(n,x)) /
                            (k*r*hn(n-1, x) - n*hn(n,x)))

    # Расчет значений
    f = np.linspace(fmin, fmax, 2500)
    lambda_ = c / f
    k = 2*np.pi / lambda_
    
    # Расчет суммы
    s = 0
    for n in range(1, 1000, 1):
        if all((-1)**n * (n + 0.5) * (bn(n, k*r) - an(n, k*r))) >= 10e-12:
            s += ((-1)**n * (n + 0.5) * (bn(n, k*r) - an(n, k*r)))
            #print(s)
        else:
            break

    sigma = ((lambda_**2/np.pi) * (np.abs(s))**2)
    
    #!!!Для наглядности можно вывести в консоль
    #print (f)
    #print (lambda_)
    #print (k)
    #print(sigma)

    # Вывод файла
    """
    !!!ДЛЯ ПОНИМАНИЯ ВЫВОДА ФАЙЛА!!!

    csv.DictWriter: 
        создает объект, который работает как csv.writer(),
        но позволяет передавать строку с данными на запись как словарь,
        ключи которой задаются необязательным параметром fieldnames
    
    join: 
        Отвечает за объединение списка строк с помощью определенного указателя

    split():
        Разбивает строку по указанному разделителю и возвращает список строк
    
    writer.writeheader():
        Доступен только в экземпляру класса класса csv.DictWriter().
        Записывает строку с именами полей, как указано в конструкторе
    
    """

    lines = ""
    with open("result.csv",mode = "w", encoding='utf-8') as file:
        filednames = ['№', 'Длина волны,м', 'Частота,Гц', 'ЭПР,м^2']
        writer = csv.DictWriter(file, fieldnames = filednames)
        writer.writeheader()
        writer.writerows([{'№':i+1, 'Длина волны,м':lambda_[i],
            'Частота,Гц':f[i],'ЭПР,м^2':sigma[i]} for i in range(len(sigma))])

    with open("result.csv", mode="r", encoding='utf-8') as file:
        for line in file:
            lines+= " ".join(line.split('\n'))
            lines = lines.replace("  ",'\n')

    with open("result.csv", mode="w", encoding='utf-8') as file:
            for line in lines:
                    file.write(line)

# Построение графика    
if __name__ == '__main__':
    # Интервал изменения переменной по оси X
    xmin = 0.0
    xmax = 100.0

    # Количество отсчетов на заданном интервале
    count = 200

    # !!! Нарисуем одномерный график
    plt.plot(f, sigma)

    # Название осей
    plt.xlabel("$f$,Гц")
    plt.ylabel("$σ$,м^2")

    # Сетка
    plt.grid()
    
    # !!! Покажем окно с нарисованным графиком
    plt.show()