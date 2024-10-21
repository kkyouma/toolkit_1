from matplotlib.patches import FancyArrowPatch


def draw_arrow(
    tail_position,
    head_position,
    fig,
    invert=False,
    radius=0.5,
    text_color="black",
    kw=None,
):
    """
    Dibuja una flecha entre dos posiciones en una figura de matplotlib.

    Args:
        tail_position (tuple): Coordenadas (x, y) de la posición de la cola.
        head_position (tuple): Coordenadas (x, y) de la posición de la cabeza.
        fig (matplotlib.figure.Figure): La figura de matplotlib donde se dibujará la flecha.
        invert (bool): Si es True, invierte el arco de la flecha. Por defecto es False.
        radius (float): Curvatura del arco de la flecha. Valores positivos para curvar hacia un lado y negativos para el otro.
        text_color (str): Color de la flecha. Por defecto es 'black'.
        kw (dict): Diccionario con argumentos adicionales para FancyArrowPatch.

    Returns:
        FancyArrowPatch: El objeto de la flecha creada.
    """

    # Validación de las posiciones (deben ser tuplas de longitud 2)
    if not (isinstance(tail_position, tuple) and len(tail_position) == 2):
        raise ValueError("tail_position debe ser una tupla con 2 elementos (x, y)")
    if not (isinstance(head_position, tuple) and len(head_position) == 2):
        raise ValueError("head_position debe ser una tupla con 2 elementos (x, y)")

    # Configuración por defecto de la flecha
    if kw is None:
        kw = {}
    kw.setdefault("arrowstyle", "Simple, tail_width=0.9, head_width=4, head_length=8")
    kw.setdefault("color", text_color)
    kw.setdefault("lw", 0.5)

    # Definir el estilo de la conexión (curvatura del arco)
    connectionstyle = f"arc3,rad={-radius if invert else radius}"

    # Crear la flecha
    arrow_patch = FancyArrowPatch(
        tail_position,
        head_position,
        connectionstyle=connectionstyle,
        transform=fig.transFigure,
        **kw,
    )

    # Agregar la flecha a los parches de la figura
    fig.patches.append(arrow_patch)

    # Retornar el objeto de la flecha por si es necesario modificarlo
    return arrow_patch
