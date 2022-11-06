# Импортирование библиотек
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import os

""" 
Дано:
# A = 1.34941
# x = [-10; 10]
f(x)=-0.0001(|sin(x)*sin(A)*exp(|100-(sqrt(x**2+A**2)/pi)|)|+1)**0.1
"""

A = 1.34941

# Функции для упрощения записи
def sqrt(a):
    if a >= 0:
        return np.sqrt(a)

def abs(a):
    return np.abs(a)

def sin(a):
    return np.sin(a)   

def e(a):
    return np.exp(a)

def func(x):
    return -0.0001 * (abs(sin(x) * sin(A) * e(abs(100 - sqrt(x**2 + A**2) / np.pi))) + 1)**0.1

# Пустые списки
xs = []
ys = []

for x in range(-10, 10, 1):

    # f(x)
    y = func(x)

    # Добавление элемментов в списки
    xs.append(x)
    ys.append(y)

    # Для проверки
    #print(x)
    #print(y)


# Создание XML файла
if __name__ == '__main__':

    # Создание главного элемента
    root = ET.Element('data')

    # Создание подэлементов
    for i in range(len(xs)):
        row = ET.SubElement(root, 'row')
        x = ET.SubElement(row, 'x').text = str(xs[i])
        y = ET.SubElement(row, 'y').text = str(ys[i])
  
    # Создание директории если её нет 
    d = os.path.dirname(__file__) # директория скрипта
    p = r'{}/results'.format(d) # создание path

    try:
        os.makedirs(p)
    except OSError:
        pass

    # Сохранение файла XML
    tree = ET.ElementTree(root)
    tree.write('results/results.xml', encoding='utf-8')

# Построение графика    
if __name__ == '__main__':
    # Интервал изменения переменной по оси X
    xmin = -10.0
    xmax = 10.0

    # Количество отсчетов на заданном интервале
    count = 200

    # !!! Создадим список координат по оси X на отрезке [-xmin; xmax], включая концы
    xlist = np.linspace(xmin, xmax, count)

    # Вычислим значение функции в заданных точках
    ylist = [func(x) for x in xlist]

    # !!! Нарисуем одномерный график
    plt.plot(xlist, ylist)

    # Название осей
    plt.xlabel('x')
    plt.ylabel('f(x)')

    # Сетка
    plt.grid()
    
    # !!! Покажем окно с нарисованным графиком
    plt.show()