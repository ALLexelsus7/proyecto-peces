# Prototipo Distribuido de Microservicio gRPC para Gestión de Catálogo de Peces Exóticos

## 1. Descripción General

Este proyecto constituye un prototipo funcional y academically-oriented de un **microservicio distribuido de alta eficiencia** diseñado para la gestión estructurada de un catálogo de peces exóticos. El sistema implementa operaciones CRUD completas mediante la arquitectura **gRPC sobre HTTP/2**, reemplazando los protocolos REST tradicionales con un esquema de comunicación optimizado para bajo latencia y alto throughput.

### Propósito del Sistema

El prototipo demuestra la implementación de un servicio backend que:

- **Persiste estructuradamente** un catálogo de especies exóticas clasificadas por propósito (ornamental o de consumo) y hábitat natural (zonas de profundidad oceánica).
- **Garantiza integridad de datos** mediante políticas de borrado lógico y lógica defensiva para la evolución de esquemas.
- **Optimiza comunicación distribuida** mediante gRPC, eliminando el overhead de HTTP/REST tradicional.
- **Implementa persistencia NoSQL** con MongoDB, permitiendo flexibilidad en la estructura de documentos.

### Alcance Académico

Este proyecto es un entregable para la asignatura **Bases de Datos II** (Quinto Semestre) y sirve como laboratorio práctico para:

- Diseño e implementación de microservicios distribuidoš.
- Integración de protocolos RPC modernos con sistemas de persistencia NoSQL.
- Construcción de contenedores Docker para orquestación de servicios.
- Validación de integridad en operaciones CRUD con lógica defensiva.

---

## 2. Arquitectura de Software

### Patrón Arquitectónico: Arquitectura de Capas

El sistema está organizado en tres capas bien definidas:

```
┌─────────────────────────────────────────────────────────────┐
│                  CAPA DE PRESENTACIÓN                       │
│                    Postman (Cliente)                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                  HTTP/2 + gRPC
                     │
┌────────────────────▼────────────────────────────────────────┐
│              CAPA DE LÓGICA DE NEGOCIO                       │
│        Servidor gRPC (Python + gRPC Framework)              │
│        - PezServiceServicer                                 │
│        - Métodos CRUD (Create, Read, Update, Delete)        │
└────────────────────┬────────────────────────────────────────┘
                     │
                   TCP/IP
                     │
┌────────────────────▼────────────────────────────────────────┐
│              CAPA DE PERSISTENCIA                            │
│        MongoDB (Base de Datos NoSQL)                        │
│        - Colección: productos                               │
│        - Borrado lógico: campo "activo"                     │
└─────────────────────────────────────────────────────────────┘
```

### Flujo de Comunicación

1. **Cliente (Postman)** envía una solicitud serializada en formato Protobuf mediante HTTP/2 al servidor gRPC.
2. **Servidor gRPC** deserializa el mensaje y lo mapea a la estructura interna de Python.
3. **Capa de Lógica de Negocio** ejecuta la operación correspondiente (CRUD) y aplica reglas de negocio.
4. **Driver PyMongo** convierte la operación Python a una consulta BSON y la envía a MongoDB.
5. **MongoDB** persiste o recupera los datos según la operación solicitada.
6. **Respuesta**: El servidor serializa el resultado nuevamente en Protobuf y lo devuelve al cliente.

### Principios Arquitectónicos Aplicados

- **Separación de Responsabilidades**: Cada capa maneja un dominio específico (presentación, lógica, persistencia).
- **Abstracción de Protocolos**: gRPC abstrae la complejidad de la serialización y comunicación de red.
- **Independencia de Tecnología**: Las capas pueden ser reemplazadas sin afectar el resto (ej: cambiar MongoDB por PostgreSQL).
- **Escalabilidad Horizontal**: El servicio puede replicarse detrás de un load balancer sin cambios en la lógica.

---

## 3. Stack Tecnológico

### Lenguajes y Frameworks

| Componente | Tecnología | Versión | Propósito |
|-----------|------------|---------|----------|
| Servidor Backend | Python 3 | 3.9+ | Runtime de lógica de negocio |
| Framework RPC | gRPC | 1.60.0 | Comunicación distribuida sobre HTTP/2 |
| Herramientas gRPC | grpcio-tools | 1.60.0 | Compilación de archivos .proto |
| Driver Base de Datos | PyMongo | 4.6.1 | Acceso a MongoDB desde Python |

