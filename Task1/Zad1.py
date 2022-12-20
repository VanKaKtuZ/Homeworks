# Импортирование библиотек
import numpy as np
from numpy import sin, sqrt, abs, exp, pi
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

# Функция
def func(x):
    return -0.0001 * (abs(sin(x) * sin(A) * exp(abs(100 - sqrt(x**2 + A**2) /
                                                             pi))) + 1)**0.1

if __name__ == '__main__':
    # Пустые списки
    xs = []
    ys = []

    for x in np.arange(-10, 10, 0.001):
        # f(x)
        y = func(x)

        # Добавление элемментов в списки
        xs.append(x)
        ys.append(y)

        # Для проверки
        #print(x)
        #print(y)


    # Создание XML файла

    # Создание главного элемента
    root = ET.Element('data')

    # Создание подэлементов
    for i in range(len(xs)):
        row = ET.SubElement(root, 'row')
        x = ET.SubElement(row, 'x').text = str(xs[i])
        y = ET.SubElement(row, 'y').text = str(ys[i])
  
    # Создание директории если её нет 
    d = os.path.dirname(__file__) # директория скрипта
    p = r'{}/results'.format(d) # создание path (пути)

    try:
        os.makedirs(p)
    except OSError:
        pass

    # Сохранение файла XML
    tree = ET.ElementTree(root)
    tree.write('results/results.xml', encoding='utf-8', xml_declaration = True)

    # Построение графика    

    # !!! Нарисуем одномерный график
    plt.plot(xs, ys)

    # Название осей
    plt.xlabel('x')
    plt.ylabel('f(x)')

    # Сетка
    plt.grid()
    
    # !!! Покажем окно с нарисованным графиком
    plt.show()