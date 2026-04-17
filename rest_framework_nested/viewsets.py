from __future__ import annotations

import contextlib
from typing import Any, Generic, Iterator, TypeVar

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model, QuerySet
from django.http import HttpRequest, QueryDict
from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer

T_Model = TypeVar('T_Model', bound=Model)


@contextlib.contextmanager
def _force_mutable(querydict: QueryDict | dict[str, Any]) -> Iterator[QueryDict | dict[str, Any]]:
    """
    Takes a HttpRequest querydict from Django and forces it to be mutable.
    Reverts the initial state back on exit, if any.
    """
    pass


class NestedViewSetMixin(Generic[T_Model]):
    def _get_parent_lookup_kwargs(self) -> dict[str, str]:
        """
        Locates and returns the `parent_lookup_kwargs` dict informing
        how the kwargs in the URL maps to the parents of the model instance

        For now, fetches from `parent_lookup_kwargs`
        on the ViewSet or Serializer attached. This may change on the future.
        """
        pass

    def get_queryset(self) -> QuerySet[T_Model]:
        """
        Filter the `QuerySet` based on its parents as defined in the
        `serializer_class.parent_lookup_kwargs` or `viewset.parent_lookup_kwargs`
        """
        pass

    def initial(self, request: Request, *args: Any, **kwargs: Any) -> None:
        """
        Adds the parent params from URL inside the children data available
        """
        pass
