import sys
import time

# Configuración de animaciones
ANIMAR_TITULOS = True
RETRASO_TITULO = 0.02


def type_print(texto, retraso=0.02, terminar=True):
    for ch in str(texto):
        print(ch, end='', flush=True)
        time.sleep(retraso)
    if terminar:
        print()


def print_menu_box(titulo, opciones, pausa=0.22):
    print()
    time.sleep(pausa)
    ancho = max(len(titulo), *(len(o) for o in opciones))

    # título animado opcional (sin caja ASCII)
    if ANIMAR_TITULOS:
        type_print(titulo.center(ancho), retraso=RETRASO_TITULO)
    else:
        print(titulo.center(ancho))

    # opciones (sin animación)
    print()
    for o in opciones:
        print(o)
    print()


def convertir_decimal_a_base_entera(numero, base):
    digitos = "0123456789ABCDEF"
    if numero == 0:
        return "0"
    lista_resultados = []
    valor = numero
    while valor > 0:
        lista_resultados.append(digitos[valor % base])
        valor //= base
    lista_resultados.reverse()
    return ''.join(lista_resultados)


def convertir_base_a_decimal(cadena, base):
    cadena = cadena.strip().upper()
    valor_decimal = 0
    for caracter in cadena:
        if '0' <= caracter <= '9':
            dig = ord(caracter) - ord('0')
        else:
            dig = ord(caracter) - ord('A') + 10
        if dig >= base:
            raise ValueError('Dígito fuera de rango para la base')
        valor_decimal = valor_decimal * base + dig
    return valor_decimal


def complemento_a_dos(numero, bits):
    limite_minimo = -(1 << (bits - 1))
    limite_maximo = (1 << (bits - 1)) - 1
    if numero < limite_minimo or numero > limite_maximo:
        raise OverflowError('Overflow: no cabe en el número de bits especificado')
    mascara = (1 << bits) - 1
    enmascarado = numero & mascara
    binario = format(enmascarado, 'b').zfill(bits)
    return binario


def complemento_a_dos_a_decimal(binario_str):
    bits = len(binario_str)
    valor_entero = int(binario_str, 2)
    if binario_str[0] == '0':
        return valor_entero
    else:
        return valor_entero - (1 << bits)


def ca2_to_decimal_invert(ca2_str):
    """Convertir Ca2 a decimal usando el método invertir+1 para negativos."""
    if ca2_str[0] == '0':
        return int(ca2_str, 2)
    invertido = ''.join('1' if b == '0' else '0' for b in ca2_str)
    magnitud = int(invertido, 2) + 1
    return -magnitud


def procesar_complemento_a_dos(numero, bits_num):
    """Realiza la conversión a complemento a dos y muestra la verificación.

    Lógica extraída desde el menú para mantener el menú limpio.
    Lanza OverflowError si el número no cabe en los bits indicados.
    """
    limite_minimo = -(1 << (bits_num - 1))
    limite_maximo = (1 << (bits_num - 1)) - 1
    if numero < limite_minimo or numero > limite_maximo:
        raise OverflowError('Overflow: no cabe en el número de bits especificado')

    mascara = (1 << bits_num) - 1

    if numero >= 0:
        bin_relleno = format(numero, 'b').zfill(bits_num)
        type_print(f'Número positivo. Binario ({bits_num} bits): {bin_relleno}')
        ca2 = bin_relleno
    else:
        valor_abs = abs(numero)
        bin_abs = format(valor_abs, 'b')
        if len(bin_abs) > bits_num:
            raise OverflowError('Overflow: valor absoluto demasiado grande para los bits')
        bin_abs_relleno = bin_abs.zfill(bits_num)
        type_print(f'Valor absoluto |X| en binario (relleno a {bits_num} bits): {bin_abs_relleno}')
        # complemento a uno
        complemento_uno = ''.join('1' if b == '0' else '0' for b in bin_abs_relleno)
        type_print(f'Complemento a uno (C1): {complemento_uno}')
        # sumar 1
        suma_uno = (int(complemento_uno, 2) + 1) & mascara
        ca2 = format(suma_uno, 'b').zfill(bits_num)
        type_print(f'Sumar 1 al C1 -> Complemento a dos (Ca2): {ca2}')

    # Verificación / reconversión mostrando el proceso
    type_print('')
    type_print('--- Verificación: revertir Ca2 a decimal ---')
    type_print(f'Ca2 actual: {ca2}')
    if ca2[0] == '0':
        reconvertido = int(ca2, 2)
        type_print('Bit de signo 0 -> número positivo')
        # mostrar proceso de expansión polinómica (dígito * base^posición)
        type_print('Proceso (expansión polinómica):')
        contribuciones = []
        suma_total = 0
        # mostrar desde LSB (posición 0) hasta MSB
        for pos, bit in enumerate(reversed(ca2)):
            if bit == '1':
                val = 1 << pos
                contribuciones.append(f'1 * 2^{pos} = {val}')
                suma_total += val
            else:
                contribuciones.append(f'0 * 2^{pos} = 0')
        # imprimir algunas contribuciones (no todas si son muchas)
        max_mostrar = 8
        if len(contribuciones) <= max_mostrar:
            for c in contribuciones:
                type_print('  ' + c)
        else:
            # mostrar las últimas y las primeras para no ser muy verboso
            for c in contribuciones[:4]:
                type_print('  ' + c)
            type_print('  ...')
            for c in contribuciones[-4:]:
                type_print('  ' + c)

        type_print('Suma de contribuciones = ' + str(suma_total))
        type_print('Decimal reconvertido: ' + str(reconvertido))
    else:
        type_print('Bit de signo 1 -> número negativo')
        # método elegido: invertir y sumar 1 para obtener la magnitud
        invertido = ''.join('1' if b == '0' else '0' for b in ca2)
        type_print('Invertir bits (C1 de Ca2): ' + invertido)
        magnitud = int(invertido, 2) + 1
        type_print('Sumar 1 al C1 para obtener |X|: ' + str(magnitud))
        type_print('Decimal reconvertido: -' + str(magnitud))
        # resumen corto (solo mostrar la magnitud negativa calculada)


