# -*- coding: utf-8 -*-


class BaseModel(object):

    @property
    def modifiable_fields(self):
        fields = []
        un_modifiable_fields = getattr(self, 'un_modifiable_fields', [])
        for field in self._meta.fields:
            if field.name not in un_modifiable_fields:
                fields.append(field.name)
        return fields.remove('id') if id in fields else fields
