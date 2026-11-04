import math_operations as math
from math_operations import keliling_persegi, luas_persegi

print(f"Luas persegi (sisi 5): {luas_persegi(5)}")
print(f"Keliling persegi (sisi 5): {keliling_persegi(5)}")
print(f"Luas persegi panjang (10, 6): {math.luas_persegi_panjang(10, 6)}")
print(f"Keliling persegi panjang (10, 6): {math.keliling_persegi_panjang(10, 6)}")
print(f"Luas lingkaran (jari-jari 7): {math.luas_lingkaran(7):.2f}")
print(f"Keliling lingkaran (jari-jari 7): {math.keliling_lingkaran(7):.2f}")
print(f"25 C ke Fahrenheit: {math.celcius_ke_fahrenheit(25):.2f} F")
print(f"25 C ke Kelvin: {math.celcius_ke_kelvin(25):.2f} K")