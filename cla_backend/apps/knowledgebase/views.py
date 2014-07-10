from rest_framework import viewsets
from rest_framework import filters

from .models import Article, ArticleCategory
from .serializers import ArticleSerializer, ArticleCategorySerializer


class BaseArticleViewSet(viewsets.ReadOnlyModelViewSet):
    model = Article
    serializer_class = ArticleSerializer

    paginate_by = 20
    paginate_by_param = 'page_size'
    max_paginate_by = 100

    filter_backends = (
        filters.SearchFilter,
        filters.DjangoFilterBackend
    )

    filter_fields = ('article_category',)

    search_fields = ('organisation', 'service_name', 'description',
                     'keywords', 'when_to_use', 'type_of_service',
                     'address', 'article_category__name')


class BaseArticleCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    model = ArticleCategory
    serializer_class = ArticleCategorySerializer