from django.contrib import admin

from .models import (
    Category,
    Case,
    EligibilityCheck,
    PersonalDetails,
    Property,
    Person,
    EODDetails,
    EODDetailsCategory,
    MatterType,
)

from .admin_support.forms import CategoryModelForm


class CategoryModelAdmin(admin.ModelAdmin):
    form = CategoryModelForm


class EODDetailsCategoryAdmin(admin.TabularInline):
    model = EODDetailsCategory
    readonly_fields = ("category", "is_major")
    extra = 0


class EODDetailsAdmin(admin.ModelAdmin):
    inlines = (EODDetailsCategoryAdmin,)


class CaseAdmin(admin.ModelAdmin):
    raw_id_fields = (
        "eligibility_check",
        "diagnosis",
        "personal_details",
        "thirdparty_details",
        "adaptation_details",
        "from_case",
    )


admin.site.register(Category, CategoryModelAdmin)
# admin.site.register(Question)
# admin.site.register(Answer)
admin.site.register(Case, CaseAdmin)
admin.site.register(EligibilityCheck)
admin.site.register(PersonalDetails)
admin.site.register(Property)
admin.site.register(Person)
admin.site.register(EODDetails, EODDetailsAdmin)
admin.site.register(MatterType)
