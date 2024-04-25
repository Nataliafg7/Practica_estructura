
class Nodo:
   
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

    def __repr__(self) -> str:
        return f"Nodo({self.valor})"



class ListaEnlazadaSimple:

    def __init__(self) -> None:
        self.inicio = None

    def insertar_al_inicio(self, valor):
        nodo = Nodo(valor)
        nodo.siguiente = self.inicio
        self.inicio = nodo

    def insertar(self, valor):
        if self.inicio is None:
            self.inicio = Nodo(valor)
            return

        actual = self.inicio
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente = Nodo(valor)

    def buscar(self, func_busqueda, buscar_todos=False):
        lista_resultados = ListaEnlazadaSimple()

        actual = self.inicio
        while actual:
            if func_busqueda(actual.valor):
                if buscar_todos == False:
                    return actual
                lista_resultados.insertar(actual.valor)
            actual = actual.siguiente

        if buscar_todos and lista_resultados.inicio:
            return lista_resultados

        return None

    def eliminar(self, func_busqueda, eliminar_todos=False):
        actual = self.inicio
        previo = None
        while actual:
            if func_busqueda(actual.valor):
                if previo is None:
                    self.inicio = actual.siguiente
                else:
                    previo.siguiente = actual.siguiente
                if eliminar_todos == False:
                    return
            else:
                previo = actual
            actual = actual.siguiente

    def reemplazar(self, func_busqueda, nuevo_valor):
        actual = self.inicio
        while actual:
            if func_busqueda(actual.valor):
                actual.valor = nuevo_valor
                return
            actual = actual.siguiente


    def __repr__(self) -> str:
        _repr = ""
        actual = self.inicio
        while actual:
            _repr += f"[{actual.valor}] -> "
            actual = actual.siguiente
        _repr += "None"  # Agregar "None" al final para indicar el final de la lista
        return _repr

class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre
        self.num_libros_alquilados = 0

    def alquilar_libro(self):
        self.num_libros_alquilados += 1
class Libro:

    def __init__(
        self,
        numero: int,
        genero: str,
        titulo: str,
        autor: str,
        año: int,
        tarifa_diaria_alquiler: float,
        esta_rentado: bool = False,
        notas: str = None,
    ) -> None:
        self.numero = numero
        self.genero = genero
        self.titulo = titulo
        self.autor = autor
        self.año = año
        self.tarifa_diaria_alquiler = tarifa_diaria_alquiler
        self.esta_rentado = esta_rentado
        self.notas = notas

    def __repr__(self) -> str:
        return f"[{self.numero}] {self.titulo} by {self.autor} ({self.año} {self.genero} {self.tarifa_diaria_alquiler})"

    def obtener_info(self):
        return {
            "numero": self.numero,
            "genero": self.genero,
            "titulo": self.titulo,
            "autor": self.autor,
            "año": self.año,
            "tarifa_diaria_alquiler": self.tarifa_diaria_alquiler,
            "esta_rentado": self.esta_rentado,
            "notas": self.notas,
        }



