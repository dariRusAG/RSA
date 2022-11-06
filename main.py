import math
import random
import sympy


class my_signature_RSA:
    M = None  # исходное сообщение
    S = None  # лист с закодированным исходным сообщением
    C = []  # лист с зашифрованным исходным сообщением

    def generate_keys(self, my_mess):
        self.M = my_mess

        # Перевод каждого символа нашего сообщения через latin-1
        self.S = list(my_mess.encode('latin-1'))
        my_mess_encode = "|".join(map(str, self.S))

        # Запись в общий файл
        with open("general.txt", "w", encoding="utf-8") as file_general:
            file_general.write("Исходное сообщение: " + self.M + "\n" +
                               "Исходное сообщение через кодировку: " + my_mess_encode + "\n\n")

        # Генерация простого числа
        def gen_256():
            a = []
            for i in range(8):
                # Добавляет в массив случайно выбранный элемент из последовательности 0, 1
                a.append(random.choice("01"))
            # Первый элемент и последний присваиваем 1
            a[0] = "1"
            a[-1] = "1"  # устранение четности

            # Возвращает десятичное число, преобразованное из объединенного кортежа элементов двоичного кода
            return int(("".join(a)), 2)

        def get_prime():
            while True:
                # Генерация простого числа
                a = gen_256()
                # Проверка числа на простоту
                if sympy.isprime(a):
                    return a

        def check(p, q):
            if sympy.isprime(p) and \
                    sympy.isprime(q) and \
                    p != q:
                return True
            else:
                return False

        # Генерация целого числа е
        def generate_e(fi):
            for i in range(2, fi):
                # Проверка сгенерированного числа: простое и взаимно простое с fi
                if sympy.isprime(i) and math.gcd(fi, i) == 1:
                    return i

        # Рекурсивная реализация расширенного алгоритма Евклида.
        # Возвращает целые числа x, y и gcd(a, b) для уравнения Безу: ax + by = gcd(a, b)
        def bezout_recursive(a, b):
            if not b:  # если b = 0
                return 1, 0, a
            y, x, g = bezout_recursive(b, a % b)
            return x, y - (a // b) * x, g

        # Автоматическая генерация
        def generate_all_auto():
            while True:
                p = get_prime()
                q = get_prime()
                mod = p * q
                fi = (p - 1) * (q - 1)
                e = generate_e(fi)
                d = bezout_recursive(fi, e)[1]
                if d > 0 and p != q:
                    return p, q, mod, fi, e, d

        # Ручной ввод
        def generate_all():
            while True:
                while True:
                    p = input("p = ")
                    q = input("q = ")
                    if p.isdigit() and q.isdigit():
                        p = int(p)
                        q = int(q)
                        if check(p, q):
                            break
                print("Выход из генерации p и q" + "\n")
                mod = p * q
                fi = (p - 1) * (q - 1)
                e = generate_e(fi)
                d = bezout_recursive(fi, e)[1]
                if d > 0:
                    return p, q, mod, fi, e, d

        while True:
            var = input("p и q: 1 - автоматическая генерация. 2 - самостоятельно добавить: ")
            if var == "1":
                p, q, mod, fi, e, d = generate_all_auto()
                break
            elif var == "2":
                p, q, mod, fi, e, d = generate_all()
                break
            else:
                print("Нет такой команды")

        with open("public_key", "w", encoding="utf-8") as file:
            file.write(str(mod) + "," + str(e))

        with open("private_key", "w", encoding="utf-8") as file:
            file.write(str(mod) + "," + str(d))

        with open("all_data", "w", encoding="utf-8") as file:
            file.write("p: " + str(p) + "\n" +
                       "q: " + str(q) + "\n" +
                       "mod: " + str(mod) + "\n" +
                       "fi: " + str(fi) + "\n" +
                       "e: " + str(e) + "\n" +
                       "d: " + str(d))

    # Шифрование сообщения с помощью ключей
    def encoding(self):
        # Открываем файл с открытым ключом
        with open("public_key", "r", encoding="utf-8") as file:
            for line in file:
                line = [int(i) for i in line.split(",")]

        # Шифрование сообщения
        for i in range(len(self.S)):
            self.C.append((self.S[i] ** line[1]) % line[0])

        # Запись зашифрованного сообщения в общий файл
        my_mess_encode = "|".join(map(str, self.C))
        with open("general.txt", "a+", encoding="utf=8") as file_gen:
            file_gen.write("Зашифрованное сообщение: " + my_mess_encode + "\n")

    # Дешифрование сообщения с помощью ключей
    def decoding(self):
        # Открываем файл с закрытым ключом
        with open("private_key", "r", encoding="utf-8") as file:
            for line in file:
                line = [int(i) for i in line.split(",")]

        # Дешифрование сообщение
        for i in range(len(self.C)):
            self.S[i] = (self.C[i] ** line[1]) % line[0]

        # Запись дешифрованного сообщения в общий файл
        my_mess_decode = "".join(map(str, list(bytes(self.S).decode('utf-8'))))
        with open("general.txt", "a+", encoding="utf=8") as file_gen:
            file_gen.write("Дешифрованное сообщение: " + my_mess_decode + "\n\n")

            # Проверка подлинности
            if my_mess_decode == self.M:
                file_gen.write("RSA сработал правильно. Сообщения идентичны")
            else:
                file_gen.write("RSA сработал неправильно")


if __name__ == '__main__':
    cipher = my_signature_RSA()

    # Генерация ключей
    cipher.generate_keys("as d12.,GH!@l-PPP0")
    # cipher.generate_keys("aAaAaA")
    # cipher.generate_keys("          ")

    # Кодирование сообщения
    cipher.encoding()

    # Декодирование сообщения
    cipher.decoding()
