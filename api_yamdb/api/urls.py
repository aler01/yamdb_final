from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import RegisterViewSet, TokenView, UsersViewSet

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitlesViewSet)

router_v1 = DefaultRouter()
router_v1.register(r'users', UsersViewSet, basename='users')
router_v1.register(r'titles', TitlesViewSet, basename='Title')
router_v1.register(r'genres', GenreViewSet, basename='Genre')
router_v1.register(r'categories', CategoryViewSet, basename='Category')
router_v1.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', RegisterViewSet.as_view({'post': 'create'}),
         name='get_confirmation_code'),
    path('v1/auth/token/', TokenView.as_view({'post': 'create'}),
         name='get_token'),
]
