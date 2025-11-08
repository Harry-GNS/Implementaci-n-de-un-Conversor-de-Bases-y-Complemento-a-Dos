def convertir_decimal_a_base_entera(numero, base):
    digitos = "0123456789ABCDEF"
    if numero == 0:
        return "0"
    resultado = []
    n = numero
    while n > 0:
        resultado.append(digitos[n % base])
        n //= base
    resultado.reverse()
    return ''.join(resultado)


def convertir_base_a_decimal(cadena, base):
    cadena = cadena.strip().upper()
    valor = 0
    for c in cadena:
        if '0' <= c <= '9':
            d = ord(c) - ord('0')
        else:
            d = ord(c) - ord('A') + 10
        if d >= base:
            raise ValueError('Dígito fuera de rango para la base')
        valor = valor * base + d
    return valor


def complemento_a_dos(numero, bits):
    limite_min = -(1 << (bits - 1))
    limite_max = (1 << (bits - 1)) - 1
    if numero < limite_min or numero > limite_max:
        raise OverflowError('Overflow: no cabe en el número de bits especificado')
    mask = (1 << bits) - 1
    valor = numero & mask
    binario = format(valor, 'b').zfill(bits)
    return binario


def complemento_a_dos_a_decimal(binario_str):
    bits = len(binario_str)
    valor = int(binario_str, 2)
    if binario_str[0] == '0':
        return valor
    else:
        return valor - (1 << bits)


def menu_decimal_a_otras_bases():
    n = int(input('Ingrese un número entero decimal positivo: '))
    if n < 0:
        print('Número debe ser positivo')
        return
    print('Binario:', convertir_decimal_a_base_entera(n, 2))
    print('Octal:', convertir_decimal_a_base_entera(n, 8))
    print('Hexadecimal:', convertir_decimal_a_base_entera(n, 16))


def menu_otras_bases_a_decimal():
    print('Elija la base de entrada: 2-binario, 8-octal, 16-hexadecimal')
    b = int(input('Base: '))
    s = input('Ingrese el número en esa base: ')
    try:
        d = convertir_base_a_decimal(s, b)
        print('Decimal:', d)
    except Exception as e:
        print('Error:', e)


def menu_complemento_a_dos():
    x = int(input('Ingrese número entero (positivo o negativo): '))
    bits = int(input('Ingrese número de bits (ej. 8, 16, 32): '))
    try:
        ca2 = complemento_a_dos(x, bits)
        print(f'Representación Ca2 ({bits} bits):', ca2)
        reconv = complemento_a_dos_a_decimal(ca2)
        print('Reconversión a decimal desde Ca2:', reconv)
    except OverflowError as e:
        print('Error:', e)


def menu_avanzado():
    print('Opciones avanzadas:')
    print('1) Suma y resta en binario (Complemento a 2)')
    print('2) Conversión en coma flotante (no implementado)')
    print('3) Reducción de expresiones booleanas (no implementado)')
    opc = input('Elegir opción (volver con Enter): ')
    if opc == '1':
        a = int(input('Primer sumando (decimal): '))
        b = int(input('Segundo sumando (decimal): '))
        bits = int(input('Bits para la operación: '))
        try:
            ra = complemento_a_dos(a, bits)
            rb = complemento_a_dos(b, bits)
            suma = (a + b)
            ca2suma = complemento_a_dos(suma, bits)
            print('A (Ca2):', ra)
            print('B (Ca2):', rb)
            print('Suma decimal:', suma)
            print('Suma (Ca2) con truncamiento a', bits, 'bits:', ca2suma)
        except OverflowError as e:
            print('Error:', e)


def main():
    while True:
        print('\n--- Conversor de Bases y Complemento a Dos ---')
        print('1) Decimal -> Binario/Octal/Hex')
        print('2) Bin/Oct/Hex -> Decimal')
        print('3) Complemento a Dos (representación y verificación)')
        print('4) Avanzado')
        print('5) Salir')
        opcion = input('Elija una opción: ')
        if opcion == '1':
            menu_decimal_a_otras_bases()
        elif opcion == '2':
            menu_otras_bases_a_decimal()
        elif opcion == '3':
            menu_complemento_a_dos()
        elif opcion == '4':
            menu_avanzado()
        elif opcion == '5':
            print('Saliendo')
            break
        else:
            print('Opción no válida')


if __name__ == '__main__':
    main()
