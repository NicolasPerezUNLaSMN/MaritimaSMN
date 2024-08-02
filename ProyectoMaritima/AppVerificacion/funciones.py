from AppMaritima.models import *

def beaufort_to_knots(beaufort):
    """
    Convierte un valor de la escala de Beaufort a la velocidad máxima en nudos.
    
    :param beaufort: Valor de la escala de Beaufort (0-12), puede ser None
    :return: Velocidad máxima del viento en nudos
    """

   


    print(f"----> {beaufort}")
    if beaufort is "null":
        beaufort = 0
    else:
        try:
            beaufort = int(beaufort)
        except ValueError:
            raise ValueError("El valor de la escala de Beaufort debe ser un número entero o 'null'")
    
    if not (0 <= beaufort <= 12):
        raise ValueError("El valor de la escala de Beaufort debe estar entre 0 y 12")

    beaufort_scale_to_knots = {
        0: (0, 1),
        1: (1, 3),
        2: (4, 6),
        3: (7, 10),
        4: (11, 16),
        5: (17, 21),
        6: (22, 27),
        7: (28, 33),
        8: (34, 40),
        9: (41, 47),
        10: (48, 55),
        11: (56, 63),
        12: (64, 71)
    }

    knots_range = beaufort_scale_to_knots[beaufort]
    return max(knots_range)  # Devolver el valor máximo del rango de nudos


def obtenerCredenciales():

    credential =  Credential.objects.order_by('-id').first()
    return credential