from model_mommy.recipe import Recipe, seq, foreign_key

from ..models import Category, EligibilityCheck, Property, Finance, \
    Case, PersonalDetails


category = Recipe(Category,
    name=seq('Name'), order = seq(0)
)

finance = Recipe(Finance)

eligibility_check = Recipe(EligibilityCheck,
    category=foreign_key(category),
    dependants_young=5, dependants_old=6,
    your_finances=foreign_key(finance),
    partner_finances=foreign_key(finance)
)

property = Recipe(Property,
    eligibility_check=foreign_key(eligibility_check)
)

personal_details = Recipe(PersonalDetails)

case = Recipe(Case,
    eligibility_check=foreign_key(eligibility_check),
    personal_details=foreign_key(personal_details)
)