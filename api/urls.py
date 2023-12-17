from django.urls import path ,include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router=DefaultRouter()
router.register('guests',views.viewsets_guest)
router.register('movies',views.viewsets_movie)
router.register('reserv',views.viewsets_reservation)


urlpatterns = [
    path('lista/',views.FBV_list),
    path('pk/<int:pk>/',views.FBV_pk),
    path('class/',views.CBV_list.as_view()),
    path('class/<int:pk>',views.CBV_PK.as_view()),
    path('mixi/',views.Mixins_list.as_view()),
    path('mixi/<int:pk>',views.Mixins_Pk.as_view()),
    path('generic/',views.generics_list.as_view()),
    path('generic/<int:pk>',views.generics_Pk.as_view()),
    path('vwset/',include(router.urls)),
    path('findmovie/',views.find_movie),
    path('new reservation/',views.reservation_movie),

    path('api_auth/',include('rest_framework.urls')),
    #token_auth
    path('api_token_auth',obtain_auth_token),
    path('post/<int:pk>',views.Post_pk.as_view()),

] 