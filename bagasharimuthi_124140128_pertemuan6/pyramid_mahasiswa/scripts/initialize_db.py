import argparse
import sys
from datetime import date

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from .. import models


def setup_models(dbsession):
    """Menambahkan data awal (seeding) mahasiswa dan matakuliah ke database."""
    if dbsession.query(models.MyModel).filter_by(name='one').first() is None:
        dbsession.add(models.MyModel(name='one', value=1))

    initial_mahasiswas = [
        models.Mahasiswa(
            nim='124140212',
            nama='Arya Dimar Fath',
            jurusan='Teknik Informatika',
            tanggal_lahir=date(2005, 4, 12),
            alamat='Bandar Lampung',
        ),
        models.Mahasiswa(
            nim='124140008',
            nama='MAULANA MUHAMMAD RIZKI',
            jurusan='Teknik Informatika',
            tanggal_lahir=date(2005, 7, 20),
            alamat='Lampung Selatan',
        ),
    ]
    for mhs in initial_mahasiswas:
        if dbsession.query(models.Mahasiswa).filter_by(nim=mhs.nim).first() is None:
            dbsession.add(mhs)

    initial_matakuliahs = [
        models.Matakuliah(
            kode_mk='IF25-22015',
            nama_mk='Sistem Informasi',
            sks=3,
            semester=4,
        ),
        models.Matakuliah(
            kode_mk='IF25-22014',
            nama_mk='Pengembangan Aplikasi Web',
            sks=3,
            semester=4,
        ),
        models.Matakuliah(
            kode_mk='IF25-21008',
            nama_mk='Jaringan Komputer',
            sks=3,
            semester=3,
        ),
    ]
    for mk in initial_matakuliahs:
        if dbsession.query(models.Matakuliah).filter_by(kode_mk=mk.kode_mk).first() is None:
            dbsession.add(mk)


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            setup_models(dbsession)
            print("Berhasil memasukkan data seeding awal mahasiswa dan matakuliah!")
    except OperationalError:
        print("Pyramid gagal terhubung ke database SQL.")
        print("Pastikan service PostgreSQL berjalan dan connection string di development.ini benar.")


if __name__ == '__main__':
    main()
