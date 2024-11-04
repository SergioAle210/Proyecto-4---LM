# El objetivo de este programa es simular un sistema de control difuso para un calentador de agua.
# El sistema tiene dos entradas: la temperatura actual del agua y la temperatura deseada del agua.
# La salida del sistema es el porcentaje de uso del calentador.

# Importamos las bibliotecas necesarias
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from colorama import Fore, Style, init

# Inicializamos colorama para poder usar colores en la terminal
init(autoreset=True)


# Función para mostrar un menú interactivo
def mostrar_menu():
    print(Fore.GREEN + Style.BRIGHT + "-" * 60)
    print(Fore.CYAN + "Sistema de Control Difuso del Calentador de Agua")
    print(Fore.GREEN + "-" * 60)

    # Verificamos que las temperaturas estén en el rango [-90, 60]
    while True:
        try:
            print(Fore.YELLOW + "Ingrese los siguientes valores:")
            temp_actual = float(
                input(Fore.YELLOW + "Temperatura actual (entre -90 y 60 grados): ")
            )
            temp_deseada = float(
                input(Fore.YELLOW + "Temperatura deseada (entre -90 y 60 grados): ")
            )

            if temp_deseada < temp_actual:
                print(
                    Fore.RED
                    + "Error: La temperatura deseada debe ser mayor o igual a la actual."
                )
                continue

            # Verificación de que las temperaturas estén dentro del rango
            if -90 <= temp_actual <= 60 and -90 <= temp_deseada <= 60:
                break
            else:
                print(
                    Fore.RED + "Error: La temperatura debe estar entre -90 y 60 grados."
                )
        except ValueError:
            print(Fore.RED + "Error: Entrada no válida. Por favor, ingrese un número.")

    return temp_actual, temp_deseada


# Definimos las variables difusas para la temperatura actual y deseada.
# Usamos el rango [-90, 60] ya que es el rango registrado de temperaturas más bajas y más altas en el mundo.
temp_actual = ctrl.Antecedent(np.arange(-90, 61, 1), "temp_actual")
temp_deseada = ctrl.Antecedent(np.arange(-90, 61, 1), "temp_deseada")
calentador = ctrl.Consequent(np.arange(0, 101, 1), "calentador")

# Aseguramos que la defuzzificación se haga por el método del centroide,
# que es el método más común para obtener un valor final difuso en control difuso.
calentador.defuzzify_method = "centroid"

# Creación de funciones de pertenencia suaves para cada nivel de temperatura.
# Estas funciones gaussianas representan de forma más gradual los cambios entre niveles de temperatura.
temp_actual["super_frio"] = fuzz.gaussmf(temp_actual.universe, -90, 10)
temp_actual["muy_frio"] = fuzz.gaussmf(temp_actual.universe, -60, 10)
temp_actual["frio"] = fuzz.gaussmf(temp_actual.universe, -20, 10)
temp_actual["templado"] = fuzz.gaussmf(temp_actual.universe, 10, 10)
temp_actual["caliente"] = fuzz.gaussmf(temp_actual.universe, 30, 10)
temp_actual["muy_caliente"] = fuzz.gaussmf(temp_actual.universe, 50, 10)
temp_actual["extremadamente_caliente"] = fuzz.gaussmf(temp_actual.universe, 60, 10)

# Las funciones de pertenencia para la temperatura deseada son similares.
temp_deseada["super_baja"] = fuzz.gaussmf(temp_deseada.universe, -90, 10)
temp_deseada["muy_baja"] = fuzz.gaussmf(temp_deseada.universe, -60, 10)
temp_deseada["baja"] = fuzz.gaussmf(temp_deseada.universe, -20, 10)
temp_deseada["media"] = fuzz.gaussmf(temp_deseada.universe, 10, 10)
temp_deseada["alta"] = fuzz.gaussmf(temp_deseada.universe, 30, 10)
temp_deseada["muy_alta"] = fuzz.gaussmf(temp_deseada.universe, 50, 10)
temp_deseada["extremadamente_alta"] = fuzz.gaussmf(temp_deseada.universe, 60, 10)

# Definimos funciones de pertenencia para el calentador.
# Estas funciones indican el porcentaje de uso del calentador.
calentador["muy_bajo"] = fuzz.trimf(calentador.universe, [0, 0, 25])
calentador["bajo"] = fuzz.trimf(calentador.universe, [10, 30, 50])
calentador["medio"] = fuzz.trimf(calentador.universe, [40, 50, 70])
calentador["alto"] = fuzz.trimf(calentador.universe, [60, 75, 90])
calentador["muy_alto"] = fuzz.trimf(calentador.universe, [75, 90, 100])

# Definición de las reglas difusas.
# Cada regla indica cómo deben interactuar las temperaturas actual y deseada
# para determinar el porcentaje de uso del calentador.
# A continuación se definen 23 reglas.
# Cada regla combina un nivel de temperatura actual con uno de temperatura deseada
# y asigna un nivel de uso del calentador.

