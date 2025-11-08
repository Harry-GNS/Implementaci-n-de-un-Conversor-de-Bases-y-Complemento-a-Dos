import sys
import time

# Configuración de animaciones
ANIMATE_TITLES = True
TITLE_DELAY = 0.02


def type_print(text, delay=0.02, end=True):
    for ch in str(text):
        print(ch, end='', flush=True)
        time.sleep(delay)
    if end:
        print()


def print_menu_box(title, options, pause=0.22):
    print()
    time.sleep(pause)
    width = max(len(title), *(len(o) for o in options))

    # título animado opcional (sin caja ASCII)
    if ANIMATE_TITLES:
        type_print(title.center(width), delay=TITLE_DELAY)
    else:
        print(title.center(width))

    # opciones (sin animación)
    print()
    for o in options:
        print(o)
    print()


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


def ca2_to_decimal_invert(ca2_str):
    """Convertir Ca2 a decimal usando el método invertir+1 para negativos."""
    if ca2_str[0] == '0':
        return int(ca2_str, 2)
    inv = ''.join('1' if b == '0' else '0' for b in ca2_str)
    mag = int(inv, 2) + 1
    return -mag


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
            limite_min = -(1 << (bits - 1))
            limite_max = (1 << (bits - 1)) - 1
            if x < limite_min or x > limite_max:
                raise OverflowError('Overflow: no cabe en el número de bits especificado')

            mask = (1 << bits) - 1

            if x >= 0:
                bin_padded = format(x, 'b').zfill(bits)
                type_print(f'Número positivo. Binario ({bits} bits): {bin_padded}')
                ca2 = bin_padded
            else:
                abs_val = abs(x)
                abs_bin = format(abs_val, 'b')
                if len(abs_bin) > bits:
                    raise OverflowError('Overflow: valor absoluto demasiado grande para los bits')
                abs_bin_padded = abs_bin.zfill(bits)
                type_print(f'Valor absoluto |X| en binario (relleno a {bits} bits): {abs_bin_padded}')
                # complemento a uno
                c1 = ''.join('1' if b == '0' else '0' for b in abs_bin_padded)
                type_print(f'Complemento a uno (C1): {c1}')
                # sumar 1
                suma = (int(c1, 2) + 1) & mask
                ca2 = format(suma, 'b').zfill(bits)
                type_print(f'Sumar 1 al C1 -> Complemento a dos (Ca2): {ca2}')

            # Verificación / reconversión mostrando el proceso
            type_print('')
            type_print('--- Verificación: revertir Ca2 a decimal ---')
            type_print(f'Ca2 actual: {ca2}')
            if ca2[0] == '0':
                reconv = int(ca2, 2)
                type_print('Bit de signo 0 -> número positivo')
                # mostrar proceso de expansión polinómica (dígito * base^posición)
                type_print('Proceso (expansión polinómica):')
                contribs = []
                total = 0
                # mostrar desde LSB (posición 0) hasta MSB
                for i, bit in enumerate(reversed(ca2)):
                    if bit == '1':
                        val = 1 << i
                        contribs.append(f'1 * 2^{i} = {val}')
                        total += val
                    else:
                        contribs.append(f'0 * 2^{i} = 0')
                # imprimir algunas contribuciones (no todas si son muchas)
                max_show = 8
                if len(contribs) <= max_show:
                    for c in contribs:
                        type_print('  ' + c)
                else:
                    # mostrar las últimas y las primeras para no ser muy verboso
                    for c in contribs[:4]:
                        type_print('  ' + c)
                    type_print('  ...')
                    for c in contribs[-4:]:
                        type_print('  ' + c)

                type_print('Suma de contribuciones = ' + str(total))
                type_print('Decimal reconvertido: ' + str(reconv))
            else:
                type_print('Bit de signo 1 -> número negativo')
                # método elegido: invertir y sumar 1 para obtener la magnitud
                inv = ''.join('1' if b == '0' else '0' for b in ca2)
                type_print('Invertir bits (C1 de Ca2): ' + inv)
                mag = int(inv, 2) + 1
                type_print('Sumar 1 al C1 para obtener |X|: ' + str(mag))
                type_print('Decimal reconvertido: -' + str(mag))
                # resumen corto (solo mostrar la magnitud negativa calculada)
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
    # Mantener el submenú en bucle para que "Volver al submenú" funcione correctamente
    while True:
        print_menu_box('Avanzado: Suma y Resta (Complemento a 2)', ['1) Suma', '2) Resta', '3) Volver'])
        opc = input('Elija una opción: ')
        if opc == '3' or opc == '':
            return
        if opc not in ('1', '2'):
            print('Opción no válida')
            continue

        try:
            a = int(input('Primer operando (decimal): '))
            b = int(input('Segundo operando (decimal): '))
            bits = int(input('Bits para la operación (ej. 8,16,32): '))
        except Exception:
            print('Entrada inválida')
            # volver a mostrar el submenú
            continue

        try:
            ra = complemento_a_dos(a, bits)
            rb = complemento_a_dos(b, bits)
        except OverflowError as e:
            print('Error en representación de operandos:', e)
            # volver a mostrar el submenú
            continue

        type_print('A (Ca2): ' + ra)
        type_print('B (Ca2): ' + rb)

        if opc == '1':
            esperado = a + b
            operacion = 'Suma'
        else:
            esperado = a - b
            operacion = 'Resta'

        mask = (1 << bits) - 1
        ca2_res = format(esperado & mask, 'b').zfill(bits)

        # mostrar resultado en Ca2 y reconvertir usando invertir+1 para negativos
        type_print(f'{operacion} decimal esperada: {esperado}')
        type_print('Resultado (Ca2, truncado a N bits): ' + ca2_res)

        reconv = ca2_to_decimal_invert(ca2_res)

        # overflow si el valor aritmético no cabe en N bits
        limite_min = -(1 << (bits - 1))
        limite_max = (1 << (bits - 1)) - 1
        if esperado < limite_min or esperado > limite_max:
            print('Advertencia: overflow aritmético - el resultado real no cabe en', bits, 'bits')

        accion = post_conversion_menu()
        if accion == 'submenu':
            # volver a mostrar el submenú
            continue
        elif accion == 'main':
            return
        elif accion == 'exit':
            sys.exit(0)


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
