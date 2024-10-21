import pandas as pd


def get_percent(
    df: pd.DataFrame, cat_col: str, group_col: str = "week", freq: str = "W"
) -> pd.DataFrame:
    """
    Calcula el porcentaje de ocurrencias de una categoría dentro de un grupo.

    Args:
        df (pd.DataFrame): DataFrame que contiene los datos.
        cat_col (str): Nombre de la columna categórica.
        group_col (str): Columna por la cual agrupar los datos (por defecto 'week').
        freq (str): Frecuencia para la agrupación temporal, si es un tipo de fecha (por defecto 'W' para semanas).

    Returns:
        pd.DataFrame: DataFrame con los porcentajes por grupo y categoría.
    """
    if group_col not in df.columns:
        raise ValueError(f"La columna '{group_col}' no existe en el DataFrame")

    if pd.api.types.is_datetime64_any_dtype(df[group_col]):
        df[group_col] = pd.to_datetime(
            df[group_col], errors="coerce"
        )  # Manejar errores de conversión a NaT
        df = df.dropna(subset=[group_col])

        df[group_col] = df[group_col].dt.to_period(freq).dt.start_time
        full_range = pd.period_range(
            df[group_col].min(), df[group_col].max(), freq=freq
        ).to_timestamp()
    else:
        full_range = df[group_col].unique()

    total_group = df.groupby(group_col).size()
    total_group_cat = df.groupby([group_col, cat_col]).size().unstack(fill_value=0)

    total_group = total_group.reindex(full_range, fill_value=0)
    total_group_cat = total_group_cat.reindex(full_range, fill_value=0)

    percent_group = total_group_cat.div(total_group, axis=0)
    percent_group = percent_group.reset_index()

    return percent_group


def sort_by_common_categories(df: pd.DataFrame, cat_col: str) -> pd.DataFrame:
    """
    Ordena un DataFrame basado en las categorías más comunes de una columna categórica.

    Args:
        df (pd.DataFrame): DataFrame que contiene los datos.
        cat_col (str): Nombre de la columna categórica.

    Returns:
        pd.DataFrame: DataFrame ordenado basado en la frecuencia de las categorías.
    """
    category_order = df[cat_col].value_counts().index
    df_sorted = df.set_index(cat_col).loc[category_order].reset_index()
    return df_sorted


def filter_common_categories(
    df: pd.DataFrame,
    cat_col: str,
    threshold: float = 0.01,
    normalize: bool = True,
    sort_by_common: bool = False,
) -> pd.DataFrame:
    """
    Filtra las filas de un DataFrame basadas en un umbral para una columna categórica,
    y opcionalmente las ordena por la frecuencia de las categorías más comunes.

    Args:
        df (pd.DataFrame): DataFrame que contiene los datos.
        cat_col (str): Nombre de la columna categórica.
        threshold (float): Umbral mínimo de proporción de las categorías para ser incluidas (por defecto 0.01).
        normalize (bool): Si se debe normalizar la cuenta de categorías (por defecto True).
        sort_by_common (bool): Si se debe ordenar el DataFrame por la frecuencia de categorías comunes (por defecto False).

    Returns:
        pd.DataFrame: DataFrame filtrado que contiene solo las categorías comunes, opcionalmente ordenado.
    """
    if cat_col not in df.columns:
        raise ValueError(f"La columna '{cat_col}' no existe en el DataFrame")

    # Filtrado basado en el umbral
    category_counts = df[cat_col].value_counts(normalize=normalize)
    common_categories = category_counts[category_counts >= threshold].index

    df_filtered = df[df[cat_col].isin(common_categories)]

    # Si sort_by_common es True, ordenamos el DataFrame
    if sort_by_common:
        df_filtered = sort_by_common_categories(df_filtered, cat_col)

    return df_filtered
