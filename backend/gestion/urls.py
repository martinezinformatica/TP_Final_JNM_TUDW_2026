from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, PedidoViewSet, SolicitarCodigoView, VerificarCodigoView, LoginPersonalView, LoginUnificadoView

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'pedidos', PedidoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/solicitar-codigo/', SolicitarCodigoView.as_view(), name='solicitar-codigo'),
    path('auth/verificar-codigo/', VerificarCodigoView.as_view(), name='verificar-codigo'),
    path('auth/login/', LoginPersonalView.as_view(), name='login-personal'),
    path('auth/login-unificado/', LoginUnificadoView.as_view()),
]