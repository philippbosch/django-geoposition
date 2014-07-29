from decimal import Decimal
from django.test import SimpleTestCase
from geoposition import Geoposition
from example.models import PointOfInterest


class GeopositionTestCase(SimpleTestCase):
    def test_init_with_decimals(self):
        gp = Geoposition(Decimal('52.5'), Decimal('13.4'))
        self.assertEqual(gp.latitude, Decimal('52.5'))
        self.assertEqual(gp.longitude, Decimal('13.4'))

    def test_init_with_strs(self):
        gp = Geoposition('52.5', '13.4')
        self.assertEqual(gp.latitude, Decimal('52.5'))
        self.assertEqual(gp.longitude, Decimal('13.4'))

    def test_init_with_floats(self):
        gp = Geoposition(52.5, 13.4)
        self.assertEqual(gp.latitude, Decimal('52.5'))
        self.assertEqual(gp.longitude, Decimal('13.4'))

    def test_repr(self):
        gp = Geoposition(52.5, 13.4)
        self.assertEqual(repr(gp), 'Geoposition(52.5,13.4)')

    def test_len(self):
        gp = Geoposition(52.5, 13.4)
        self.assertEqual(len(gp), 9)

    def test_equality(self):
        gp1 = Geoposition(52.5, 13.4)
        gp2 = Geoposition(52.5, 13.4)
        self.assertEqual(gp1, gp2)

    def test_inequality(self):
        gp1 = Geoposition(52.5, 13.4)
        gp2 = Geoposition(52.4, 13.1)
        self.assertNotEqual(gp1, gp2)

    def test_equality_with_none(self):
        gp1 = Geoposition(52.5, 13.4)
        gp2 = None
        self.assertFalse(gp1 == gp2)

    def test_inequality_with_none(self):
        gp1 = Geoposition(52.5, 13.4)
        gp2 = None
        self.assertTrue(gp1 != gp2)

    def test_db_value_to_python_object(self):
        obj = PointOfInterest.objects.create(name='Foo', address='some where', city='city', zipcode='12345', position=Geoposition(52.5,13.4))
        poi = PointOfInterest.objects.get(id=obj.id)
        self.assertIsInstance(poi.position, Geoposition)
