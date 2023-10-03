from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('/<int:item_id>', views.item, name="content"),
]

# cahighschools.org/archive?page=5
# cahighschools.org/archive/598
# cahighschools.org/archive/contribute
# cahighschools.org/archive/submit

# 1. users and site moderators will never know your full name, this is only accessible to site
# admins if your account has been flagged for unethical practices.


# title
# tags
    # subject - 
        # english
            # format - 
                # essay
                # paragraph
                # literature
                # general
                # misc

            # type -
                # fiction
                # non-fiction
                # historical
                # informative
                # research
        # biology, chemistry, etc

    # grade - 9, 10, 11, 12


# description
# a 255 letter description on how you would describe this post