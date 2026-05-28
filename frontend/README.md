# 🍺 Natural Mystic - Sistema de Gestión Gastronómica y Carta Digital

Este repositorio contiene el desarrollo de la plataforma web Full Stack para la cervecería **Natural Mystic** (General Roca - Fiske Menuco). El sistema está diseñado con una arquitectura desacoplada para agilizar la experiencia del cliente en el salón y optimizar la administración del negocio mediante un panel de control inteligente en tiempo real.

---

## 🚀 Objetivos del Proyecto

- **Experiencia de Usuario Integrada**: Permitir que los clientes escaneen la mesa, visualicen la carta interactiva con control de stock y despachen pedidos directo a la cocina.
- **Panel de Administración Centralizado**: Proveer una interfaz administrativa simétrica y compacta que organice de forma eficiente el alta de productos/mesas, la edición en línea y la visualización de analíticas clave.
- **Seguridad y Autenticación Robusta**: Restringir el acceso a los módulos críticos (`Administrador` y `Cocina`) mediante validación de credenciales basada en estándares modernos de la industria.

---

## 🛠️ Stack Tecnológico Pensado

El ecosistema de la aplicación se estructura con herramientas modernas, escalables y de alto rendimiento:

### 🖥️ Backend (API REST)

- **Python**: Lenguaje base para el desarrollo de la lógica del servidor.
- **Django & Django REST Framework (DRF)**: Framework robusto utilizado para el modelado de datos relacionales, el ORM y la exposición segura de los endpoints de `Productos`, `Mesas` y `Pedidos`.
- **PostgreSQL**: Motor de base de datos relacional para garantizar la persistencia e integridad de los registros históricos del bar.

### 🎨 Frontend (SPA)

- **Vue 3 (Composition API)**: Framework progresivo para estructurar una interfaz ágil, modular y reactiva.
- **Vite**: Entorno de desarrollo rápido para compilar y empaquetar el frontend con tiempos de carga óptimos.
- **Pinia**: Almacén de estado global para centralizar la gestión del carrito de compras del cliente y la sesión activa del personal.
- **Axios**: Cliente HTTP encargado de la comunicación asíncrona con el backend.
- **CSS3 (Custom Properties)**: Diseño temático a medida ("Mystic Dark") con fuentes monoespaciadas y acentos en dorado.

---

## 🔐 Seguridad e Interoperabilidad: Implementación de JWT

Para proteger los datos sensibles del negocio y segmentar los roles de usuario (Administradores, Mozos y Cocineros), el sistema implementará **JSON Web Tokens (JWT)** mediante la librería `django-rest-framework-simplejwt`:

- **Autenticación Desacoplada**: El backend no guardará sesiones en el servidor (Stateless). Cuando el usuario inicie sesión, recibirá un `access token` y un `refresh token`.
- **Persistencia Segura**: El frontend almacenará los tokens en el almacenamiento del navegador (`localStorage`) para mantener la sesión activa sin interrumpir la experiencia.
- **Interoperabilidad**: Cada petición realizada desde Vue mediante **Axios** inyectará el token automáticamente en las cabeceras HTTP (`Authorization: Bearer <token>`) para validar los permisos de escritura y lectura en las secciones protegidas.

---

## 📋 Detalle de la Estructura de Administración Implementada

El panel de control (`Admin.vue`) se organizó bajo una matriz visual simétrica optimizada para el administrador:

1. **Gestión Operativa (Bloque Superior)**: Formularios en paralelo para la creación inmediata de nuevos productos (control de nombre, precio y stock) y el alta dinámica de mesas.
2. **Monitoreo y Control (Bloque Central - Layout de 2 Cuadros)**:
   - **Cuadro Izquierdo (Lista de Productos)**: Vista unificada que permite modificar precios, editar stock en línea o eliminar artículos, confinada en un contenedor con scroll interno para evitar desplazamientos infinitos.
   - **Cuadro Derecho (🏆 Top 10 Más Vendidos)**: Componente reactivo computado en tiempo real que procesa el historial de pedidos entregados y despliega un ranking automático con los productos más exitosos del bar para la toma de decisiones comerciales.
3. **Historial General (Bloque Inferior)**: Registro cronológico de auditoría de pedidos con estado "Entregado", detallando totales, número de mesa y desglose de ítems.

---

## 📈 Estado y Próximos Pasos

- [x] Maquetado estético e interfaz adaptativa de la Carta Digital.
- [x] Rediseño y balanceo del Panel de Administración (Grilla simétrica y Top 10).
- [ ] Configuración del backend de Django para la emisión de endpoints JWT (`/api/token/` y `/api/token/refresh/`).
- [ ] Integración de los interceptores de Axios en Vue para adjuntar los tokens de seguridad a las rutas restringidas.
- [ ] Estabilización del enrutamiento nativo con `Vue Router`.

---

_Desarrollado para Natural Mystic — Calidad y control en cada pinta._
