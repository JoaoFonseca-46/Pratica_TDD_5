from django.urls import path

from core.views import (
    login,
    logout,
    home,
    listar_links,
    cadastrar_link,
    editar_link,
    excluir_link
)

urlpatterns = [

    path('login/', login, name='login'),

    path('logout/', logout, name='logout'),

    path('index/', home, name='index'),

    path('links/', listar_links, name='listar_links'),

    path('cadastrar/', cadastrar_link, name='cadastrar_link'),

    path('editar/<int:id>/', editar_link, name='editar_link'),

    path('excluir/<int:id>/', excluir_link, name='excluir_link'),

    path('', home, name='home')

]