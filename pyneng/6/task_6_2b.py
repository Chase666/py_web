# -*- coding: utf-8 -*-
"""
Задание 6.2b
Сделать копию скрипта задания 6.2a.
Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.
Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.
Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

while True:
    ip = input("Введите IP адрес: ")
    octets = ip.split(".")
    correct_ip = True

    if len(octets) == 4:
        for octet in octets:
            if not (octet.isdigit() and int(octet) in range(256)):
                correct_ip = False
                break
    else:
        correct_ip = False
    if correct_ip:
        break
    print("Неправильный IP-адрес")

oct1 = int(octets[0])

if 1 <= oct1 <= 223:
    print("unicast")
elif 224 <= oct1 <= 239:
    print("multicast")
elif ip == "0.0.0.0":
    print("unassigned")
elif ip == "255.255.255.255":
    print("local broadcast")
else:
    print("unused")