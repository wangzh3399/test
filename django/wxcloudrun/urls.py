"""wxcloudrun URL Configuration

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

from wxcloudrun import views
#from django.conf.urls import url
from django.urls import re_path as url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.static import serve
urlpatterns = [
    # 计数器接口
        #url(r'^admin/', admin.site.urls),
    #url(r'^chaining/', include('smart_selects.urls')),
    #url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    #url(r'^$',index),
    #url(r'^index$',index),
    #url(r'^category/(?P<category_id>[0-9]+)/(?P<page>[0-9]+)$',category),
    #url(r'^detail/(?P<product_id>[0-9]+)$',detail),
    #url(r'^standard/(?P<product_id>[0-9]+)$',standard),
    #url(r'^service/(?P<product_id>[0-9]+)$',service),
    #url(r'^commetList/(?P<product_id>[0-9]+)$',commetList),
    #url(r'^productOption/(?P<product_id>[0-9]+)$',productOption),

    #url(r'^active$',active),
    #url(r'^newer/(?P<newer_id>[0-9]+)$',newer),
    #url(r'^crowd/(?P<crowd_id>[0-9]+)$',crowd),
    #url(r'^group/(?P<group_id>[0-9]+)$',group),
    #url(r'^limit/(?P<limit_id>[0-9]+)$',limit),
    #url(r'^speed/(?P<speed_id>[0-9]+)$',speed),
    #url(r'^append$',append),
    #url(r'^coupon/(?P<coupon_id>[0-9]+)$',coupon),
    #url(r'^getCoupon/(?P<coupon_id>[0-9]+)$',getCoupon),

    
    #url(r'^shopcart$',shopcart),
    #url(r'^delShopCartItem/(?P<shopcartitem_id>[0-9]+)$',delShopCartItem),
    #url(r'^changeShopCartItemCount/(?P<shopcartitem_id>[0-9]+)/(?P<count>[0-9]+)$',changeShopCartItemCount),
    #url(r'^addInCart$',addInCart),
    #url(r'^getShopCartItemCount$',getShopCartItemCount),
    #url(r'^selectAll/(?P<bool>[0-9])$',selectAll),
    #url(r'^getActiveCount$',getActiveCount),   
    #url(r'^myself$',myself),

    url(r'^order$',views.order),
    #url(r'^orderConfirm$',orderConfirm),
    #url(r'^useCoupon$',useCoupon),
    #url(r'^doUseMyCoupon/(?P<mycoupon_id>[0-9]+)$',doUseMyCoupon),
     
    #url(r'^takeOrderDirect$',takeOrderDirect),
    #url(r'^paySuccessPage$',paySuccessPage),  
    #url(r'^wepay_result$',wepay_result),
    #url(r'^orderdetail/(?P<order_id>[0-9]+)$',orderDetail),
    #url(r'^commet/(?P<product_id>[0-9]+)$',commet),
    #url(r'^commetSuccess$',commetSuccess),

    #url(r'^address$',address),
    #url(r'^newAddress/(?P<url>\w+)$',newAddress),
    #url(r'^delAddress/(?P<address_id>[0-9]+)$',delAddress),
    
    #url(r'^myservice$',myservice),
    #url(r'^collection$',collection),
    #url(r'^coin$',coin),
    #url(r'^coinDetail$',coinDetail),
    #url(r'^mycoupon$',myCoupon),
    #url(r'^setup$',setup),

    #url(r'^ajax/get_signature$', jsapi_signature),
    #url(r'^ajax/getCountry/(?P<region_id>[0-9]+)$',getCountry),
    #url(r'^ajax/getMoney$', getMoney),
    #url(r'^ajax/isUseCoin/(?P<boolString>\w+)$',isUseCoin),
    #url(r'^ajax/collect/(?P<product_id>[0-9]+)$', collect),
    #url(r'^ajax/getShopCartStatus$', getShopCartStatus),
    #url(r'^ajax/setDefaultAddress/(?P<address_id>[0-9]+)/(?P<url>\w+)$',setDefaultAddress),
    #url(r'^ajax/selectCartItem/(?P<shopcartitem_id>[0-9]+)$',selectCartItem),
    #url(r'^ajax/unselectCartItem/(?P<shopcartitem_id>[0-9]+)$',unselectCartItem),




    # 获取主页
    url(r'^^wxui(/)?$', views.index),
    url(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    url(r'^myself$',views.myself),
    url(r'^condition$',views.conditionManage),
    url(r'^condition/create',views.createcondition),
    url(r'^strategy$',views.strategyManage),
    url(r'^strategy/create',views.createstrategy),
    url(r'^stockpool$',views.stockpoolManage),
    url(r'^stockpool/create',views.createstockpool),
    url(r'^notice$',views.noticeManage), 
    url(r'^notice/create',views.createnotice),
    url(r'^monitortask$',views.monitortaskManage), 
    url(r'^monitortask/create',views.createmonitortask),

    url(r'^strategy/new$',views.strategyNew),
    url(r'^strategy/newFilterShow$',views.strategyNewFilterShow), 
    url(r'^strategy/createOrUpdate$',views.strategyCreateOrUpdate),
    url(r'^strategy/newBuyInShow$',views.strategyNewBuyInShow),
    url(r'^strategy/Management$',views.strategyManagement),
    url(r'^personal$',views.personal),
    url(r'(/)?$', views.wxapi),
    url(r'', views.default)

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)