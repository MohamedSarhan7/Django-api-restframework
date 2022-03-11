from django.urls import path,include
from .views import norest_nomodel, no_rest_from_model, FBV_list, FBV_pk
from .views import List_CBV, CVB_pk, mixins_list, mixins_pk,generics_list,generics_pk
from .views import viewsets_guest, viewsets_movie, viewsets_reservation, find_movie, new_reservation

from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("guests",viewsets_guest)
router.register("movies", viewsets_movie)
router.register("reservations", viewsets_reservation)
urlpatterns = [
    path("django/fun/1", norest_nomodel),
    path("django/fun/2", no_rest_from_model),


    path("api/fbv_list", FBV_list),
    path("api/fbv_pk/<int:pk>", FBV_pk),

    # CBV
    path("api/cbv", List_CBV.as_view()),
    path("api/cbv/<int:pk>", CVB_pk.as_view()),
    
    # Mixins
    path("api/mixins_list",mixins_list.as_view()),
    path("api/mixins_pk/<int:pk>",mixins_pk.as_view()),
    
    # Generics 
    
    path("api/gerecis_list", generics_list.as_view()),
    path("api/gerecis_pk/<int:pk>",generics_pk.as_view()),
    
    
    # viewsets
    path("api/viewsets/", include(router.urls)),
    
    
    #find movie
    
    path("findmovie",find_movie),
    
    # new reservation
    path("new_reservation",new_reservation),
    

]
