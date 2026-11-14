from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from library_item import LibraryItem


class Member:
    """Anggota yang menyimpan data dan daftar pinjaman."""

    def __init__(self, nama: str, nim: str) -> None:
        self.__nama = nama
        self.__nim = nim
        self.__daftar_pinjaman: list[LibraryItem] = []

    @property
    def nama(self) -> str:
        return self.__nama

    @property
    def nim(self) -> str:
        return self.__nim

    @property
    def daftar_pinjaman(self) -> tuple[LibraryItem, ...]:
        return tuple(self.__daftar_pinjaman)

    def pinjam_item(self, item: LibraryItem) -> bool:
        """Catat item ke daftar pinjaman."""
        if item in self.__daftar_pinjaman:
            return False
        self.__daftar_pinjaman.append(item)
        return True

    def kembalikan_item(self, item: LibraryItem) -> bool:
        """Hapus item dari daftar pinjaman."""
        if item not in self.__daftar_pinjaman:
            return False
        self.__daftar_pinjaman.remove(item)
        return True

    def get_detail(self) -> str:
        """Detail anggota dan pinjaman."""
        if not self.__daftar_pinjaman:
            daftar = "-"
        else:
            daftar = ", ".join(
                f"{item.id_item}: {item.judul}" for item in self.__daftar_pinjaman
            )
        return f"Anggota: {self.__nama} ({self.__nim}) | Pinjaman: {daftar}"

    def __str__(self) -> str:
        return self.get_detail()
