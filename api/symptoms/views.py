from django.core.exceptions import FieldError
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from api.permissions import IsOauthAuthenticatedCustomer
from api.symptoms.models import Symptoms
from api.symptoms.serializer import SymptomsSerializer
from api.views import BaseAPIView


class SymptomsView(BaseAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedCustomer,)

    def get(self, request, pk=None):
        try:
            limit = int(request.query_params.get('limit', 10))
            offset = int(request.query_params.get('offset', 0))
            # category_id = request.query_params.get('category-id', None)
            # search = request.query_params.get('search', None)
            # publish = request.query_params.get('publish', None)
            # out_stock = request.query_params.get('out-of-stock', None)
            # low_thresh = request.query_params.get('low-thresh', None)
            # is_active = request.query_params.get('is-active', None)
            #  drop-dow params shows only parent products
            # listing = request.query_params.get('drop-down', None)

            query_set = Q(user_id=request.user.id)

            if pk:
                query_set &= Q(id=pk)
                query = Symptoms.objects.get(query_set)
                serializer = SymptomsSerializer(query)
                count = 1
            else:
                query = Symptoms.objects.filter(query_set).order_by('-id')

                serializer = SymptomsSerializer(
                    query[offset:limit + offset],
                    many=True,

                )
                count = query.count()
            return self.send_response(
                success=True,
                code='200',
                status_code=status.HTTP_200_OK,
                payload=serializer.data,
                count=count
            )
        except Symptoms.DoesNotExist:
            return self.send_response(
                success=False,
                code='422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='Symptoms Does`t Exist'
            )
        except FieldError as e:
            return self.send_response(
                success=False,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                code=f'422',
                description=str(e)
            )

        except Exception as e:
            return self.send_response(
                success=False,
                description=e
            )

    def post(self, request):
        try:
            serializer = SymptomsSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                validated_data["user_id"] = request.user.id
                serializer.save(**validated_data)
                return self.send_response(
                    success=True,
                    code=f'201',
                    status_code=status.HTTP_201_CREATED,
                    description='Symptom Added Successfully',

                )
            else:
                return self.send_response(
                    success=False,
                    code=f'422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description=serializer.errors
                )
        except FieldError:
            return self.send_response(
                code=f'500',
                description="Cannot resolve keyword given in 'order_by' into field"
            )

        except Exception as e:
            if hasattr(e.__cause__, 'pgcode') and e.__cause__.pgcode == '23505':
                if "StockKeepingUnit" in e.args[0]:
                    message = "Syptom exists in the system"
                else:
                    message = "Product with this name or slug already exists in the system."
                return self.send_response(
                    code=f'422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description=message
                )

            return self.send_response(
                code=f'500',
                description=str(e)
            )

    def put(self, request, pk=None):
        try:
            serializer = SymptomsSerializer(
                instance=Symptoms.objects.get(id=pk),
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return self.send_response(
                    success=True,
                    code=f'201',
                    status_code=status.HTTP_201_CREATED,
                    description='Symptom Updated Successfully',

                )
            else:
                return self.send_response(
                    success=False,
                    code=f'422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description=serializer.errors
                )
        except Symptoms.DoesNotExist:
            return self.send_response(
                success=False,
                code='422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='Symptom Does`t Exist'
            )

        except Exception as e:

            return self.send_response(
                success=False,
                description=e
            )


class DeleteSymptomsView(BaseAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedCustomer,)

    def get(self, request, pk=None):
        try:

            Symptoms.objects.get(id=pk, user_id=request.user.id).delete()
            return self.send_response(
                success=True,
                code='200',
                status_code=status.HTTP_200_OK,
                description='Symptoms Deleted Successfully'

            )


        except Symptoms.DoesNotExist:
            return self.send_response(
                success=False,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                code='422',
                description='Invalid Product id'
            )

        except Exception as e:
            return self.send_response(
                success=False,
                description=str(e)
            )
