from datetime import datetime
from django.utils.formats import date_format
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status

from contracts.serializer import ContractSerializer
from .models import Contract
from clients.models import Client
from rest_framework import generics
import pandas as pd

class RequestFailed(APIException):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    default_detail = 'Data Import failed , Duplication of enteries.'

def filter_groups(group):
    return group.name not in ['X', '.','..','...']
def filter(name):
    return not len(name) < 12  and  name[0].isalpha()  and name[-1].isalpha()
def formatDate(date):
    date = datetime.strptime(date , '%d/%m/%Y')
    date = date.strftime('%Y-%m-%d')
    return date

class ImportExtractionDataView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES['excel']
        data = pd.read_excel(file,skiprows=3)
        # data['Date Effet'] = pd.to_datetime(data['Date Effet'], format='mixed').dt.strftime('%y-%m-%d')
        last_extraction = Contract.objects.order_by('-effect_date').first()
        last_extraction_serializer = ContractSerializer(instance=last_extraction).data
        if last_extraction is not None :
            recent_date = last_extraction_serializer['effect_date']
            pd_date= formatDate(data['Date Effet'].min())
            if recent_date > pd_date:
                raise RequestFailed()
        grouped = data.groupby('Numéro de contribuable')
        filtered_groups = grouped.filter(filter_groups)
        filtered_groups = filtered_groups[filtered_groups['Numéro de contribuable'].apply(filter)]
        info_clients = filtered_groups[['Numéro de contribuable' , 'Civilité','Nom','Prénom','Adresse']]
        info_clients.reset_index(inplace=True)
        info_contracts = filtered_groups[['Numéro de contribuable' , 'Agence','Date Emission','Prénom','Grande Branche','Branche', 'Produit', 'N° Police','Date Effet',
       'Date Echéance', 'N° Assuré', 'Prime Nette', 'Acc Cie',
       'Acc App']]
        for client_info in info_clients.T.to_dict().values():
            if not Client.objects.filter(Taxpayer_number  = client_info['Numéro de contribuable']).exists():
                client = Client.objects.create(Taxpayer_number=client_info['Numéro de contribuable'] , civil_status=client_info['Civilité'],first_name='',last_name=['Prénom'],address=['Nom'])
        for contract in info_contracts.T.to_dict().values():
            date_create = formatDate(contract['Date Emission'])
            effect_date = formatDate( contract['Date Effet'])
            end_date = formatDate( contract['Date Echéance'])
            Contract.objects.create(Taxpayer_number=contract["Numéro de contribuable"] ,branch=contract['Branche'] , big_branch=contract['Grande Branche'] , product=contract['Produit'] ,agent = contract['Agence'] , date_create=date_create ,effect_date =effect_date , end_date=end_date ,Police_number=contract['N° Police'])
        return Response(data={'msg':"Successully Imported Extraction Data"})