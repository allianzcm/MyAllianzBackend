from App.urls import path
from .views import ImportExtractionDataView


urlpatterns = [
    path('upload_extractions' ,ImportExtractionDataView.as_view() , name='ImportExtractionDataView' )    
]