class Libreria:
    def __init__(self):
        self.libros = ListaEnlazadaSimple()
        self.usuarios = {}

    def alquilar_libro(self, usuario, numero_libro):
        def busqueda(x):
            return x.numero == numero_libro

        libro_encontrado = self.buscar(busqueda)
        if libro_encontrado:
            libro = libro_encontrado.valor
            if not libro.esta_rentado:
                libro.esta_rentado = True
                mensaje = f"El libro '{libro.titulo}' ha sido alquilado exitosamente por {usuario.nombre}."
                
                # Verificar si el usuario ya está en el diccionario
                if usuario.nombre in self.usuarios:
                    # Si el usuario ya está en el diccionario, aumentamos la cantidad de libros alquilados
                    self.usuarios[usuario.nombre] += 1
                else:
                    # Si el usuario no está en el diccionario, lo agregamos con 1 libro alquilado
                    self.usuarios[usuario.nombre] = 1
            else:
                mensaje = f"El libro '{libro.titulo}' ya está alquilado."
        else:
            mensaje = f"No se encontró ningún libro con el número de identificación '{numero_libro}'."

        return mensaje

    # Resto del código...
    def crear_libro(self, libro: Libro):
        self.libros.insertar(libro)


    def eliminar_libro(self, func_busqueda, eliminar_todos=False):
        self.libros.eliminar(func_busqueda, eliminar_todos)
        
    def buscar(self, func_busqueda, buscar_todos=False):
        return self.libros.buscar(func_busqueda, buscar_todos)

    def buscar_por_genero(self, genero: str):
        def busqueda(x: Libro):
            return x.genero == genero
        
        libros_encontrados, cantidad_libros = self.buscar(busqueda, buscar_todos=True), 0
        
        mensaje = f"Género: {genero}\n"
        if libros_encontrados:
            # Contar la cantidad de libros encontrados
            actual = libros_encontrados.inicio
            while actual:
                cantidad_libros += 1
                actual = actual.siguiente

            mensaje += f"El total de libros encontrados del genero especificado son: {cantidad_libros}\n"
            mensaje += "Libros encontrados:\n"
            actual = libros_encontrados.inicio
            while actual:
                mensaje += f"{actual.valor}\n"
                actual = actual.siguiente
        else:
            mensaje += "No se encontraron libros de este género.\n"
        return mensaje

    def buscar_por_titulo(self, titulo: str):
        def busqueda(x: Libro):
            return x.titulo == titulo

    def buscar_por_autor(self, autor: str, buscar_todos=False):
        def busqueda(x: Libro):
            return x.autor == autor

        return self.buscar(busqueda, buscar_todos=buscar_todos)

    def buscar_por_año(self, año: int, buscar_todos=False):
        def busqueda(x: Libro):
            return x.año == año
        libro_encontrado = self.buscar(busqueda)
        if libro_encontrado:
                libro = libro_encontrado.valor
                disponible = "disponible" if not libro.esta_rentado else "no disponible"
                mensaje = f"El libro del año'{año}' está en la biblioteca y su estado es {disponible} para alquilar."
        else:
            mensaje = f"El libro del año'{año}' no se encuentra en la biblioteca."
        return mensaje, self.buscar(busqueda)


    def buscar_disponibles_para_alquiler(self):
        mensaje = "Los libros disponibles para alquilar son:"
        def busqueda(x: Libro):
            
            return not x.esta_rentado

        libros_disponibles = self.buscar(busqueda, buscar_todos=True)
    
        return mensaje, libros_disponibles

    def buscar_alquilados(self):
        mensaje = "Los libros que se encuentran alquilados son:"
        def busqueda(x: Libro):
            return x.esta_rentado

        libros_alquilados = self.buscar(busqueda, buscar_todos=True)
    
        return mensaje, libros_alquilados

    def buscar_disponibles_por_genero(self, genero: str):
        def busqueda(x: Libro):
            return not x.esta_rentado and x.genero == genero

        return self.buscar(busqueda, buscar_todos=True)

    def buscar_rentados_por_genero(self, genero: str):
        def busqueda(x: Libro):
            return x.esta_rentado and x.genero == genero

        return self.buscar(busqueda, buscar_todos=True)

    def alquilar_libro_identificacion(self, numero_libro):
        def busqueda(x):
            return x.numero == numero_libro
        libro_encontrado = self.buscar(busqueda)
        if libro_encontrado:
            libro = libro_encontrado.valor
            if not libro.esta_rentado:
                libro.esta_rentado = True
                mensaje = f"El libro'{libro.titulo}' ha sido alquilado exitosamente."
            else:
                    mensaje = f"El libro '{libro.titulo}' ya está alquilado."
        else:
                mensaje = f"No se encontró ningún libro con el número de identificación '{numero_libro}'."

        return mensaje
    
    
    def alquilar_libro_genero(self, genero):
        def busqueda(x):
            return x.genero == genero
        libro_encontrado = self.buscar(busqueda)
        if libro_encontrado:
            libro = libro_encontrado.valor
            if not libro.esta_rentado:
                libro.esta_rentado = True
                mensaje = f"El libro '{libro.titulo}' ha sido alquilado exitosamente."
            else:
                    mensaje = f"El libro '{libro.titulo}' ya está alquilado."
        else:
                mensaje = f"No se encontró ningún libro con el genero '{genero}'."

        return mensaje

            
    def devolver_libro(self, libro: Libro):
        def busqueda(x: Libro):
            return x.numero == libro.numero

        libro.esta_rentado = False

        self.libros.reemplazar(busqueda, libro)
    
