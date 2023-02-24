# -*- coding: utf-8 -*-
"""
Задание 6.2a
Сделать копию скрипта задания 6.2.
Добавить проверку введенного IP-адреса.
Адрес считается корректно заданным, если он:
   - состоит из 4 чисел (а не букв или других символов)
   - числа разделенны точкой
   - каждое число в диапазоне от 0 до 255
Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.
Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

ip = input("Введите IP адрес: ")
octets = ip.split(".")
correct_ip = True

if len(octets) != 4:
    correct_ip = False
else:
    for o in octets:

        if not (o.isdigit() and int(o) in range(256)):
            correct_ip = False
            break
if correct_ip != True:
    print("Неправильный IP-адрес")
else:
    octets_num = [int(i) for i in octets]
    if octets_num[0] in range(1, 224):
        print("unicast")
    elif octets_num[0] in range(224, 240):
        print("multicast")
    elif ip == "255.255.255.255":
        print("local broadcast")
    elif ip == "0.0.0.0":
        print("unassigned")
    else:
        print("unused")
