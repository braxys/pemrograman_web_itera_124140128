from __future__ import annotations

from typing import Optional

from library_item import LibraryItem
from member import Member


class Library:
    """Mengelola koleksi dan transaksi peminjaman."""

    def __init__(self, nama: str = "Perpustakaan ITERA") -> None:
        self.nama = nama
        self.__koleksi: list[LibraryItem] = []

    @property
    def total_item(self) -> int:
        return len(self.__koleksi)

    @property
    def item_tersedia(self) -> int:
        return sum(1 for item in self.__koleksi if not item.is_dipinjam)

    def __cari_by_id(self, id_item: str) -> Optional[LibraryItem]:
        id_dicari = id_item.strip().lower()
        for item in self.__koleksi:
            if item.id_item.lower() == id_dicari:
                return item
        return None

    def tambah_item(self, item: LibraryItem) -> bool:
        """Tambah item ke koleksi."""
        if not isinstance(item, LibraryItem):
            print("Gagal: item harus berupa turunan LibraryItem.")
            return False

        if self.__cari_by_id(item.id_item) is not None:
            print(f"Gagal: ID '{item.id_item}' sudah terdaftar.")
            return False

        self.__koleksi.append(item)
        print(f"Item '{item.judul}' berhasil ditambahkan.")
        return True

    def tampilkan_katalog(self) -> None:
        """Tampilkan item yang tersedia."""
        print(f"\n=== KATALOG TERSEDIA: {self.nama} ===")
        tersedia = [item for item in self.__koleksi if not item.is_dipinjam]

        if not tersedia:
            print("Tidak ada item yang tersedia.")
        else:
            for item in tersedia:
                print(item.get_detail())

        print(f"Jumlah tersedia: {len(tersedia)} dari {self.total_item} item")

    def tampilkan_semua_item(self) -> None:
        """Tampilkan semua item dan statusnya."""
        print(f"\n=== SEMUA ITEM: {self.nama} ===")
        if not self.__koleksi:
            print("Koleksi perpustakaan masih kosong.")
            return

        for item in self.__koleksi:
            print(item.get_detail())

    def cari_item(self, keyword: str) -> list[LibraryItem]:
        """Cari item berdasarkan ID atau judul."""
        kata_kunci = keyword.strip().lower()
        if not kata_kunci:
            return []

        return [
            item
            for item in self.__koleksi
            if kata_kunci in item.id_item.lower() or kata_kunci in item.judul.lower()
        ]

    def pinjam_item(self, id_item: str, member: Member) -> Optional[LibraryItem]:
        """Pinjamkan item ke anggota."""
        item = self.__cari_by_id(id_item)
        if item is None:
            print(f"Gagal: item dengan ID '{id_item}' tidak ditemukan.")
            return None

        if item.is_dipinjam:
            print(f"Gagal: '{item.judul}' sedang dipinjam.")
            return None

        if not item.pinjam():
            print(f"Gagal: '{item.judul}' tidak dapat dipinjam.")
            return None

        if not member.pinjam_item(item):
            item.kembalikan()
            print(f"Gagal: '{item.judul}' sudah tercatat pada anggota ini.")
            return None

        print(f"{member.nama} berhasil meminjam '{item.judul}'.")
        return item

    def kembalikan_item(
        self, id_item: str, member: Member, hari_terlambat: int = 0
    ) -> Optional[float]:
        """Kembalikan item dan hitung denda."""
        item = self.__cari_by_id(id_item)
        if item is None:
            print(f"Gagal: item dengan ID '{id_item}' tidak ditemukan.")
            return None

        if not item.is_dipinjam:
            print(f"Gagal: '{item.judul}' tidak sedang dipinjam.")
            return None

        if item not in member.daftar_pinjaman:
            print(f"Gagal: '{item.judul}' tidak tercatat pada pinjaman {member.nama}.")
            return None

        denda = item.hitung_denda(hari_terlambat)
        item.kembalikan()
        member.kembalikan_item(item)

        print(
            f"{member.nama} mengembalikan '{item.judul}'. "
            f"Denda keterlambatan {max(0, hari_terlambat)} hari: Rp {denda:,.0f}"
        )
        return denda
