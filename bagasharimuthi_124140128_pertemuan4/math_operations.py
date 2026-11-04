PI = 3.14159


def luas_persegi(sisi):
    """Hitung luas persegi.

    Args:
        sisi: Panjang sisi persegi.

    Returns:
        Luas persegi.
    """
    return sisi * sisi


def keliling_persegi(sisi):
    """Hitung keliling persegi.

    Args:
        sisi: Panjang sisi persegi.

    Returns:
        Keliling persegi.
    """
    return 4 * sisi


def luas_persegi_panjang(panjang, lebar):
    """Hitung luas persegi panjang.

    Args:
        panjang: Panjang persegi panjang.
        lebar: Lebar persegi panjang.

    Returns:
        Luas persegi panjang.
    """
    return panjang * lebar


def keliling_persegi_panjang(panjang, lebar):
    """Hitung keliling persegi panjang.

    Args:
        panjang: Panjang persegi panjang.
        lebar: Lebar persegi panjang.

    Returns:
        Keliling persegi panjang.
    """
    return 2 * (panjang + lebar)


def luas_lingkaran(jari_jari):
    """Hitung luas lingkaran.

    Args:
        jari_jari: Jari-jari lingkaran.

    Returns:
        Luas lingkaran.
    """
    return PI * jari_jari ** 2


def keliling_lingkaran(jari_jari):
    """Hitung keliling lingkaran.

    Args:
        jari_jari: Jari-jari lingkaran.

    Returns:
        Keliling lingkaran.
    """
    return 2 * PI * jari_jari


def celcius_ke_fahrenheit(celcius):
    """Konversi suhu Celsius ke Fahrenheit.

    Args:
        celcius: Suhu dalam derajat Celsius.

    Returns:
        Suhu dalam derajat Fahrenheit.
    """
    return (9 / 5) * celcius + 32


def celcius_ke_kelvin(celcius):
    """Konversi suhu Celsius ke Kelvin.

    Args:
        celcius: Suhu dalam derajat Celsius.

    Returns:
        Suhu dalam Kelvin.
    """
    return celcius + 273.15