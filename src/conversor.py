import sys
import time


def type_print(text, delay=0.02):
    for ch in str(text):
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()


def print_menu_box(title, options, pause=0.52):
    time.sleep(pause)
    width = max(len(title), *(len(o) for o in options)) + 6
    top = '+' + '-' * (width - 2) + '+'
    
    print(top)
    print('| ' + title.center(width - 4) + ' |')
    print('+' + '=' * (width - 2) + '+')
    for o in options:
        print('| ' + o.ljust(width - 4) + ' |')
    print(top)


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
    while True:
        entrada = input('Ingrese un número entero decimal positivo: ')
        try:
            n = int(entrada)
            if n < 0:
                print('Número debe ser positivo')
                print('1) Reintentar')
                print('2) Volver al menú principal')
                ele = input('Elija una opción: ')
                if ele == '1' or ele == '':
                    continue
                else:
                    return
            break
        except ValueError:
            print('Entrada no válida')
            print('1) Reintentar')
            print('2) Volver al menú principal')
            ele = input('Elija una opción: ')
            if ele == '1' or ele == '':
                continue
            else:
                return
    while True:
        print_menu_box(f'Convertir {n} a', ['1) Binario', '2) Octal', '3) Hexadecimal', '4) Todos', '5) Volver'])
        op = input('Elija una opción: ')
        if op == '1':
            type_print('Binario: ' + convertir_decimal_a_base_entera(n, 2))
            accion = post_conversion_menu()
        elif op == '2':
            type_print('Octal: ' + convertir_decimal_a_base_entera(n, 8))
            accion = post_conversion_menu()
        elif op == '3':
            type_print('Hexadecimal: ' + convertir_decimal_a_base_entera(n, 16))
            accion = post_conversion_menu()
        elif op == '4' or op == '':
            type_print('Binario: ' + convertir_decimal_a_base_entera(n, 2))
            type_print('Octal: ' + convertir_decimal_a_base_entera(n, 8))
            type_print('Hexadecimal: ' + convertir_decimal_a_base_entera(n, 16))
            accion = post_conversion_menu()
        elif op == '5':
            break
        else:
            print('Opción no válida')
            continue

        if accion == 'submenu':
            continue
        elif accion == 'main':
            break
        elif accion == 'exit':
            sys.exit(0)


def post_conversion_menu():
    print_menu_box('Qué desea hacer ahora', ['1) Volver al submenú', '2) Volver al menú principal', '3) Salir del programa'])
    elec = input('Elija una opción: ')
    if elec == '1' or elec == '':
        return 'submenu'
    elif elec == '2':
        return 'main'
    elif elec == '3':
        return 'exit'
    else:
        print('Opción no válida, volviendo al submenú')
        return 'submenu'


def menu_otras_bases_a_decimal():
    while True:
        print_menu_box('Convertir a decimal desde', ['1) Binario (base 2)', '2) Octal (base 8)', '3) Hexadecimal (base 16)', '4) Volver'])
        opcion = input('Elija una opción: ')
        if opcion == '1':
            base = 2
        elif opcion == '2':
            base = 8
        elif opcion == '3':
            base = 16
        elif opcion == '4' or opcion == '':
            return
        else:
            print('Opción no válida')
            continue

        # pedir número en la base seleccionada
        while True:
            s = input(f'Ingrese el número en base {base}: ')
            try:
                d = convertir_base_a_decimal(s, base)
                type_print('Decimal: ' + str(d))
            except Exception as e:
                print('Error:', e)
                print('1) Reintentar')
                print('2) Volver al submenú')
                ele = input('Elija una opción: ')
                if ele == '1' or ele == '':
                    continue
                else:
                    break

            accion = post_conversion_menu()
            if accion == 'submenu':
                break
            elif accion == 'main':
                return
            elif accion == 'exit':
                sys.exit(0)


def menu_complemento_a_dos():
    while True:
        x_str = input('Ingrese número entero (positivo o negativo): ')
        try:
            x = int(x_str)
        except Exception:
            print('Entrada no válida')
            print('1) Reintentar')
            print('2) Volver al menú principal')
            ele = input('Elija una opción: ')
            if ele == '1' or ele == '':
                continue
            else:
                return

        bits_str = input('Ingrese número de bits (ej. 8, 16, 32): ')
        try:
            bits = int(bits_str)
            if bits <= 0:
                raise ValueError()
        except Exception:
            print('Bits inválidos')
            print('1) Reintentar')
            print('2) Volver al menú principal')
            ele = input('Elija una opción: ')
            if ele == '1' or ele == '':
                continue
            else:
                return

        try:
            ca2 = complemento_a_dos(x, bits)
            type_print(f'Representación Ca2 ({bits} bits): {ca2}')
            reconv = complemento_a_dos_a_decimal(ca2)
            type_print('Reconversión a decimal desde Ca2: ' + str(reconv))
        except OverflowError as e:
            print('Error:', e)
            print('1) Reintentar')
            print('2) Volver al menú principal')
            ele = input('Elija una opción: ')
            if ele == '1' or ele == '':
                continue
            else:
                return

        accion = post_conversion_menu()
        if accion == 'submenu':
            continue
        elif accion == 'main':
            return
        elif accion == 'exit':
            sys.exit(0)


def menu_avanzado():
    print_menu_box('Opciones avanzadas', ['1) Suma y resta en binario (Complemento a 2)', '2) Conversión en coma flotante (no implementado)', '3) Reducción de expresiones booleanas (no implementado)'])
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
        print_menu_box('Conversor de Bases y Complemento a Dos', ['1) Decimal -> Binario/Octal/Hex', '2) Bin/Oct/Hex -> Decimal', '3) Complemento a Dos (representación y verificación)', '4) Avanzado', '5) Salir'])
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
