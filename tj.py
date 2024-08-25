def teste(valor):
    for i in range(1, valor + 1):
        print('{} ** 2 = {}'.format(i, i**2))

resultado = teste(int(input()))
print(resultado)