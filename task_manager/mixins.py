class QuerySetOptimizeMixin:
    select_related_fields = []
    prefetch_related_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self, 'select_related_fields'):
            queryset = queryset.select_related(*self.select_related_fields)
        if hasattr(self, 'prefetch_related_fields'):
            queryset = queryset.prefetch_related(*self.prefetch_related_fields)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'model'):
            queryset = self.get_queryset()
            context[self.get_context_object_name(queryset)] = queryset
        return context
