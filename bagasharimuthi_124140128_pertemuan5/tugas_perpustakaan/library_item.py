from abc import ABC, abstractmethod


class LibraryItem(ABC):
    """Abstract base class untuk semua item perpustakaan."""

    def __init__(self, id_item: str, judul: str, tahun: int) -> None:
        self.__id_item = id_item
        self.judul = judul
        self.tahun = tahun
        self._dipinjam = False

    @property
    def id_item(self) -> str:
        return self.__id_item

    @property
    def is_dipinjam(self) -> bool:
        return self._dipinjam

    @abstractmethod
    def hitung_denda(self, hari_terlambat: int) -> float:
        """Hitung denda berdasarkan hari keterlambatan."""
        raise NotImplementedError

    @abstractmethod
    def get_detail(self) -> str:
        """Kembalikan detail item."""
        raise NotImplementedError

    def pinjam(self) -> bool:
        """Tandai item dipinjam; False jika sudah dipinjam."""
        if self._dipinjam:
            return False
        self._dipinjam = True
        return True

    def kembalikan(self) -> bool:
        """Tandai item tersedia; False jika tidak sedang dipinjam."""
        if not self._dipinjam:
            return False
        self._dipinjam = False
        return True

    def __str__(self) -> str:
        return self.get_detail()


class Book(LibraryItem):
    """Buku dengan penulis dan denda Rp 1.000 per hari."""

    DENDA_PER_HARI = 1000

    def __init__(self, id_item: str, judul: str, tahun: int, penulis: str) -> None:
        super().__init__(id_item, judul, tahun)
        self.penulis = penulis

    def hitung_denda(self, hari_terlambat: int) -> float:
        """Hitung denda buku."""
        hari_valid = max(0, hari_terlambat)
        return float(hari_valid * self.DENDA_PER_HARI)

    def get_detail(self) -> str:
        """Detail buku dan status."""
        status = "Dipinjam" if self.is_dipinjam else "Tersedia"
        return (
            f"[{self.id_item}] {self.judul} ({self.tahun}) | Buku | "
            f"Penulis: {self.penulis} | Status: {status}"
        )


class Magazine(LibraryItem):
    """Majalah dengan edisi dan denda Rp 500 per hari."""

    DENDA_PER_HARI = 500

    def __init__(self, id_item: str, judul: str, tahun: int, edisi: str) -> None:
        super().__init__(id_item, judul, tahun)
        self.edisi = edisi

    def hitung_denda(self, hari_terlambat: int) -> float:
        """Hitung denda majalah."""
        hari_valid = max(0, hari_terlambat)
        return float(hari_valid * self.DENDA_PER_HARI)

    def get_detail(self) -> str:
        """Detail majalah dan status."""
        status = "Dipinjam" if self.is_dipinjam else "Tersedia"
        return (
            f"[{self.id_item}] {self.judul} ({self.tahun}) | Majalah | "
            f"Edisi: {self.edisi} | Status: {status}"
        )
