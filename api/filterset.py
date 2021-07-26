from django_filters import Filter, FilterSet
from django_filters.constants import EMPTY_VALUES

class ListFilter(Filter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        value_list = value.split(",")
        qs = super().filter(qs, value_list)
        return qs

class ProductListFilter(FilterSet):
    category_name_fr = ListFilter(field_name="category_name_fr", lookup_expr="in")