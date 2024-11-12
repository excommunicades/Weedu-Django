from django.urls import path

from api.api_actions.views.level_views import(
    GetXp
)

from api.api_actions.views.achievement_views import(
    Achievements
)

# router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('get-xp/', GetXp.as_view(), name="get_user_xp"),
    path('achievs/', Achievements.as_view(), name='create_achievement'),
    path('achievs/<int:pk>/', Achievements.as_view(), name='create_achievement'),
]
