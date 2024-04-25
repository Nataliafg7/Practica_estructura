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
        _repr += "None"
        return _repr



class Libro:

    def __init__(
        self,
        numero: int,
        genero: str,
        titulo: str,
        autor: str,
        annio: int,
        tarifa_diaria_alquiler: float,
        esta_rentado: bool = False,
        notas: str = None,
    ) -> None:
        self.numero = numero
        self.genero = genero
        self.titulo = titulo
        self.autor = autor
        self.annio = annio
        self.tarifa_diaria_alquiler = tarifa_diaria_alquiler
        self.esta_rentado = esta_rentado
        self.notas = notas

    def __repr__(self) -> str:
        return f"[{self.numero}] {self.titulo} by {self.autor} ({self.annio})"

    def obtener_info(self):
        return {
            "numero": self.numero,
            "genero": self.genero,
            "titulo": self.titulo,
            "autor": self.autor,
            "annio": self.annio,
            "tarifa_diaria_alquiler": self.tarifa_diaria_alquiler,
            "esta_rentado": self.esta_rentado,
            "notas": self.notas,
        }


class Libreria:
    def __init__(self) -> None:
        self.libros = ListaEnlazadaSimple()

    def crear_libro(self, libro: Libro):
        self.libros.insertar(libro)

    def eliminar_libro(self, func_busqueda, eliminar_todos=False):
        self.libros.eliminar(func_busqueda, eliminar_todos)

    def buscar(self, func_busqueda, buscar_todos=False):
        return self.libros.buscar(func_busqueda, buscar_todos)

    def buscar_por_genero(self, genero: str):
        def busqueda(x: Libro):
            return x.genero == genero

        return self.buscar(busqueda, buscar_todos=True)

    def buscar_por_titulo(self, titulo: str):
        def busqueda(x: Libro):
            return x.titulo == titulo

        return self.buscar(busqueda)

    def buscar_por_autor(self, autor: str, buscar_todos=False):
        def busqueda(x: Libro):
            return x.autor == autor

        return self.buscar(busqueda, buscar_todos=buscar_todos)

    def buscar_por_annio(self, annio: int, buscar_todos=False):
        def busqueda(x: Libro):
            return x.annio == annio

        return self.buscar(busqueda, buscar_todos=buscar_todos)

    def buscar_disponibles_para_alquiler(self):
        def busqueda(x: Libro):
            return not x.esta_rentado

        return self.buscar(busqueda, buscar_todos=True)

    def buscar_alquilados(self):
        def busqueda(x: Libro):
            return x.esta_rentado

        return self.buscar(busqueda, buscar_todos=True)

    def buscar_disponibles_por_genero(self, genero: str):
        def busqueda(x: Libro):
            return not x.esta_rentado and x.genero == genero

        return self.buscar(busqueda, buscar_todos=True)

    def buscar_rentados_por_genero(self, genero: str):
        def busqueda(x: Libro):
            return x.esta_rentado and x.genero == genero

        return self.buscar(busqueda, buscar_todos=True)

    def alquilar_libro(self, libro: Libro):
        def busqueda(x: Libro):
            return x.numero == libro.numero

        libro.esta_rentado = True

        self.libros.reemplazar(busqueda, libro)

    def devolver_libro(self, libro: Libro):
        def busqueda(x: Libro):
            return x.numero == libro.numero

        libro.esta_rentado = False

        self.libros.reemplazar(busqueda, libro)


if __name__ == "__main__":
    books = [
        Libro(1, "Fiction", "The Great Gatsby", "F. Scott Fitzgerald", 1925, 0.5),
        Libro(2, "Drama", "To Kill a Mockingbird", "Harper Lee", 1960, 0.75),
        Libro(3, "Fiction", "1984", "George Orwell", 1949, 0.6, True),
        Libro(4, "Drama", "Brave New World", "Aldous Huxley", 1932, 0.7),
        Libro(5, "Fiction", "Animal Farm", "George Orwell", 1945, 0.6, True),
        Libro(6, "Suspenso", "The Catcher in the Rye", "J.D. Salinger", 1951, 0.8),
        Libro(7, "Fiction", "The Grapes of Wrath", "John Steinbeck", 1939, 0.9),
    ]

    libreria = Libreria()
    for book in books:
        libreria.crear_libro(book)

    # print(libreria.libros)

    # print(libreria.buscar_por_genero("Drama"))
    # print(libreria.buscar_por_titulo("The Grapes of Wrath"))
    # print(libreria.buscar_por_autor("George Orwell", buscar_todos=True))
    # print(libreria.buscar_por_annio(1945, buscar_todos=True))
    # print(libreria.buscar_disponibles_para_alquiler())
    # print(libreria.buscar_alquilados())
    # print(libreria.buscar_disponibles_por_genero("Fiction"))
    # print(libreria.buscar_rentados_por_genero("Fiction"))

    print(libreria.buscar_disponibles_para_alquiler())
    nodo = libreria.buscar_por_titulo("The Great Gatsby")
    libreria.alquilar_libro(nodo.valor)
    print(libreria.buscar_disponibles_para_alquiler())
