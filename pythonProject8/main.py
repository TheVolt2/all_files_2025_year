# def createGreetings(names):
#      print("С новым годом", names, "!")
#
# names = ["Анна", "Иван", "Олег"]
# for i in range(len(names)):
#      createGreetings(names[i])


sirius = "*"
space = ' '
vusota = int(input("Введите высоту:")) * 2
iu = vusota

for i in range(vusota + 1):
    a = i
    b = a % 2
    iu -= 1
    ic = i/2
    space_sirius = space + sirius
    space_sirius_ic = i * space_sirius
    if b != 0:
        print(int(iu) * space + space_sirius_ic)
    else:
        None

# a = 0
# b = 0
# c = 0
#
# podarki = int(input("Введите подарки:"))
#
# podarki_nacelo = podarki % 3
#
# a = podarki // 3 + podarki_nacelo
# b = podarki // 3
# c = podarki // 3
#
# name_a = input("Введите имя")
# name_b = input("Введите имя")
# name_c = input("Введите имя")
#
# slovar = {name_a: a, name_b: b, name_c: c}
#
# print(slovar)

# def validateGiftIds(giftIds):
#     if giftIds[0] == giftIds[1]:
#         print(giftIds[0])
#     if giftIds[0] == giftIds[2]:
#         print(giftIds[0])
#     if giftIds[0] == giftIds[3]:
#         print(giftIds[0])
#
#     if giftIds[1] == giftIds[2]:
#         print(giftIds[1])
#     if giftIds[1] == giftIds[3]:
#         print(giftIds[1])
#     if giftIds[2] == giftIds[3]:
#         print(giftIds[2])
#
#
# giftIds = ["ID234", "ID234", "ID123", "ID345"]
# print(validateGiftIds(giftIds))
