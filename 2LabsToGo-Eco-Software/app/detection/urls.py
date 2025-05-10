from django.urls import path
from .views import DetectionView , ImportCSV, DetectionDetail, TakeImage, GetConfig, DeleteImage, DeleteImages, Image_Process, WhiteBalance
from finecontrol.views import MethodList
urlpatterns = [
    path('capture/', DetectionView.as_view(), name='capture'),
    path('capture/list', MethodList.as_view(), name='method_list'),
    path('capture/save/', DetectionDetail.as_view(), name='detection_element'),
    path('capture/load/<int:id>/', DetectionDetail.as_view(), name='detection_element'),
    path('capture/takeimage', TakeImage.as_view(), name='take_image'),
    path('capture/getconfig/<int:id>/', GetConfig.as_view(), name='get_config'),
    path('capture/delete/<int:id>/', DeleteImage.as_view(), name='delete_image'),
    path('capture/deleteall/<int:id>/', DeleteImages.as_view(), name='delete_all_images'),
    path('imageProcess/', Image_Process.as_view(), name = 'imageProcess'),
    path('imageProcess/whitebalance/', WhiteBalance.as_view(), name = 'whitebalance'),   
    path('import_csv/', ImportCSV.as_view(), name='import_csv'),
    
]