### Protocolos de Comunicación

- **HTTP/2**: Protocolo de transporte subyacente (mejora sobre HTTP/1.1 con multiplexing, header compression y server push).
- **gRPC**: Remote Procedure Call framework que serializa mensajes usando **Protocol Buffers v3**.
- **Protocol Buffers (Protobuf)**: Formato de serialización binario eficiente definido en `peces.proto`.

### Infraestructura

| Componente | Tecnología | Versión | Propósito |
|-----------|------------|---------|----------|
| Base de Datos | MongoDB | 6.0 | Almacenamiento NoSQL de documentos |
| Contenedorización | Docker | Latest | Encapsulación de servicios |
| Orquestación | Docker Compose | 3.8 | Orquestación local de múltiples servicios |

---

## 4. Modelo de Base de Datos

### Estrategia NoSQL: Documentos Flexibles

MongoDB almacena cada pez exótico como un documento JSON flexible dentro de la colección `productos`, con la siguiente estructura:

### Esquema de la Colección `productos`

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "nombre_comun": "Pez Payaso",
  "especie": "Amphiprion ocellaris",
  "descripcion": "Pez tropical de agua salada, famoso por su simbiosis con anémonas",
  "precio": 25.99,
  "stock": 15,
  "categoria": ["costa", "oceanico"],
  "estado": ["ornamental"],
  "imagen_url": "https://ejemplo.com/imagen_pez_payaso.jpg",
  "activo": true
}
```

### Campos del Documento

| Campo | Tipo | Descripción | Constraint |
|-------|------|-------------|-----------|
| `_id` | ObjectId | Identificador único generado por MongoDB | Primary Key |
| `nombre_comun` | String | Nombre vernacular de la especie | Not Null |
| `especie` | String | Nombre científico (ej: *Amphiprion ocellaris*) | Not Null |
| `descripcion` | String | Descripción detallada de características | Not Null |
| `precio` | Double | Precio en unidad monetaria local | Not Null |
| `stock` | Int32 | Cantidad disponible en inventario | Not Null |
| `categoria` | Array[String] | Clasificación por hábitat (ej: *zona_hadal*, *costa*) | Not Null |
| `estado` | Array[String] | Propósito del pez (ej: *ornamental*, *consumo*) | Not Null |
| `imagen_url` | String | URL de la imagen del pez | Not Null |
| `activo` | Boolean | Indicador de borrado lógico (false = eliminado lógicamente) | Default: true |

### Política de Borrado Lógico

El sistema **NO elimina documentos físicamente** de la base de datos. En su lugar:

1. Cuando se invoca `DeletePez(id)`, se actualiza el campo `activo` a `false`.
2. Las consultas **deben filtrar explícitamente** por `activo: true` (implementación futura).
3. Se preserva el **historial completo** de datos para auditoría y recuperación.

**Beneficios**:
- Historial íntegro para análisis histórico.
- Recuperación de datos eliminados sin restauración de backups.
- Cumplimiento de políticas de auditoría y compliance.

### Índices Recomendados

Para optimizar consultas en producción:

```javascript
db.productos.createIndex({ "especie": 1 })
db.productos.createIndex({ "estado": 1 })
db.productos.createIndex({ "categoria": 1 })
db.productos.createIndex({ "activo": 1 })
db.productos.createIndex({ "precio": 1 })
```

---

## 5. Capa de Presentación

### Modelo de Interfaz: API gRPC sin Frontend Tradicional

Este proyecto **no incluye un frontend web tradicional** (HTML, JavaScript, React, etc.). En su lugar:

- **Postman** actúa como el **cliente oficial de API** para consumir el microservicio gRPC.
- Las solicitudes se estructuran como llamadas RPC sobre HTTP/2.
- Las respuestas se reciben en formato Protobuf serializado.

### ¿Por qué Postman en lugar de un Frontend Web?

| Aspecto | Decisión |
|--------|----------|
| Propósito del Proyecto | Prototipo de backend distribuido, no una aplicación completa |
| Enfoque Académico | Énfasis en microservicios y persistencia, no en UI/UX |
| Eficiencia | Postman permite testing rápido sin overhead de desarrollo frontend |
| Interoperabilidad | gRPC es agnóstico a lenguaje/plataforma del cliente |

### Consumo del API desde Postman

#### 1. Crear un Pez (CreatePez)

**URL (gRPC)**: `grpc://localhost:50051`  
**Método**: `peces.PezService.CreatePez`  
**Body (JSON)**: 