#Creamos una instancia de la clase libreria, y pasamos como argumentos los datos de los libros

libreria = Libreria()

libro1 = Libro(1.1, "Novela", "Julio Cortazar", "Rayuela", 1963, 10.000)
libro6 = Libro(1.2, "Novela", "María", "Jorge Isaacs", 1867, 6.500)
libro2 = Libro(2.1, "Crecimiento", "David Graeber", "Trabajis de mierda", 2018, 12.000)
libro3 = Libro(2.2, "Crecimiento", "Walter Riso", "Pensar bien, sentirse bien", 2004, 6.000)
libro4=Libro(2.3, "Crecimiento", "Ryan Holiday", "La disciplina marcará tu destino", 2022, 15.000)
libro5= Libro(2.4, "Crecimiento", "Steve Harvey", "Actua como dama pero piensa como hombre", 2015, 10.000)

# AGREGAR LIBRO 
#Llamamos el metodo crear libro de la clase Libreria y le pasamos el objeto
libreria.crear_libro(libro1)
libreria.crear_libro(libro2)
libreria.crear_libro(libro3)
libreria.crear_libro(libro4)
libreria.crear_libro(libro5)

"""

# Imprimir libros
print(libro1, libro2, libro3, libro4, libro5, libro6,  sep="\n")

# BORRAR LIBROS
 
 # Borrar por titulo
criterio_titulo_buscar = "Cien años de soledadd"
libro_encontrado = libreria.buscar_por_titulo(criterio_titulo_buscar)

if libro_encontrado:
    def criterio_busqueda(libro):
        return libro.titulo == criterio_titulo_buscar

    libreria.eliminar_libro(criterio_busqueda)
    print("El libro fue eliminado con exito")
else:
    print("Error, el libro no se encuentra en la libreria.")


# Imprimir todos los libros actualizados despues de que lo eliminamos
print("Libros actualizados después de eliminar:")
print(libreria.libros)

 # Borrar por autor
criterio_autor_buscar ="Gabriel García Márquez"
libro_encontrado=libreria.buscar_por_autor(criterio_autor_buscar)

if libro_encontrado:
    def criterio_busqueda2(libro):
        return libro.autor ==criterio_autor_buscar
    libreria.eliminar_libro(criterio_busqueda2, True)
    print("El libro fue eliminado con exito")
else:
    print("Error, el libro no se encuentra en la libreria.")

# Imprimir todos los libros actualizados despues de que lo eliminamos
print("Libros actualizados después de eliminar:")
print(libreria.libros)        

#BUSCAR TODOS LOS LIBROS POR GENERO

#Busca por genero, dice cuantos hay y si estan disponibles o no para alquilar

print ("Todos los libros que solicito son:",libreria.buscar_por_genero("Ficcion"))
print ("Todos los libros disponibles que solicito son:",libreria.buscar_disponibles_por_genero("Ficcion"))

#Busca por titulo, muestra si se tiene el la biblioteca y si esta o no disponible para alquilar
print(libreria.buscar_por_titulo("Simón Bolívar: Una biografía"))

#Busca por año, muestra si se tiene el la biblioteca y si esta o no disponible para alquilar
print(libreria.buscar_por_año(2001,True))



#Lista todos los libros disponibles para alquilar 
print(libreria.buscar_disponibles_para_alquiler())
#Lista todos los libros que estan ocupados (ya alquilados)
print(libreria.buscar_alquilados())

# Alquilar libro por numero de libro 
numero_libro = 1.1
print(libreria.alquilar_libro_identificacion(numero_libro))

"Alquilar libro por el genero novela"
genero="Novela"
print(libreria.alquilar_libro_genero(genero))


# Descuento 

# Crear usuarios
primer_usuario = Usuario("Juliana")

# Alquilar libros
print(libreria.alquilar_libro(primer_usuario, 1.1))  
print(libreria.alquilar_libro(primer_usuario, 2.1))  

# Mostrar el estado de los libros después del alquiler
print(libreria.libros)

#Devolver libro
libro_devuelto = Libro(1.1, "Novela", "Julio Cortazar", "Rayuela", 1963, 10.000)
print(libreria.devolver_libro(libro_devuelto))
print(f"El libro '{libro_devuelto.titulo}' ha sido devuelto correctamente.")
"""
