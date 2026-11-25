from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPBadRequest,
)
from sqlalchemy.exc import IntegrityError
from ..models import Matakuliah


def _validate_positive_int(value, field_name):
    """Memastikan field bertipe integer positif (> 0)."""
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        return f'Field {field_name} harus berupa bilangan bulat positif (> 0)'
    return None


@view_config(route_name='matakuliah_list', renderer='json')
def matakuliah_list(request):
    """View untuk mengambil semua data matakuliah."""
    dbsession = request.dbsession
    matakuliahs = dbsession.query(Matakuliah).order_by(Matakuliah.id.asc()).all()
    return {'matakuliahs': [mk.to_dict() for mk in matakuliahs]}


@view_config(route_name='matakuliah_detail', renderer='json')
def matakuliah_detail(request):
    """View untuk melihat detail satu matakuliah berdasarkan ID di URL."""
    dbsession = request.dbsession
    try:
        matakuliah_id = int(request.matchdict['id'])
    except ValueError:
        return HTTPBadRequest(json_body={'error': 'ID harus berupa bilangan bulat'})
    matakuliah = dbsession.query(Matakuliah).filter_by(id=matakuliah_id).first()

    if matakuliah is None:
        return HTTPNotFound(
            json_body={'error': f'Matakuliah dengan ID {matakuliah_id} tidak ditemukan'}
        )

    return {'matakuliah': matakuliah.to_dict()}


@view_config(route_name='matakuliah_add', request_method='POST', renderer='json')
def matakuliah_add(request):
    """View untuk menambahkan matakuliah baru dari payload JSON."""
    try:
        json_data = request.json_body
    except ValueError:
        return HTTPBadRequest(json_body={'error': 'Payload JSON tidak valid'})

    if not isinstance(json_data, dict):
        return HTTPBadRequest(json_body={'error': 'Payload JSON harus berupa objek'})

    try:
        required_fields = ['kode_mk', 'nama_mk', 'sks', 'semester']
        for field in required_fields:
            if field not in json_data or json_data[field] is None or json_data[field] == '':
                return HTTPBadRequest(json_body={'error': f'Field {field} wajib diisi!'})

        kode_mk = str(json_data['kode_mk']).strip()
        nama_mk = str(json_data['nama_mk']).strip()
        if not kode_mk or not nama_mk:
            return HTTPBadRequest(
                json_body={'error': 'Field kode_mk dan nama_mk tidak boleh kosong'}
            )

        for int_field in ('sks', 'semester'):
            error_msg = _validate_positive_int(json_data[int_field], int_field)
            if error_msg:
                return HTTPBadRequest(json_body={'error': error_msg})

        matakuliah = Matakuliah(
            kode_mk=kode_mk,
            nama_mk=nama_mk,
            sks=json_data['sks'],
            semester=json_data['semester'],
        )

        dbsession = request.dbsession
        dbsession.add(matakuliah)
        dbsession.flush()

        return {'success': True, 'matakuliah': matakuliah.to_dict()}

    except IntegrityError:
        request.dbsession.rollback()
        return HTTPBadRequest(json_body={'error': 'Kode matakuliah sudah terdaftar'})
    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})


@view_config(route_name='matakuliah_update', request_method='PUT', renderer='json')
def matakuliah_update(request):
    """View untuk mengupdate data matakuliah berdasarkan ID."""
    dbsession = request.dbsession
    try:
        matakuliah_id = int(request.matchdict['id'])
    except ValueError:
        return HTTPBadRequest(json_body={'error': 'ID harus berupa bilangan bulat'})

    matakuliah = dbsession.query(Matakuliah).filter_by(id=matakuliah_id).first()
    if matakuliah is None:
        return HTTPNotFound(
            json_body={'error': f'Matakuliah dengan ID {matakuliah_id} tidak ditemukan'}
        )

    try:
        json_data = request.json_body
    except ValueError:
        return HTTPBadRequest(json_body={'error': 'Payload JSON tidak valid'})

    if not isinstance(json_data, dict):
        return HTTPBadRequest(json_body={'error': 'Payload JSON harus berupa objek'})

    try:
        if 'kode_mk' in json_data:
            kode_mk = str(json_data['kode_mk']).strip() if json_data['kode_mk'] is not None else ''
            if not kode_mk:
                return HTTPBadRequest(json_body={'error': 'Field kode_mk wajib diisi!'})
            matakuliah.kode_mk = kode_mk

        if 'nama_mk' in json_data:
            nama_mk = str(json_data['nama_mk']).strip() if json_data['nama_mk'] is not None else ''
            if not nama_mk:
                return HTTPBadRequest(json_body={'error': 'Field nama_mk wajib diisi!'})
            matakuliah.nama_mk = nama_mk

        if 'sks' in json_data:
            error_msg = _validate_positive_int(json_data['sks'], 'sks')
            if error_msg:
                return HTTPBadRequest(json_body={'error': error_msg})
            matakuliah.sks = json_data['sks']

        if 'semester' in json_data:
            error_msg = _validate_positive_int(json_data['semester'], 'semester')
            if error_msg:
                return HTTPBadRequest(json_body={'error': error_msg})
            matakuliah.semester = json_data['semester']

        dbsession.flush()
        return {'success': True, 'matakuliah': matakuliah.to_dict()}

    except IntegrityError:
        dbsession.rollback()
        return HTTPBadRequest(json_body={'error': 'Kode matakuliah sudah terdaftar'})
    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})


@view_config(route_name='matakuliah_delete', request_method='DELETE', renderer='json')
def matakuliah_delete(request):
    """View untuk menghapus matakuliah berdasarkan ID."""
    dbsession = request.dbsession
    try:
        matakuliah_id = int(request.matchdict['id'])
    except ValueError:
        return HTTPBadRequest(json_body={'error': 'ID harus berupa bilangan bulat'})

    matakuliah = dbsession.query(Matakuliah).filter_by(id=matakuliah_id).first()
    if matakuliah is None:
        return HTTPNotFound(
            json_body={'error': f'Matakuliah dengan ID {matakuliah_id} tidak ditemukan'}
        )

    dbsession.delete(matakuliah)

    return {'success': True, 'message': f'Matakuliah dengan ID {matakuliah_id} berhasil dihapus'}
