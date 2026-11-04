berat = int(input("Berat badan (Cth: 60): "))
tinggi = float(input("Tinggi badan (Cth: 1.77): "))
bmi = berat / (tinggi * tinggi)

if bmi < 18.5:
    kategori = "Berat badan kurang"
elif bmi < 25:
    kategori = "Berat badan normal"
elif bmi < 30:
    kategori = "Berat badan berlebih"
else:
    kategori = "Obesitas"

print(f"BMI: {bmi:.2f}")
print(f"Kategori: {kategori}")