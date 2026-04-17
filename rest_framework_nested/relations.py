"""
Serializer fields that deal with relationships with nested resources.

These fields allow you to specify the style that should be used to represent
model relationships with hyperlinks.
"""
from __future__ import annotations

from functools import reduce
from typing import Any, Generic, TypeVar

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from rest_framework.relations import HyperlinkedRelatedField, ObjectTypeError, ObjectValueError
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request


T_Model = TypeVar('T_Model', bound=Model)


class NestedHyperlinkedRelatedField(HyperlinkedRelatedField, Generic[T_Model]):
    lookup_field = 'pk'
    parent_lookup_kwargs = {
        'parent_pk': 'parent__pk'
    }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.parent_lookup_kwargs = kwargs.pop('parent_lookup_kwargs', self.parent_lookup_kwargs)
        super().__init__(*args, **kwargs)

    def get_url(self, obj: Model, view_name: str, request: Request, format: str | None) -> str | None:
        """
        Given an object, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        pass

    def get_object(self, view_name: str, view_args: list[Any], view_kwargs: dict[str, Any]) -> T_Model:
        """
        Return the object corresponding to a matched URL.

        Takes the matched URL conf arguments, and should return an
        object instance, or raise an `ObjectDoesNotExist` exception.
        """
        pass

    def use_pk_only_optimization(self) -> bool:
        pass

    def to_internal_value(self, data: Any) -> T_Model:
        pass


class NestedHyperlinkedIdentityField(NestedHyperlinkedRelatedField[T_Model]):
    def __init__(self, view_name: str | None = None, **kwargs: Any) -> None:
        assert view_name is not None, 'The `view_name` argument is required.'
        kwargs['read_only'] = True
        kwargs['source'] = '*'
        super().__init__(view_name=view_name, **kwargs)