def suma_ca2(operando_a, operando_b, bits_operacion):

    ca2_a = complemento_a_dos(operando_a, bits_operacion)
    ca2_b = complemento_a_dos(operando_b, bits_operacion)
    resultado_esperado = operando_a + operando_b
    mascara = (1 << bits_operacion) - 1
    ca2_resultado = format(resultado_esperado & mascara, 'b').zfill(bits_operacion)
    reconvertido = ca2_to_decimal_invert(ca2_resultado)
    limite_minimo = -(1 << (bits_operacion - 1))
    limite_maximo = (1 << (bits_operacion - 1)) - 1
    overflow = resultado_esperado < limite_minimo or resultado_esperado > limite_maximo
    return {
        'ca2_a': ca2_a,
        'ca2_b': ca2_b,
        'ca2_resultado': ca2_resultado,
        'reconvertido': reconvertido,
        'overflow': overflow,
        'resultado_esperado': resultado_esperado,
    }



def resta_ca2(operando_a, operando_b, bits_operacion):
    """Resta con complemento a dos en N bits (A - B)."""
    ca2_a = complemento_a_dos(operando_a, bits_operacion)
    ca2_b = complemento_a_dos(operando_b, bits_operacion)
    resultado_esperado = operando_a - operando_b
    mascara = (1 << bits_operacion) - 1
    ca2_resultado = format(resultado_esperado & mascara, 'b').zfill(bits_operacion)
    reconvertido = ca2_to_decimal_invert(ca2_resultado)
    limite_minimo = -(1 << (bits_operacion - 1))
    limite_maximo = (1 << (bits_operacion - 1)) - 1
    overflow = resultado_esperado < limite_minimo or resultado_esperado > limite_maximo
    return {
        'ca2_a': ca2_a,
        'ca2_b': ca2_b,
        'ca2_resultado': ca2_resultado,
        'reconvertido': reconvertido,
        'overflow': overflow,
        'resultado_esperado': resultado_esperado,
    }


