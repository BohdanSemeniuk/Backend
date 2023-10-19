class EnablePATCHMethodMixin:
    """
    Enable partial updates(PATCH method).
    """
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
