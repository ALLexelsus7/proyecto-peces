# Imports necesarios para gRPC, MongoDB y manejo de objetos BSON
import grpc
from concurrent import futures
from pymongo import MongoClient
from bson import ObjectId

# Importacion de los archivos generados por la compilacion del proto
import peces_pb2
import peces_pb2_grpc

# Conexión a MongoDB (con el nombre del servicio asignado en Docker)
client = MongoClient("mongodb://mongodb:27017/")
db = client["tienda_peces"]
collection = db["productos"] [cite: 68]

# Implementacion del servicio gRPC definido en el proto, con metodos para CRUD de peces exoticos
class PezServiceServicer(peces_pb2_grpc.PezServiceServicer):

    def CreatePez(self, request, context):
        # Mapeo de gRPC Request a Documento BSON de MongoDB
        nuevo_pez = {
            "nombre_comun": request.nombre_comun,
            "especie": request.especie,
            "descripcion": request.descripcion,
            "precio": request.precio,
            "stock": request.stock,
            "categoria": list(request.categoria),
            "estado": list(request.estado),
            "imagen_url": request.imagen_url,
            "activo": True # Por defecto inicia activo
        }
        resultado = collection.insert_one(nuevo_pez)
        
        return peces_pb2.Pez(
            id=str(resultado.inserted_id),
            **nuevo_pez
        )

    def ReadPez(self, request, context):
        documento = collection.find_one({"_id": ObjectId(request.id)})
        if not documento:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("El pez exótico no existe.")
            return peces_pb2.Pez()
        
        return peces_pb2.Pez(
            id=str(documento["_id"]),
            nombre_comun=documento["nombre_comun"],
            especie=documento["especie"],
            descripcion=documento["descripcion"],
            precio=documento["precio"],
            stock=documento["stock"],
            categoria=documento["categoria"],
            estado=documento["estado"],
            imagen_url=documento["imagen_url"],
            activo=documento["activo"]
        )

    def UpdatePez(self, request, context):
        pez_data = request.pez
        actualizacion = {
            "nombre_comun": pez_data.nombre_comun,
            "especie": pez_data.especie,
            "descripcion": pez_data.descripcion,
            "precio": pez_data.precio,
            "stock": pez_data.stock,
            "categoria": list(pez_data.categoria),
            "estado": list(pez_data.estado),
            "imagen_url": pez_data.imagen_url,
            "activo": pez_data.activo
        }
        
        collection.update_one({"_id": ObjectId(pez_data.id)}, {"$set": actualizacion})
        return pez_data

    def DeletePez(self, request, context):
        # REGLA DE NEGOCIO: Borrado lógico en lugar de físico para mantener historial 
        resultado = collection.update_one(
            {"_id": ObjectId(request.id)}, 
            {"$set": {"activo": False}}
        )
        
        if resultado.modified_count > 0:
            return peces_pb2.DeletePezResponse(success=True, mensaje="Pez marcado como Inactivo con éxito.")
        return peces_pb2.DeletePezResponse(success=False, mensaje="No se pudo actualizar el estado.")
    
# Inicialización del servidor gRPC y registro del servicio implementado, escuchando en el puerto 50051
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    peces_pb2_grpc.add_PezServiceServicer_to_server(PezServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Servidor gRPC ejecutándose en el puerto 50051...")
    server.start()
    server.wait_for_termination()

# Punto de entrada del script para iniciar el servidor gRPC
if __name__ == '__main__':
    serve()