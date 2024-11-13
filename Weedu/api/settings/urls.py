from django.urls import path

from api.api_actions.views.level_views import(
    GetXp
)

from api.api_actions.views.achievement_views import(
    Achievements,
    Get_User_Achievement
)
from api.api_actions.views.award_views import (
    Awards,
    Get_User_Award
)

# router.register(r'users', UserViewSet, basename='user')


urlpatterns = [

    # user actions
    path('get-xp/', GetXp.as_view(), name="get_user_xp"),
    
    # achievements actions
    path('achievs/', Achievements.as_view(), name='achievment_actions'),
    path('achievs/<int:pk>/', Achievements.as_view(), name='achievment_actions_obj'),
    path('get-achiev/', Get_User_Achievement.as_view(), name='achievment_actions_obj'),
    # awards actions
    path('awards/', Awards.as_view(), name='award_actions'),
    path('awards/<int:pk>/', Awards.as_view(), name='award_actions_obj'),
    path('get-award/', Get_User_Award.as_view(), name='achievment_actions_obj'),
]
