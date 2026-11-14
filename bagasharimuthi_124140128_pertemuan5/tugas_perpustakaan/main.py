from library import Library
from library_item import Book, LibraryItem, Magazine
from member import Member


def main() -> None:
    perpustakaan = Library("Perpustakaan ITERA")

    print("=== 1. MENAMBAHKAN ITEM ===")
    buku_python = Book("B001", "Python Crash Course", 2019, "Eric Matthes")
    buku_clean = Book("B002", "Clean Code", 2008, "Robert C. Martin")
    majalah_geo = Magazine("M001", "National Geographic", 2024, "05/2024")

    for item in (buku_python, buku_clean, majalah_geo):
        perpustakaan.tambah_item(item)

    print("\n=== 2. KATALOG AWAL ===")
    perpustakaan.tampilkan_katalog()

    print("\n=== 3. PENCARIAN BERDASARKAN JUDUL ===")
    hasil_judul = perpustakaan.cari_item("python")
    if hasil_judul:
        for item in hasil_judul:
            print(item.get_detail())
    else:
        print("Item tidak ditemukan.")

    print("\n=== 4. PENCARIAN BERDASARKAN ID ===")
    hasil_id = perpustakaan.cari_item("M001")
    if hasil_id:
        for item in hasil_id:
            print(item.get_detail())
    else:
        print("Item tidak ditemukan.")

    print("\n=== 5. PEMINJAMAN ITEM ===")
    anggota = Member("Bagas Hari Muthi", "124140128")
    perpustakaan.pinjam_item("B001", anggota)

    print("\nMencoba meminjam item yang sama untuk kedua kalinya:")
    perpustakaan.pinjam_item("B001", anggota)

    print("\n=== 6. STATUS SETELAH PEMINJAMAN ===")
    perpustakaan.tampilkan_semua_item()
    print(anggota.get_detail())

    print("\n=== 7. PENGEMBALIAN DAN DENDA ===")
    denda = perpustakaan.kembalikan_item("B001", anggota, hari_terlambat=3)
    if denda is not None:
        print(f"Total denda yang dibayar: Rp {denda:,.0f}")

    print("\n=== 8. PERBANDINGAN DENDA (POLYMORPHISM) ===")
    for item in (buku_clean, majalah_geo):
        print(
            f"{item.judul}: denda 3 hari = Rp {item.hitung_denda(3):,.0f} "
            f"(jenis: {type(item).__name__})"
        )

    print("\n=== 9. KATALOG AKHIR ===")
    perpustakaan.tampilkan_katalog()
    print(anggota.get_detail())

    print("\n=== 10. BUKTI ABSTRACT CLASS ===")
    try:
        LibraryItem("X001", "Item Abstrak", 2024)
    except TypeError as error:
        print(f"LibraryItem tidak dapat diinstansiasi langsung: {error}")


if __name__ == "__main__":
    main()
