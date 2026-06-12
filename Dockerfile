# Imagen ligera de Python
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los requerimientos
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del codigo al contenedor
COPY . .

# Compila peces.proto para generar los dos archivos _pb2 de gRPC
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. peces.proto

# Expone el puerto en el que corre el servidor
EXPOSE 50051

# Arranca la aplicacion
CMD ["python", "server.py"]