```json
{
  "nombre_comun": "Pez Payaso",
  "especie": "Amphiprion ocellaris",
  "descripcion": "Pez tropical de agua salada con rayas naranja y blancas",
  "precio": 25.99,
  "stock": 10,
  "categoria": ["costa", "oceanico"],
  "estado": ["ornamental"],
  "imagen_url": "https://ejemplo.com/pez_payaso.jpg"
}
```

**Respuesta**:

```json
{
  "id": "507f1f77bcf86cd799439011",
  "nombre_comun": "Pez Payaso",
  "especie": "Amphiprion ocellaris",
  "descripcion": "Pez tropical de agua salada con rayas naranja y blancas",
  "precio": 25.99,
  "stock": 10,
  "categoria": ["costa", "oceanico"],
  "estado": ["ornamental"],
  "imagen_url": "https://ejemplo.com/pez_payaso.jpg",
  "activo": true
}
```

#### 2. Leer un Pez (ReadPez)

**Método**: `peces.PezService.ReadPez`  
**Body**:

```json
{
  "id": "507f1f77bcf86cd799439011"
}
```

#### 3. Actualizar un Pez (UpdatePez)

**Método**: `peces.PezService.UpdatePez`  
**Body**:

```json
{
  "pez": {
    "id": "507f1f77bcf86cd799439011",
    "nombre_comun": "Pez Payaso",
    "especie": "Amphiprion ocellaris",
    "descripcion": "Descripción actualizada",
    "precio": 29.99,
    "stock": 8,
    "categoria": ["costa", "oceanico"],
    "estado": ["ornamental"],
    "imagen_url": "https://ejemplo.com/pez_payaso_v2.jpg",
    "activo": true
  }
}
```

#### 4. Eliminar un Pez (DeletePez - Borrado Lógico)

**Método**: `peces.PezService.DeletePez`  
**Body**:

```json
{
  "id": "507f1f77bcf86cd799439011"
}
```

**Respuesta**:

```json
{
  "success": true,
  "mensaje": "Pez marcado como Inactivo con éxito."
}
```

---

## 6. Estructura del Proyecto

```
proyecto-peces/
├── peces.proto                    # Definición de mensajes y servicios gRPC
├── peces_pb2.py                   # Archivo generado: definiciones de mensajes
├── peces_pb2_grpc.py              # Archivo generado: definiciones de servicios
├── server.py                      # Implementación del servidor gRPC
├── requirements.txt               # Dependencias de Python
├── Dockerfile                     # Definición de la imagen Docker del servicio
├── docker-compose.yml             # Orquestación de servicios (MongoDB + gRPC)
├── .gitignore                     # Archivos excluidos del control de versiones
├── README.md                      # Este archivo
└── __pycache__/                   # Caché de Python (generado automáticamente)
    ├── peces_pb2.cpython-311.pyc
    └── peces_pb2_grpc.cpython-311.pyc
```

### Descripción de Archivos Clave

#### `peces.proto`
Define la interfaz del servicio gRPC mediante Protocol Buffers v3:
- **Message Pez**: Estructura central que representa un pez exótico.
- **Request/Response Messages**: Estructuras para cada operación CRUD.
- **Service PezService**: Define los cuatro métodos RPC disponibles.

#### `server.py`
Implementación del servidor gRPC en Python:
- **Clase PezServiceServicer**: Implementa los métodos definidos en el .proto.
- **Métodos CRUD**: `CreatePez`, `ReadPez`, `UpdatePez`, `DeletePez`.
- **Integración MongoDB**: Conexión a MongoDB y mapeo de datos BSON.
- **Función serve()**: Inicia el servidor gRPC en el puerto 50051.

