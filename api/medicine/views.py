from datetime import date
import datetime

from django.core.exceptions import FieldError
from django.db.models import Q, Prefetch
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from api.medicine.models import Medicine, DosageTime, DosageHistory
from api.medicine.serializer import MedicineSerializer, ImageSerializer
from api.permissions import IsOauthAuthenticatedCustomer
from api.views import BaseAPIView


class MedicineView(BaseAPIView):
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

            query_set = Q(user_id=request.user.id, is_active=True)

            if pk:
                query_set &= Q(id=pk)
                query = Medicine.objects.prefetch_related(
                    Prefetch(
                        "medicine_dosage",
                        queryset=DosageTime.objects.filter(is_active=True)
                    )
                ).get(query_set)
                serializer = MedicineSerializer(query)
                count = 1
            else:
                query = Medicine \
                    .objects \
                    .prefetch_related(
                    Prefetch(
                        "medicine_dosage",
                        queryset=DosageTime.objects.filter(is_active=True)
                    )
                ) \
                    .filter(query_set) \
                    .order_by('-id')

                serializer = MedicineSerializer(
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
        except Medicine.DoesNotExist:
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
            serializer = MedicineSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                validated_data["user_id"] = request.user.id
                serializer.save(**validated_data)
                return self.send_response(
                    success=True,
                    code=f'201',
                    status_code=status.HTTP_201_CREATED,
                    description='Medicine Added Successfully',

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
                return self.send_response(
                    code=f'422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description=str(e)
                )

            return self.send_response(
                code=f'500',
                description=str(e)
            )

    def put(self, request, pk=None):
        try:
            serializer = MedicineSerializer(
                instance=Medicine.objects.get(id=pk),
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return self.send_response(
                    success=True,
                    code=f'201',
                    status_code=status.HTTP_201_CREATED,
                    description='Medicine Updated Successfully',

                )
            else:
                return self.send_response(
                    success=False,
                    code=f'422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description=serializer.errors
                )
        except Medicine.DoesNotExist:
            return self.send_response(
                success=False,
                code='422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='Medicine Does`t Exist'
            )

        except Exception as e:
            if hasattr(e.__cause__, 'pgcode') and e.__cause__.pgcode == '23505':
                return self.send_response(
                    code=f'422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description=str(e)
                )

            return self.send_response(
                success=False,
                description=e
            )


class DeleteMedicineView(BaseAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedCustomer,)

    def get(self, request, pk=None):
        try:

            if Medicine.objects.filter(id=pk, user_id=request.user.id).update(is_active=False):
                return self.send_response(
                    success=True,
                    code='200',
                    status_code=status.HTTP_200_OK,
                    description='Medicine Deleted Successfully'

                )

            else:
                return self.send_response(
                    success=False,
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    code='422',
                    description='Invalid Medicine id'
                )


        except Exception as e:
            return self.send_response(
                success=False,
                description=str(e)
            )


class DoseIntakeView(BaseAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedCustomer,)

    def get(self, request, pk=None):
        try:
            dat = request.query_params.get('date', date.today())

            obj, is_created = DosageHistory.objects.get_or_create(date=dat,
                                                                  dosage_id=pk)
            if is_created:
                return self.send_response(
                    success=True,
                    status_code=status.HTTP_200_OK,
                    description='Dose Intake Successfully'
                )
            else:
                return self.send_response(
                    success=False,
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    code='422',
                    description='Response already recorded'
                )
        except Exception as e:
            return self.send_response(
                success=False,
                description=str(e)
            )


class ImageUploadView(BaseAPIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        try:
            serializer = ImageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return self.send_response(
                    success=True,
                    code=status.HTTP_201_CREATED,
                    payload={
                        "name": serializer.instance.image.name,
                        "url": serializer.instance.image.url
                    },
                    status_code=status.HTTP_201_CREATED,
                    description=('Image Uploaded')
                )
            else:
                return self.send_response(
                    code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description=('Unable to upload image. Try again.'),
                    exception=serializer.errors
                )
        except Exception as e:
            return self.send_response(
                description=str(e)
            )
