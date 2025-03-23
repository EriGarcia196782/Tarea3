import os
import graphviz

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.izquierda = None
        self.derecha = None

class Buscar_arb:
    def __init__(self):
        self.raiz = None

    def insertar(self, dato):
        self.raiz = self._insertar_recursivo(self.raiz, dato)
    
    def _insertar_recursivo(self, nodo, dato):
        if nodo is None:
            return Nodo(dato)
        if dato < nodo.dato:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, dato)
        else:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, dato)
        return nodo

    def buscar(self, dato):
        return self._buscar_recursivo(self.raiz, dato)

    def _buscar_recursivo(self, nodo, dato):
        if nodo is None or nodo.dato == dato:
            return nodo
        if dato < nodo.dato:
            return self._buscar_recursivo(nodo.izquierda, dato)
        return self._buscar_recursivo(nodo.derecha, dato)

    def eliminar(self, dato):
        self.raiz = self._eliminar_recursivo(self.raiz, dato)

    def _eliminar_recursivo(self, nodo, dato):
        if nodo is None:
            return nodo
        if dato < nodo.dato:
            nodo.izquierda = self._eliminar_recursivo(nodo.izquierda, dato)
        elif dato > nodo.dato:
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, dato)
        else:
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda
            temp = self._minimo_valor_nodo(nodo.derecha)
            nodo.dato = temp.dato
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, temp.dato)
        return nodo

    def _minimo_valor_nodo(self, nodo):
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual

    def cargar_desde_archivo(self, ruta):
        if not os.path.exists(ruta):
            print("El archivo no se ha encontrado")
            return
        with open(ruta, 'r') as file:
            for linea in file:
                try:
                    dato = int(linea.strip())
                    self.insertar(dato)
                except ValueError:
                    print(f"El archivo tiene valores invalidos: {linea.strip()}")

    def generar_graphviz(self, nombre_archivo="arbol"):
        dot = graphviz.Digraph()
        self._agregar_nodos(dot, self.raiz)
        dot.render(nombre_archivo, format="png", cleanup=True)
        print(f"Imagen generada: {nombre_archivo}.png")

    def _agregar_nodos(self, dot, nodo):
        if nodo is not None:
            dot.node(str(nodo.dato))
            if nodo.izquierda is not None:
                dot.edge(str(nodo.dato), str(nodo.izquierda.dato))
                self._agregar_nodos(dot, nodo.izquierda)
            if nodo.derecha is not None:
                dot.edge(str(nodo.dato), str(nodo.derecha.dato))
                self._agregar_nodos(dot, nodo.derecha)

if __name__ == "__main__":
    arbol = Buscar_arb()
    while True:
        print("======Menu======")
        print("1. Insertar un numero")
        print("2. Buscar un numero")
        print("3. Eliminar numero")
        print("4. Cargar desde un archivo de texto")
        print("5. Generar imagen del arbol binario")
        print("6. Salir")
        print("-----------------------")
        opcion = input("Ingrese una opcion valida")

        
        if opcion == "1":
            valor = int(input("Ingrese el numero que desea ingresar:"))
            arbol.insertar(valor)
        elif opcion == "2":
            valor = int(input("Ingrese el numero que desea buscar:"))
            print("Se ha encontrado" if arbol.buscar(valor) else "No encontrado")
        elif opcion == "3":
            valor = int(input("Ingrese el numero que desea eliminar: "))
            arbol.eliminar(valor)
        elif opcion == "4":
            ruta = input("Ingrese la ruta del archivo de texto")
            arbol.cargar_desde_archivo(ruta)
        elif opcion == "5":
            arbol.generar_graphviz()
        elif opcion == "6":
            break
        else:
            print("Opcion no encontrara, seleccione una opcion valida")
