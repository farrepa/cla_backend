from django.contrib import admin

from .models import Article, ArticleCategoryMatrix, TelephoneNumber


class TelephoneNumberInline(admin.TabularInline):
    model = TelephoneNumber


class ArticleCategoryMatrixInline(admin.TabularInline):
    model = ArticleCategoryMatrix


class ArticleAdmin(admin.ModelAdmin):
    actions = None
    inlines = [TelephoneNumberInline, ArticleCategoryMatrixInline]
    ordering = ["service_name"]

    fields = (
        "resource_type",
        "service_name",
        "service_tag",
        "organisation",
        "website",
        "email",
        "description",
        "public_description",
        "how_to_use",
        "when_to_use",
        "address",
        "opening_hours",
        "keywords",
        "geographic_coverage",
        "type_of_service",
        "accessibility",
    )
    list_display = ("service_name", "resource_type")
    search_fields = [
        "service_name",
        "organisation",
        "description",
        "how_to_use",
        "when_to_use",
        "keywords",
        "type_of_service",
    ]


class ArticleCategoryMatrixAdmin(admin.ModelAdmin):
    list_display = ("service_name", "category_name", "preferred_signpost")
    actions = None
    list_editable = ("preferred_signpost",)
    list_display_links = ("service_name",)
    search_fields = ["article_category__name", "article__service_name"]
    ordering = ("article_category__name", "-preferred_signpost", "article__service_name")

    def service_name(self, obj):
        return obj.article.service_name

    def category_name(self, obj):
        return obj.article_category.name


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategoryMatrix, ArticleCategoryMatrixAdmin)