# Definición de las reglas difusas
# Super Frío
regla1 = ctrl.Rule(
    temp_actual["super_frio"] & temp_deseada["baja"], calentador["medio"]
)
regla2 = ctrl.Rule(
    temp_actual["super_frio"] & temp_deseada["media"], calentador["alto"]
)
regla3 = ctrl.Rule(temp_actual["super_frio"] & temp_deseada["alta"], calentador["alto"])
regla4 = ctrl.Rule(
    temp_actual["super_frio"] & temp_deseada["extremadamente_alta"],
    calentador["muy_alto"],
)

# Muy Frío
regla5 = ctrl.Rule(temp_actual["muy_frio"] & temp_deseada["baja"], calentador["bajo"])
regla6 = ctrl.Rule(temp_actual["muy_frio"] & temp_deseada["media"], calentador["medio"])
regla7 = ctrl.Rule(temp_actual["muy_frio"] & temp_deseada["alta"], calentador["alto"])

# Frío
regla8 = ctrl.Rule(temp_actual["frio"] & temp_deseada["baja"], calentador["bajo"])
regla9 = ctrl.Rule(temp_actual["frio"] & temp_deseada["media"], calentador["medio"])
regla10 = ctrl.Rule(temp_actual["frio"] & temp_deseada["alta"], calentador["alto"])

# Templado
regla11 = ctrl.Rule(temp_actual["templado"] & temp_deseada["baja"], calentador["bajo"])
regla12 = ctrl.Rule(
    temp_actual["templado"] & temp_deseada["media"], calentador["medio"]
)
regla13 = ctrl.Rule(temp_actual["templado"] & temp_deseada["alta"], calentador["medio"])
regla14 = ctrl.Rule(
    temp_actual["templado"] & temp_deseada["extremadamente_alta"], calentador["alto"]
)

# Caliente
regla15 = ctrl.Rule(
    temp_actual["caliente"] & temp_deseada["baja"], calentador["muy_bajo"]
)
regla16 = ctrl.Rule(temp_actual["caliente"] & temp_deseada["media"], calentador["bajo"])
regla17 = ctrl.Rule(temp_actual["caliente"] & temp_deseada["alta"], calentador["medio"])

# Muy Caliente
regla18 = ctrl.Rule(
    temp_actual["muy_caliente"] & temp_deseada["baja"], calentador["muy_bajo"]
)
regla19 = ctrl.Rule(
    temp_actual["muy_caliente"] & temp_deseada["media"], calentador["muy_bajo"]
)
regla20 = ctrl.Rule(
    temp_actual["muy_caliente"] & temp_deseada["alta"], calentador["bajo"]
)

# Extremadamente Caliente
regla21 = ctrl.Rule(
    temp_actual["extremadamente_caliente"] & temp_deseada["baja"],
    calentador["muy_bajo"],
)
regla22 = ctrl.Rule(
    temp_actual["extremadamente_caliente"] & temp_deseada["media"], calentador["bajo"]
)
regla23 = ctrl.Rule(
    temp_actual["extremadamente_caliente"] & temp_deseada["alta"],
    calentador["muy_bajo"],
)

# Creamos el sistema de control difuso y lo configuramos con todas las reglas definidas.
sistema_calentador = ctrl.ControlSystem(
    [
        regla1,
        regla2,
        regla3,
        regla4,
        regla5,
        regla6,
        regla7,
        regla8,
        regla9,
        regla10,
        regla11,
        regla12,
        regla13,
        regla14,
        regla15,
        regla16,
        regla17,
        regla18,
        regla19,
        regla20,
        regla21,
        regla22,
        regla23,
    ]
)

# Creamos la simulación del sistema de control difuso
simulacion_calentador = ctrl.ControlSystemSimulation(sistema_calentador)

# Mostramos el menú para que el usuario ingrese las temperaturas deseadas.
temp_actual_input, temp_deseada_input = mostrar_menu()

# Asignamos las entradas a la simulación.
simulacion_calentador.input["temp_actual"] = temp_actual_input
simulacion_calentador.input["temp_deseada"] = temp_deseada_input

# Ejecutamos la simulación y mostramos el resultado utilizando el método de defuzzificación por centroide.
try:
    simulacion_calentador.compute()
    # Imprimimos el porcentaje de uso del calentador calculado.
    print(
        Fore.MAGENTA
        + Style.BRIGHT
        + f"\nEl porcentaje de uso del calentador es (método del centroide): {simulacion_calentador.output['calentador']:.2f}%"
    )

    simulacion_calentador.print_state()
except Exception as e:
    print(Fore.RED + f"Ocurrió un error durante la simulación: {e}")

# Mostramos las gráficas de las funciones de pertenencia de temperatura actual, deseada y el resultado del calentador.
temp_actual.view()
temp_deseada.view()
calentador.view(simulacion_calentador)
plt.show()
