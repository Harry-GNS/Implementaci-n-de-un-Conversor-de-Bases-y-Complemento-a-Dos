import sys
import time

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


    if ANIMAR_TITULOS:
        type_print(titulo.center(ancho), retraso=RETRASO_TITULO)
    else:
        print(titulo.center(ancho))

    
    print()
    for o in opciones:
        print(o)
    print()

# Esta función posee parámetros de número y base los cuales se puede asignar un número mayor a 0 y una base de 2,8,16
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

#En esta función se realiza el cambio de una cadena que se encuentra en base 2,8,16 a decimal, el Código se encarga de que las cádenas sean validas.

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

# En está función recibe un número entre el mínimo y el máximo número que se obtiene a través de los bits dispnibles, por ejemplo 8 el min es -128 y el máx 127
#El overflow nos ayuda a validar que el número se encuentre en los bits permitidos.
#El apartado de mascara nos define el máximo que se puede obtener y retorna el enmascaro que es cambiar todo a la izquierda por 1 y después sumar 1.
def complemento_a_dos(numero, bits):
    limite_minimo = -(1 << (bits - 1))
    limite_maximo = (1 << (bits - 1)) - 1
    if numero < limite_minimo or numero > limite_maximo:
        raise OverflowError('Overflow: no cabe en el número de bits especificado')
    mascara = (1 << bits) - 1
    enmascarado = numero & mascara
    binario = format(enmascarado, 'b').zfill(bits)
    return binario
#La función lo que va a realizar es retornar del complemento a2 a decimal, teniendo en cuenta lógicamente el sigo que posee.
#Entonces posee un parámetro binario_str que nos indica el valor de bits que posee y que solo son optimos los positivos.
#Entonces se hace una validación que si el binario_str tiene su valor incial igual a 0 el valor es un entero.
#Por lo que si termina en 1 el valor entra a una operación del número halado o transformado en deciman y se lo resta con el valor de bits que posee el string o en este caso el binario_str.

def complemento_a_dos_a_decimal(binario_str):
    bits = len(binario_str)
    valor_entero = int(binario_str, 2)
    if binario_str[0] == '0':
        return valor_entero
    else:
        return valor_entero - (1 << bits)
#Convertir Ca2 a decimal usando el método invertir+1 para negativos.
#Entonces realiza una validación de que si ca2_str su primer número es positivo, lo retorna igual.
#Pero si se comienza con 1 hace el cambio de 1 por 0 y de 0 por 1, invirtiendo la cadena.
#Por último se asigna una nueva variable magnitud que posee un int con parámetros(invertido,base 2) y esto suma 1, finalizando con agregar el sigo negativo para la variable magnitud.

def ca2_to_decimal_invert(ca2_str):
    if ca2_str[0] == '0':
        return int(ca2_str, 2)
    invertido = ''.join('1' if b == '0' else '0' for b in ca2_str)
    magnitud = int(invertido, 2) + 1
    return -magnitud

#Está función posee cosas de las anteriores funciones como la verifiación del rango de acuerdo al número de bits y nos indica el overflow.
#Produce la máscara y en el primer if valida que si hay un número mayor o igual que 0, se regrese el valor y si hay espación vacíos rellana con N bits.
#Entonces si no cumple con eso entra en otro escenario donde se aplica el valor absoluto del binario.
#Este valor absoluto entra a una validación donde si el valor absoluto es mayor al número de bits se va producir un overflow.
#Pero si es igual realiza el cambio de bits de 0 por 1 y de 1 por 0 para después sumar 1 de esta forma obteniendo el complemento a2
#Lo último lo que hace es volver a pasar de complemento a2 a decimal nuevamente,de acuerdo al singo que posea.
#Entonces si postivo el decimal se imprime, pero si es negativo lo que realiza lo el cambio de 0 por 1 y de 1 por 0, después suma por 1 y por último transforma e imprime.
def procesar_complemento_a_dos(numero, bits_num):
   
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
        complemento_uno = ''.join('1' if b == '0' else '0' for b in bin_abs_relleno)
        type_print(f'Complemento a uno (C1): {complemento_uno}')
        suma_uno = (int(complemento_uno, 2) + 1) & mascara
        ca2 = format(suma_uno, 'b').zfill(bits_num)
        type_print(f'Sumar 1 al C1 -> Complemento a dos (Ca2): {ca2}')

    type_print('')
    type_print('--- Verificación: revertir Ca2 a decimal ---')
    type_print(f'Ca2 actual: {ca2}')
    if ca2[0] == '0':
        reconvertido = int(ca2, 2)
        type_print('Bit de signo 0 -> número positivo')
        type_print('Proceso (expansión polinómica):')
        contribuciones = []
        suma_total = 0
        for pos, bit in enumerate(reversed(ca2)):
            if bit == '1':
                val = 1 << pos
                contribuciones.append(f'1 * 2^{pos} = {val}')
                suma_total += val
            else:
                contribuciones.append(f'0 * 2^{pos} = 0')
        max_mostrar = 8
        if len(contribuciones) <= max_mostrar:
            for c in contribuciones:
                type_print('  ' + c)
        else:
            for c in contribuciones[:4]:
                type_print('  ' + c)
            type_print('  ...')
            for c in contribuciones[-4:]:
                type_print('  ' + c)

        type_print('Suma de contribuciones = ' + str(suma_total))
        type_print('Decimal reconvertido: ' + str(reconvertido))
    else:
        type_print('Bit de signo 1 -> número negativo')
        invertido = ''.join('1' if b == '0' else '0' for b in ca2)
        type_print('Invertir bits (C1 de Ca2): ' + invertido)
        magnitud = int(invertido, 2) + 1
        type_print('Sumar 1 al C1 para obtener |X|: ' + str(magnitud))
        type_print('Decimal reconvertido: -' + str(magnitud))
        


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
            continue

        try:
            ca2_a = complemento_a_dos(operando_a, bits_operacion)
            ca2_b = complemento_a_dos(operando_b, bits_operacion)
        except OverflowError as e:
            print('Error en representación de operandos:', e)
            continue

        type_print('A (Ca2): ' + ca2_a)
        type_print('B (Ca2): ' + ca2_b)

        if opcion_avanzado == '1':
            resultado_esperado = operando_a + operando_b
            tipo_operacion = 'Suma'
        else:
            resultado_esperado = operando_a - operando_b
            tipo_operacion = 'Resta'

        mascara = (1 << bits_operacion) - 1
        ca2_resultado = format(resultado_esperado & mascara, 'b').zfill(bits_operacion)

        type_print(f'{tipo_operacion} decimal esperada: {resultado_esperado}')
        type_print('Resultado (Ca2, truncado a N bits): ' + ca2_resultado)

        reconvertido = ca2_to_decimal_invert(ca2_resultado)

        limite_minimo = -(1 << (bits_operacion - 1))
        limite_maximo = (1 << (bits_operacion - 1)) - 1
        if resultado_esperado < limite_minimo or resultado_esperado > limite_maximo:
            print('Advertencia: overflow aritmético - el resultado real no cabe en', bits_operacion, 'bits')

        accion = post_conversion_menu()
        if accion == 'submenu':
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
