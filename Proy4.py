# El objetivo de este programa es simular un sistema de control difuso para un calentador de agua.
# El sistema tiene dos entradas: la temperatura actual del agua y la temperatura deseada del agua.
# La salida del sistema es el porcentaje de uso del calentador.
# El sistema tiene las siguientes reglas:
# 1. Si la temperatura actual es fría y la temperatura deseada es media, entonces el calentador debe estar a medio.
# 2. Si la temperatura actual es fría y la temperatura deseada es baja, entonces el calentador debe estar bajo.
# 3. Si la temperatura actual es fría y la temperatura deseada es alta, entonces el calentador debe estar alto.
# 4. Si la temperatura actual es templada y la temperatura deseada es baja, entonces el calentador debe estar bajo.
# 5. Si la temperatura actual es templada y la temperatura deseada es media, entonces el calentador debe estar medio.
# 6. Si la temperatura actual es templada y la temperatura deseada es alta, entonces el calentador debe estar medio.
# 7. Si la temperatura actual es caliente y la temperatura deseada es baja, entonces el calentador debe estar bajo.
# 8. Si la temperatura actual es caliente y la temperatura deseada es media, entonces el calentador debe estar medio.
# 9. Si la temperatura actual es caliente y la temperatura deseada es alta, entonces el calentador debe estar alto.

# Importamos las bibliotecas necesarias
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from colorama import Fore, Style, init

# Inicializamos colorama
init(autoreset=True)

# Función para mostrar un menú interactivo
def mostrar_menu():
    print(Fore.GREEN + Style.BRIGHT + "-"*60)
    print(Fore.CYAN + "Sistema de Control Difuso del Calentador de Agua")
    print(Fore.GREEN + "-"*60)
    print(Fore.YELLOW + "Ingrese los siguientes valores:")
    temp_actual = float(input(Fore.YELLOW + "Temperatura actual (entre -90 y 60 grados): "))
    temp_deseada = float(input(Fore.YELLOW + "Temperatura deseada (entre -90 y 60 grados): "))
    return temp_actual, temp_deseada

# Definición de las variables difusas con el nuevo rango de temperatura
temp_actual = ctrl.Antecedent(np.arange(-90, 61, 1), 'temp_actual')
temp_deseada = ctrl.Antecedent(np.arange(-90, 61, 1), 'temp_deseada')
calentador = ctrl.Consequent(np.arange(0, 101, 1), 'calentador')

# Creación de funciones de pertenencia más suaves (gaussianas y sigmoides)
temp_actual['super_frio'] = fuzz.gaussmf(temp_actual.universe, -90, 10)
temp_actual['muy_frio'] = fuzz.gaussmf(temp_actual.universe, -60, 10)
temp_actual['frio'] = fuzz.gaussmf(temp_actual.universe, -20, 10)
temp_actual['templado'] = fuzz.gaussmf(temp_actual.universe, 10, 10)
temp_actual['caliente'] = fuzz.gaussmf(temp_actual.universe, 30, 10)
temp_actual['muy_caliente'] = fuzz.gaussmf(temp_actual.universe, 50, 10)
temp_actual['extremadamente_caliente'] = fuzz.gaussmf(temp_actual.universe, 60, 10)

temp_deseada['super_baja'] = fuzz.gaussmf(temp_deseada.universe, -90, 10)
temp_deseada['muy_baja'] = fuzz.gaussmf(temp_deseada.universe, -60, 10)
temp_deseada['baja'] = fuzz.gaussmf(temp_deseada.universe, -20, 10)
temp_deseada['media'] = fuzz.gaussmf(temp_deseada.universe, 10, 10)
temp_deseada['alta'] = fuzz.gaussmf(temp_deseada.universe, 30, 10)
temp_deseada['muy_alta'] = fuzz.gaussmf(temp_deseada.universe, 50, 10)
temp_deseada['extremadamente_alta'] = fuzz.gaussmf(temp_deseada.universe, 60, 10)

calentador['muy_bajo'] = fuzz.trimf(calentador.universe, [0, 0, 25])
calentador['bajo'] = fuzz.trimf(calentador.universe, [10, 30, 50])
calentador['medio'] = fuzz.trimf(calentador.universe, [40, 50, 70])
calentador['alto'] = fuzz.trimf(calentador.universe, [60, 75, 90])
calentador['muy_alto'] = fuzz.trimf(calentador.universe, [75, 90, 100])

# Definición de las reglas difusas
regla1 = ctrl.Rule(temp_actual['super_frio'] & temp_deseada['extremadamente_alta'], calentador['muy_alto'])
regla2 = ctrl.Rule(temp_actual['super_frio'] & temp_deseada['alta'], calentador['alto'])
regla3 = ctrl.Rule(temp_actual['muy_frio'] & temp_deseada['media'], calentador['medio'])
regla4 = ctrl.Rule(temp_actual['frio'] & temp_deseada['media'], calentador['medio'])
regla5 = ctrl.Rule(temp_actual['templado'] & temp_deseada['baja'], calentador['bajo'])
regla6 = ctrl.Rule(temp_actual['caliente'] & temp_deseada['baja'], calentador['muy_bajo'])
regla7 = ctrl.Rule(temp_actual['muy_caliente'] & temp_deseada['muy_baja'], calentador['muy_bajo'])
regla8 = ctrl.Rule(temp_actual['extremadamente_caliente'] & temp_deseada['super_baja'], calentador['muy_bajo'])
regla9 = ctrl.Rule(temp_actual['frio'] & temp_deseada['alta'], calentador['alto'])
regla10 = ctrl.Rule(temp_actual['templado'] & temp_deseada['alta'], calentador['medio'])

# Creación del sistema de control
sistema_calentador = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5, regla6, regla7, regla8, regla9, regla10])
simulacion_calentador = ctrl.ControlSystemSimulation(sistema_calentador)

# Menú interactivo para ingresar las temperaturas
temp_actual_input, temp_deseada_input = mostrar_menu()

# Simulación del sistema de control
simulacion_calentador.input['temp_actual'] = temp_actual_input
simulacion_calentador.input['temp_deseada'] = temp_deseada_input

# Ejecutamos la simulación
try:
    simulacion_calentador.compute()
    # Mostramos el resultado en color
    print(Fore.MAGENTA + Style.BRIGHT + f"\nEl porcentaje de uso del calentador es: {simulacion_calentador.output['calentador']:.2f}%")
except Exception as e:
    print(Fore.RED + f"Ocurrió un error durante la simulación: {e}")

# Mostramos las gráficas
temp_actual.view()
temp_deseada.view()
calentador.view(simulacion_calentador)
plt.show()
