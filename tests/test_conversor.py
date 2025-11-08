from src.conversor import convertir_decimal_a_base_entera, convertir_base_a_decimal, complemento_a_dos, complemento_a_dos_a_decimal


def test_funciones_existen():
    assert callable(convertir_decimal_a_base_entera)
    assert callable(convertir_base_a_decimal)
    assert callable(complemento_a_dos)
    assert callable(complemento_a_dos_a_decimal)
