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

# 1. Definición de las variables difusas con el nuevo rango de temperatura
temp_actual = ctrl.Antecedent(np.arange(-90, 61, 1), 'temp_actual')
temp_deseada = ctrl.Antecedent(np.arange(-90, 61, 1), 'temp_deseada')
calentador = ctrl.Consequent(np.arange(0, 101, 1), 'calentador')

# 2. Creación de las funciones de pertenencia
temp_actual['super_frio'] = fuzz.trimf(temp_actual.universe, [-90, -90, -60])
temp_actual['muy_frio'] = fuzz.trimf(temp_actual.universe, [-70, -50, -30])
temp_actual['frio'] = fuzz.trimf(temp_actual.universe, [-40, -20, 0])
temp_actual['templado'] = fuzz.trimf(temp_actual.universe, [-10, 10, 30])
temp_actual['caliente'] = fuzz.trimf(temp_actual.universe, [20, 40, 50])
temp_actual['muy_caliente'] = fuzz.trimf(temp_actual.universe, [40, 50, 60])
temp_actual['extremadamente_caliente'] = fuzz.trimf(temp_actual.universe, [50, 60, 60])

temp_deseada['super_baja'] = fuzz.trimf(temp_deseada.universe, [-90, -90, -60])
temp_deseada['muy_baja'] = fuzz.trimf(temp_deseada.universe, [-70, -50, -30])
temp_deseada['baja'] = fuzz.trimf(temp_deseada.universe, [-40, -20, 0])
temp_deseada['media'] = fuzz.trimf(temp_deseada.universe, [-10, 10, 30])
temp_deseada['alta'] = fuzz.trimf(temp_deseada.universe, [20, 40, 50])
temp_deseada['muy_alta'] = fuzz.trimf(temp_deseada.universe, [40, 50, 60])
temp_deseada['extremadamente_alta'] = fuzz.trimf(temp_deseada.universe, [50, 60, 60])

calentador['muy_bajo'] = fuzz.trimf(calentador.universe, [0, 0, 25])
calentador['bajo'] = fuzz.trimf(calentador.universe, [10, 30, 50])
calentador['medio'] = fuzz.trimf(calentador.universe, [40, 50, 70])
calentador['alto'] = fuzz.trimf(calentador.universe, [60, 75, 90])
calentador['muy_alto'] = fuzz.trimf(calentador.universe, [75, 90, 100])

# 3. Definición de las reglas difusas

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

# 4. Creación del sistema de control
sistema_calentador = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5, regla6, regla7, regla8, regla9, regla10])
simulacion_calentador = ctrl.ControlSystemSimulation(sistema_calentador)

# 5. Simulación del sistema de control
simulacion_calentador.input['temp_actual'] = -5
simulacion_calentador.input['temp_deseada'] = 30

# Ejecutamos la simulación
try:
    simulacion_calentador.compute()
except Exception as e:
    print(f"Ocurrió un error durante la simulación: {e}")

# 6. Verificación y resultados
if 'calentador' in simulacion_calentador.output:
    print(f"El porcentaje de uso del calentador debe ser: {simulacion_calentador.output['calentador']:.2f}%")
    temp_actual.view()
    temp_deseada.view()
    calentador.view(simulacion_calentador)
    # Mostramos las gráficas
    plt.show()
else:
    print("Error: No se pudo calcular la salida 'calentador'. Revisa las entradas y las reglas.")