def menu_decimal_a_otras_bases():
    while True:
        entrada = input('Ingrese un número entero decimal positivo: ')
        try:
            numero_decimal = int(entrada)
            if numero_decimal < 0:
                print('Número debe ser positivo')
                print('1) Reintentar')
                print('2) Volver al menú principal')
                eleccion = input('Elija una opción: ')
                if eleccion == '1' or eleccion == '':
                    continue
                else:
                    return
            break
        except ValueError:
            print('Entrada no válida')
            print('1) Reintentar')
            print('2) Volver al menú principal')
            eleccion = input('Elija una opción: ')
            if eleccion == '1' or eleccion == '':
                continue
            else:
                return
    while True:
        print_menu_box(f'Convertir {numero_decimal} a', ['1) Binario', '2) Octal', '3) Hexadecimal', '4) Todos', '5) Volver'])
        opcion = input('Elija una opción: ')
        if opcion == '1':
            type_print('Binario: ' + convertir_decimal_a_base_entera(numero_decimal, 2))
            accion = post_conversion_menu()
        elif opcion == '2':
            type_print('Octal: ' + convertir_decimal_a_base_entera(numero_decimal, 8))
            accion = post_conversion_menu()
        elif opcion == '3':
            type_print('Hexadecimal: ' + convertir_decimal_a_base_entera(numero_decimal, 16))
            accion = post_conversion_menu()
        elif opcion == '4' or opcion == '':
            type_print('Binario: ' + convertir_decimal_a_base_entera(numero_decimal, 2))
            type_print('Octal: ' + convertir_decimal_a_base_entera(numero_decimal, 8))
            type_print('Hexadecimal: ' + convertir_decimal_a_base_entera(numero_decimal, 16))
            accion = post_conversion_menu()
        elif opcion == '5':
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
    eleccion = input('Elija una opción: ')
    if eleccion == '1' or eleccion == '':
        return 'submenu'
    elif eleccion == '2':
        return 'main'
    elif eleccion == '3':
        return 'exit'
    else:
        print('Opción no válida, volviendo al submenú')
        return 'submenu'


def menu_otras_bases_a_decimal():
    while True:
        print_menu_box('Convertir a decimal desde', ['1) Binario (base 2)', '2) Octal (base 8)', '3) Hexadecimal (base 16)', '4) Volver'])
        opcion_base = input('Elija una opción: ')
        if opcion_base == '1':
            base = 2
        elif opcion_base == '2':
            base = 8
        elif opcion_base == '3':
            base = 16
        elif opcion_base == '4' or opcion_base == '':
            return
        else:
            print('Opción no válida')
            continue

        # pedir número en la base seleccionada
        while True:
            cadena = input(f'Ingrese el número en base {base}: ')
            try:
                decimal_valor = convertir_base_a_decimal(cadena, base)
                type_print('Decimal: ' + str(decimal_valor))
            except Exception as e:
                print('Error:', e)
                print('1) Reintentar')
                print('2) Volver al submenú')
                eleccion = input('Elije una opción: ')
                if eleccion == '1' or eleccion == '':
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
        entrada_str = input('Ingrese número entero (positivo o negativo): ')
        try:
            numero = int(entrada_str)
        except Exception:
            print('Entrada no válida')
            print('1) Reintentar')
            print('2) Volver al menú principal')
            eleccion = input('Elija una opción: ')
            if eleccion == '1' or eleccion == '':
                continue
            else:
                return

        bits_str = input('Ingrese número de bits (ej. 8, 16, 32): ')
        try:
            bits_num = int(bits_str)
            if bits_num <= 0:
                raise ValueError()
        except Exception:
            print('Bits inválidos')
            print('1) Reintentar')
            print('2) Volver al menú principal')
            eleccion = input('Elija una opción: ')
            if eleccion == '1' or eleccion == '':
                continue
            else:
                return

        try:
            procesar_complemento_a_dos(numero, bits_num)
        except OverflowError as e:
            print('Error:', e)
            print('1) Reintentar')
            print('2) Volver al menú principal')
            eleccion = input('Elija una opción: ')
            if eleccion == '1' or eleccion == '':
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
        opcion_avanzado = input('Elija una opción: ')
        if opcion_avanzado == '3' or opcion_avanzado == '':
            return
        if opcion_avanzado not in ('1', '2'):
            print('Opción no válida')
            continue

        try:
            operando_a = int(input('Primer operando (decimal): '))
            operando_b = int(input('Segundo operando (decimal): '))
            bits_operacion = int(input('Bits para la operación (ej. 8,16,32): '))
        except Exception:
            print('Entrada inválida')
            # volver a mostrar el submenú
            continue

        try:
            if opcion_avanzado == '1':
                tipo_operacion = 'Suma'
                res = suma_ca2(operando_a, operando_b, bits_operacion)
            else:
                tipo_operacion = 'Resta'
                res = resta_ca2(operando_a, operando_b, bits_operacion)
        except OverflowError as e:
            print('Error en representación de operandos:', e)
            # volver a mostrar el submenú
            continue

        type_print('A (Ca2): ' + res['ca2_a'])
        type_print('B (Ca2): ' + res['ca2_b'])
        type_print(f'{tipo_operacion} decimal esperada: ' + str(res['resultado_esperado']))
        type_print('Resultado (Ca2, truncado a N bits): ' + res['ca2_resultado'])

        if res['overflow']:
            print('Advertencia: overflow aritmético - el resultado real no cabe en', bits_operacion, 'bits')

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
