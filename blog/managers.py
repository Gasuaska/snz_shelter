from django.db import models
from django.db.models import Count
from django.utils import timezone


class PostQuerySet(models.QuerySet):

    def published(self):
        return self.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True)

    def select_related_set(self):
        return self.select_related(
            'category',
            'author'
        )

    def comment_count(self):
        return (self.annotate(comment_count=Count('comments'))
                .order_by(*self.model._meta.ordering))