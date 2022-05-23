from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .routers import CustomWithoutUpdateRouter
from .views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                    ReviewViewSet, TitlesViewSet, get_token, signup)

router = DefaultRouter()
custom_router = CustomWithoutUpdateRouter()
custom_router.register('users', UserViewSet, basename='users')
custom_router.register('categories', CategoriesViewSet, basename='categories')
custom_router.register('genres', GenresViewSet, basename='genres')
custom_router.register('titles', TitlesViewSet, basename='titles')
custom_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
custom_router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/?",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(custom_router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
]
