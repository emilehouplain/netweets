"""netweets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from game import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #Hors DB
    path('formulaire', views.formulaire, name="formulaire"),
    path('', views.formulaire2, name="formulaire2"),
    path('formulaire_test', views.formulaire_test, name="formulaire_test"),


    #Analyse Compte Twitter

    #Analyse Tweets
    path('analyse_tweets/<int:compteTwitter_id>', views.analyse_tweets, name="analyse_tweets"), #int = id du compteTwitter analysé : meme modèle à utiliser pour le reste du DB ?
    path('tables/<int:compteTwitter_id>', views.tables, name="tables"), #int = id du compteTwitter analysé : meme modèle à utiliser pour le reste du DB ?
    path('analyse2/<int:compteTwitter_id>', views.analyse2, name="analyse2"),
    path('export/csv/<int:compteTwitter_id>', views.analyse2_export_csv, name='analyse2_export_csv'),
    path('geolocalisation/<int:compteTwitter_id>', views.geolocalisation, name="geolocalisation"), 
    path('reports/<int:compteTwitter_id>', views.reports, name="reports"),
	path('nuage/<int:compteTwitter_id>', views.nuage, name="nuage"),
	path('sentimental/<int:compteTwitter_id>', views.sentimental, name="sentimental"),
	path('export/csv2/<int:compteTwitter_id>', views.sentimental_export_csv, name='sentimental_export_csv'),
    path('export/csv3/<int:compteTwitter_id>', views.nuage_export_csv, name='nuage_export_csv'),
    path('analyse_semantique/<int:compteTwitter_id>', views.analyse_semantique, name='analyse_semantique'),

    #Aide
    path('faq/<int:compteTwitter_id>', views.faq, name="faq"),
    path('glossaire/<int:compteTwitter_id>', views.glossaire, name="glossaire"),

    #Informations
    path('maj/<int:compteTwitter_id>', views.maj, name="maj"),
	path('roadmap/<int:compteTwitter_id>', views.roadmap, name="roadmap"),


    #Compte utilisateur
    path('parametres/<int:compteTwitter_id>', views.parametres, name="parametres"),

    #Compte utilisateur
    path('analyse/presidentielle2022/<int:compteTwitter_id>', views.presidentielle2022, name="presidentielle2022")




	#path('moulinette/<int:compteTwitter_id>', views.moulinette, name='moulinette'),
]
