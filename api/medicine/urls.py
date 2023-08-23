from django.urls import path

from api.medicine.views import MedicineView, DeleteMedicineView

urlpatterns = [
    path("", MedicineView.as_view()),
    path("<int:pk>", MedicineView.as_view()),
    path("delete/<int:pk>", DeleteMedicineView.as_view())
]