#### `docker-compose.yml`
Orquestación de servicios:
- **Servicio MongoDB**: Base de datos NoSQL en puerto 27017.
- **Servicio gRPC Server**: Servidor Python en puerto 50051.
- **Volumen Compartido**: Los datos de MongoDB persisten incluso si se detiene el contenedor.

---

## 7. Prerrequisitos

Antes de ejecutar el proyecto, asegúrate de contar con:

### Sistema Operativo
- **Windows 10/11**, **macOS** o **Linux** (Ubuntu 20.04+)

### Herramientas Requeridas

| Herramienta | Versión Mínima | Propósito |
|------------|---------------|---------  |
| **Docker** | 20.10 | Encapsulación y ejecución de contenedores |
| **Docker Compose** | 1.29 | Orquestación de múltiples servicios |
| **Git** | 2.25+ | Control de versiones (opcional para clonar) |
| **Python** | 3.9+ | Desarrollo local (opcional, si se ejecuta sin Docker) |

### Verificación de Instalación

```bash
# Verificar Docker
docker --version
# Esperado: Docker version 20.10.x o superior

# Verificar Docker Compose
docker-compose --version
# Esperado: docker-compose version 1.29.x o superior

# Verificar Python (opcional)
python --version
# Esperado: Python 3.9+
```

### Recursos Mínimos Recomendados
- **CPU**: 2 núcleos
- **RAM**: 2 GB
- **Almacenamiento**: 500 MB disponibles (incluyendo imagen MongoDB y dependencias)
- **Conexión de Red**: Acceso local (localhost) sin restricciones

---

## 8. Instrucciones de Ejecución

### 8.1 Clonar el Repositorio

```bash
# Clonar desde el repositorio remoto
git clone https://github.com/Alexelsus/proyecto-peces.git

# Navegar al directorio del proyecto
cd proyecto-peces
```

### 8.2 Construcción y Ejecución del Proyecto

#### Opción A: Ejecución Completa con Docker Compose (Recomendado)

Este es el método más simple y recomendado para ejecutar el proyecto en su totalidad.

```bash
# Compilar las imágenes y levantar los servicios
docker-compose up --build

# En otra terminal, verificar que los servicios están activos
docker ps
```

**Esperado**:
```
CONTAINER ID   IMAGE                      STATUS
abc123def456   mongo:6.0                  Up 2 minutes   mongodb_peces
xyz789uvw012   proyecto-peces-grpc_server Up 2 minutes   grpc_server_peces
```

#### Opción B: Ejecución Step-by-Step (Desarrollo Local)

Si deseas ejecutar componentes de forma aislada:

##### 1. Iniciar MongoDB

```bash
# Opción 1a: Usando Docker
docker run -d --name mongodb_dev -p 27017:27017 mongo:6.0

# Opción 1b: Si tienes MongoDB instalado localmente
mongod --dbpath ./data
```

##### 2. Preparar el Entorno Python

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

##### 3. Compilar los Archivos Protobuf (si es necesario)

```bash
# Generar peces_pb2.py y peces_pb2_grpc.py
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. peces.proto
```

##### 4. Ejecutar el Servidor gRPC

```bash
# Iniciar el servidor
python server.py

# Esperado:
# Servidor gRPC ejecutándose en el puerto 50051...
```

### 8.3 Verificación de Conectividad

#### A. Verificar que MongoDB está activo

```bash
# Conectarse a MongoDB usando MongoDB CLI (si está instalada)
mongosh "mongodb://localhost:27017"

# En el cliente MongoDB:
> show dbs
> use tienda_peces
> db.productos.find()
```

#### B. Verificar que el servidor gRPC está escuchando

```bash
# En Linux/macOS:
netstat -tulpn | grep 50051

# En Windows (PowerShell):
netstat -ano | findstr 50051

# Esperado: Estado LISTENING en puerto 50051
```

### 8.4 Pruebas con Postman

#### Importar la Colección gRPC

1. **Abrir Postman**.
2. **Crear una nueva solicitud gRPC**:
   - Click en el `+` para nueva pestaña.
   - Seleccionar **gRPC** como tipo de solicitud.

#### 1. Crear un Pez

