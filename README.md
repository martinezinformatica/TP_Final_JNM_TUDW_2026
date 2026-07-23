Natural Mystic 1.0 - Sistema de Gestión Gastronómica y Menú Digital

Descripción del Proyecto

Natural Mystic es una aplicación web SPA (Single Page Application) diseñada para la gestión operativa y comercial de locales cerveceros. El sistema ofrece un flujo de trabajo integrado entre el cliente y el personal del establecimiento:

Menú y Carta Digital: Permite a los clientes loguearse por medio del telefono explorar productos, consultar disponibilidad de stock, armar su carrito para enviar el pedido.
Control de Cocina: Panel en tiempo real para visualizar pedidos entrantes, gestionar los estados de preparación y liberar mesas una vez finalizado el servicio.
Administración y Autenticación: Módulo de gestión para actualizar la carta, precios y stock disponible, además de un control de acceso restringido para el personal del local.

La arquitectura completa está dockerizada con Docker Compose, articulando un backend en Django REST Framework, un frontend en Vue.js, y una base de datos PostgreSQL.

Estructura del Proyecto:

TP_FINAL/
├── backend/ # Código fuente del servidor (Django REST Framework)
├── frontend/ # Código fuente de la interfaz web (Vue.js)
├── docker-compose.yml # Configuración y orquestación de servicios
├── .gitignore # Reglas de exclusión para Git
└── README.md # Documentación principal del proyecto

Requisitos Previos:

Para ejecutar la aplicación únicamente se requiere tener instalado en el sistema:

Docker Desktop o Docker Engine

Plugin de Docker Compose

No es necesario instalar Python, Node.js ni PostgreSQL en la computadora cliente, ya que todo el entorno se ejecuta aislado dentro de los contenedores.

Variables de Entorno
El proyecto está configurado para tomar los parámetros de entorno definidos en el archivo docker-compose.yml. Si se requiere modificar credenciales o conexiones, los valores predeterminados del sistema son:

Base de Datos y Backend
DB_NAME: proyecto_db

DB_USER: ana_user

DB_PASSWORD: ana_password

DB_HOST: db

Puerto Backend: 8000

Frontend
Entorno: Vite dev server

Puerto Frontend: 5173

Despliegue y Ejecución con Docker:

Levantar la infraestructura completa

Desde la raíz del proyecto (TP_FINAL), donde se ubica el archivo docker-compose.yml, ejecutá el siguiente comando para construir las imágenes y levantar los servicios:

docker compose up --build -d //Construir y levantar los contenedores con Docker Compose:
docker compose exec backend python manage.py migrate //Ejecutar las migraciones de la base de datos:
docker compose exec backend python manage.py loaddata datos_iniciales.json //Cargar los datos iniciales y usuarios de prueba
docker compose exec backend python manage.py shell -c "from django.contrib.auth.models import User; u1=User.objects.get(username='admin'); u1.set_password('admin1234'); u1.save(); u2=User.objects.get(username='2984111222'); u2.set_password('cocinero*'); u2.save(); u3=User.objects.get(username='2984333444'); u3.set_password('administrador*'); u3.save(); print('Usuarios iniciales configurados exitosamente')"

Usuarios:
SuperUsuario: Loguin: admin/Contraseña admin1234
Administrdor: Loguin: 2984333444/Contraseña: administrador*
Cocina: Loguin: 2984111222/Contraseña: cocinero*

Una vez finalizada la construcción, los servicios estarán disponibles en los siguientes accesos:

Frontend (Interfaz Web): http://localhost:5173

Backend (API REST): http://localhost:8000/api/

http://localhost:8000/admin/

Monitoreo de Logs

Para inspeccionar los registros de salida de cada servicio en tiempo real

Ver todos los logs:

docker compose logs -f

Ver logs de un servicio específico (ej. Backend o Frontend):

docker logs -f django_backend
docker logs -f vue_frontend

Detener la Aplicación

Para apagar los contenedores y liberar los puertos sin borrar los datos guardados en la base de datos

docker compose down

Si además deseás eliminar el volumen persistente de la base de datos para realizar una instalación limpia desde cero:

docker compose down -v

Licencia
Este proyecto es parte del Trabajo Práctico Final de la carrera y es de uso privado para la gestión del establecimiento Natural Mystic. Todos los derechos reservados.
