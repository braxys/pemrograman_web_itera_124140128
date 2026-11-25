import unittest
import transaction
import webtest

from pyramid import testing


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('.models')
        settings = self.config.get_settings()

        from .models import (
            get_engine,
            get_session_factory,
            get_tm_session,
        )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        from .models.meta import Base
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        from .models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


class TestMyViewSuccessCondition(BaseTest):

    def setUp(self):
        super(TestMyViewSuccessCondition, self).setUp()
        self.init_database()

        from .models import MyModel

        model = MyModel(name='one', value=55)
        self.session.add(model)

    def test_passing_view(self):
        from .views.default import my_view
        info = my_view(dummy_request(self.session))
        self.assertEqual(info['one'].name, 'one')
        self.assertEqual(info['project'], 'pyramid_mahasiswa')


class TestMyViewFailureCondition(BaseTest):

    def test_failing_view(self):
        from .views.default import my_view
        info = my_view(dummy_request(self.session))
        self.assertEqual(info.status_int, 500)


class FunctionalAPITests(unittest.TestCase):
    def setUp(self):
        from sqlalchemy import create_engine
        from sqlalchemy.pool import StaticPool
        from pyramid.config import Configurator
        from .models.meta import Base
        from .models import get_session_factory, get_tm_session

        self.engine = create_engine(
            'sqlite:///:memory:',
            connect_args={'check_same_thread': False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(self.engine)

        config = Configurator(settings={'sqlalchemy.url': 'sqlite:///:memory:'})
        config.include('pyramid_jinja2')
        config.include('pyramid_tm')
        config.include('pyramid_retry')
        config.include('.routes')

        session_factory = get_session_factory(self.engine)
        config.registry['dbsession_factory'] = session_factory
        config.add_request_method(
            lambda r: get_tm_session(session_factory, r.tm),
            'dbsession',
            reify=True,
        )
        config.scan('.views')

        app = config.make_wsgi_app()
        self.testapp = webtest.TestApp(app)

    def tearDown(self):
        from .models.meta import Base
        Base.metadata.drop_all(self.engine)

    def test_mahasiswa_crud(self):
        # Create
        res = self.testapp.post_json('/api/mahasiswa', {
            'nim': '124140128',
            'nama': 'Bagas Hari Muthi',
            'jurusan': 'Teknik Informatika',
            'tanggal_lahir': '2005-01-01',
            'alamat': 'Lampung Selatan',
        }, status=200)
        self.assertTrue(res.json['success'])
        mhs_id = res.json['mahasiswa']['id']

        # Read all
        res = self.testapp.get('/api/mahasiswa', status=200)
        self.assertEqual(len(res.json['mahasiswas']), 1)

        # Read one
        res = self.testapp.get(f'/api/mahasiswa/{mhs_id}', status=200)
        self.assertEqual(res.json['mahasiswa']['nim'], '124140128')

        # Update
        res = self.testapp.put_json(f'/api/mahasiswa/{mhs_id}', {
            'alamat': 'Bandar Lampung',
        }, status=200)
        self.assertEqual(res.json['mahasiswa']['alamat'], 'Bandar Lampung')

        # Validation 400
        self.testapp.post_json('/api/mahasiswa', {
            'nama': 'Tanpa NIM',
        }, status=400)

        # Delete
        res = self.testapp.delete(f'/api/mahasiswa/{mhs_id}', status=200)
        self.assertTrue(res.json['success'])

        # Not found 404
        self.testapp.get(f'/api/mahasiswa/{mhs_id}', status=404)

    def test_matakuliah_crud(self):
        # Create
        res = self.testapp.post_json('/api/matakuliah', {
            'kode_mk': 'IF3140',
            'nama_mk': 'Pengembangan Aplikasi Web',
            'sks': 3,
            'semester': 5,
        }, status=200)
        self.assertTrue(res.json['success'])
        mk_id = res.json['matakuliah']['id']

        # Duplicate kode_mk -> 400
        self.testapp.post_json('/api/matakuliah', {
            'kode_mk': 'IF3140',
            'nama_mk': 'Duplikat',
            'sks': 3,
            'semester': 5,
        }, status=400)

        # Invalid sks/semester (<= 0 or non-int) -> 400
        self.testapp.post_json('/api/matakuliah', {
            'kode_mk': 'IF9999',
            'nama_mk': 'Invalid SKS',
            'sks': 0,
            'semester': 3,
        }, status=400)
        self.testapp.post_json('/api/matakuliah', {
            'kode_mk': 'IF9998',
            'nama_mk': 'Invalid Semester',
            'sks': 3,
            'semester': -1,
        }, status=400)

        # Missing required fields -> 400
        self.testapp.post_json('/api/matakuliah', {
            'kode_mk': 'IF1111',
        }, status=400)

        # Read all
        res = self.testapp.get('/api/matakuliah', status=200)
        self.assertEqual(len(res.json['matakuliahs']), 1)

        # Read one
        res = self.testapp.get(f'/api/matakuliah/{mk_id}', status=200)
        self.assertEqual(res.json['matakuliah']['kode_mk'], 'IF3140')

        # Update
        res = self.testapp.put_json(f'/api/matakuliah/{mk_id}', {
            'nama_mk': 'Pengembangan Aplikasi Web Lanjut',
            'sks': 4,
        }, status=200)
        self.assertEqual(res.json['matakuliah']['sks'], 4)

        # Update invalid sks -> 400
        self.testapp.put_json(f'/api/matakuliah/{mk_id}', {
            'sks': -2,
        }, status=400)

        # Delete
        res = self.testapp.delete(f'/api/matakuliah/{mk_id}', status=200)
        self.assertTrue(res.json['success'])

        # Not found 404
        self.testapp.get(f'/api/matakuliah/{mk_id}', status=404)
        self.testapp.put_json(f'/api/matakuliah/{mk_id}', {'sks': 2}, status=404)
        self.testapp.delete(f'/api/matakuliah/{mk_id}', status=404)
