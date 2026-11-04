nilai_mahasiswa = [
    {
        "nama": "Bagas Hari Muthi",
        "nim": "124140128",
        "nilai_uts": 100,
        "nilai_uas": 80,
        "nilai_tugas": 90
    },
    {
        "nama": "Udin",
        "nim": "124140243",
        "nilai_uts": 80,
        "nilai_uas": 50,
        "nilai_tugas": 60
    },
    {
        "nama": "Wildan Setiawan",
        "nim": "124140231",
        "nilai_uts": 50,
        "nilai_uas": 20,
        "nilai_tugas": 70
    },
    {
        "nama": "Petrus Simanjuntak",
        "nim": "124140152",
        "nilai_uts": 90,
        "nilai_uas": 100,
        "nilai_tugas": 90
    },
    {
        "nama": "Arya Dimar Fath",
        "nim": "124140212",
        "nilai_uts": 70,
        "nilai_uas": 60,
        "nilai_tugas": 80
    }
]

for data in nilai_mahasiswa:
    nilai_akhir = (0.3 * data["nilai_uts"]) + (0.4 * data["nilai_uas"]) + (0.3 * data["nilai_tugas"])
    data["nilai_akhir"] = nilai_akhir

    if nilai_akhir >= 80:
        data["grade"] = "A"
    elif nilai_akhir >= 70:
        data["grade"] = "B"
    elif nilai_akhir >= 60:
        data["grade"] = "C"
    elif nilai_akhir >= 50:
        data["grade"] = "D"
    else:
        data["grade"] = "E"

print(f"{'Nama':<20} {'NIM':<12} {'Nilai Akhir':>12} {'Grade':>6}")
print("-" * 55)

for data in nilai_mahasiswa:
    print(f"{data['nama']:<20} {data['nim']:<12} {data['nilai_akhir']:>12.2f} {data['grade']:>6}")

tertinggi = max(nilai_mahasiswa, key=lambda x: x["nilai_akhir"])
terendah = min(nilai_mahasiswa, key=lambda x: x["nilai_akhir"])

print("\nNilai tertinggi:", tertinggi["nama"], "-", tertinggi["nilai_akhir"])
print("Nilai terendah:", terendah["nama"], "-", terendah["nilai_akhir"])