```
URL: grpc://localhost:50051
Método: peces.PezService.CreatePez
Body:
{
  "nombre_comun": "Pez Beta",
  "especie": "Betta splendens",
  "descripcion": "Pez de agua dulce con colores vibrantes",
  "precio": 15.50,
  "stock": 25,
  "categoria": ["agua_dulce"],
  "estado": ["ornamental"],
  "imagen_url": "https://ejemplo.com/betta.jpg"
}
```

**Respuesta Esperada**:
```json
{
  "id": "<ID_GENERADO>",
  "nombre_comun": "Pez Beta",
  "especie": "Betta splendens",
  ...
}
```

#### 2. Leer el Pez Creado

```
Método: peces.PezService.ReadPez
Body:
{
  "id": "<ID_GENERADO>"
}
```

#### 3. Actualizar el Pez

```
Método: peces.PezService.UpdatePez
Body:
{
  "pez": {
    "id": "<ID_GENERADO>",
    "nombre_comun": "Pez Beta Actualizado",
    "especie": "Betta splendens",
    "descripcion": "Descripción actualizada",
    "precio": 18.99,
    "stock": 20,
    "categoria": ["agua_dulce"],
    "estado": ["ornamental"],
    "imagen_url": "https://ejemplo.com/betta_v2.jpg",
    "activo": true
  }
}
```

#### 4. Eliminar el Pez (Borrado Lógico)

```
Método: peces.PezService.DeletePez
Body:
{
  "id": "<ID_GENERADO>"
}
```

**Respuesta Esperada**:
```json
{
  "success": true,
  "mensaje": "Pez marcado como Inactivo con éxito."
}
```

### 8.5 Detener los Servicios

```bash
# Detener todos los servicios (sin eliminar datos)
docker-compose down

# Detener y eliminar volúmenes (¡Esto elimina los datos!)
docker-compose down -v

# Detener un contenedor específico
docker stop grpc_server_peces
docker stop mongodb_peces
```

---

## 9. Troubleshooting

### Error: "Port 50051 already in use"
```bash
# Liberar el puerto en Windows (PowerShell):
netstat -ano | findstr 50051
taskkill /PID <PID> /F

# En Linux/macOS:
lsof -i :50051
kill -9 <PID>
```

### Error: "Cannot connect to MongoDB"
```bash
# Verificar que el contenedor MongoDB está activo
docker ps | grep mongodb

# Ver los logs del contenedor
docker logs mongodb_peces
```

### Error: "ModuleNotFoundError: No module named 'peces_pb2'"
```bash
# Compilar nuevamente los archivos Protobuf
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. peces.proto
```

---

## 10. Notas de Desarrollo y Mejoras Futuras

### Mejoras Potenciales

- **Autenticación y Autorización**: Implementar OAuth2 o JWT en el servidor gRPC.
- **Versionado de API**: Soportar múltiples versiones del servicio.
- **Logging Distribuido**: Integrar herramientas como ELK Stack para observabilidad.
- **Cachés**: Implementar Redis para caché de consultas frecuentes.
- **Validaciones Avanzadas**: Agregar validadores de negocio en la capa de servicios.
- **Frontend Web**: Desarrollar un cliente web en React/Vue consumiendo el API.
- **Tests Automatizados**: Implementar pruebas unitarias e integración con pytest.
- **Documentación Swagger**: Generar OpenAPI/gRPC Swagger para autodocumentación.

---

## 11. Referencias

- [Protocol Buffers Documentación](https://developers.google.com/protocol-buffers)
- [gRPC Python Documentation](https://grpc.io/docs/languages/python/)
- [MongoDB PyMongo Documentation](https://pymongo.readthedocs.io/)
- [Docker Compose Official Guide](https://docs.docker.com/compose/)
- [HTTP/2 Specification - RFC 7540](https://tools.ietf.org/html/rfc7540)

---

## 12. Licencia y Autoría

- **Autor**: Alex, Samuel & Pablo
- **Institución**: CETI 5O - Bases de Datos II / Arquitectura de Software
- **Fecha de Creación**: 2026
- **Licencia**: MIT (Libre para uso académico y comercial)

---

**Última Actualización**: Junio 2026

Para preguntas, reporte de bugs o sugerencias, abra un issue en el repositorio oficial. 💘
