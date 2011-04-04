from django.db import models


class Geoposition(object):
    def __init__(self, latitude, longitude):
        self.latitude = float(latitude)
        self.longitude = float(longitude)
    
    def __unicode__(self):
        return "%s,%s" % (self.latitude, self.longitude)


class GeopositionField(models.CharField):
    description = "A geoposition (latitude and longitude)"
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 42
        super(GeopositionField, self).__init__(*args, **kwargs)
    
    def get_internal_type(self):
        return "CharField"
    
    def to_python(self, value):
        if isinstance(value, Geoposition):
            return value
        
        args = value.split(',')
        return Geoposition(*args)
    
    def get_prep_value(value):
        return unicode(value)
    
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^geoposition\.fields\.GeopositionField"])
