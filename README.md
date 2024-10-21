# Toolkit common usages for DataFrames

Este es un paquete de funciones de uso comun al manupular DataFrames y graficar.

### Graph module

- `arrow_func`

```python

# Definir las posiciones de la flecha usando fechas y valores del DataFrame
tail_position_data = (df['dates'].iloc[2], df['values'].iloc[2])  # Fecha y valor en el índice 2
head_position_data = (df['dates'].iloc[7], df['values'].iloc[7])  # Fecha y valor en el índice 7

# Convertir las posiciones de datos a coordenadas de la figura
tail_position_fig = ax.transData.transform(tail_position_data)
head_position_fig = ax.transData.transform(head_position_data)

# Convertir las coordenadas de la figura a coordenadas normalizadas
tail_position_norm = fig.transFigure.inverted().transform(tail_position_fig)
head_position_norm = fig.transFigure.inverted().transform(head_position_fig)

# Llamar a la función draw_arrow usando las posiciones normalizadas
draw_arrow(tail_position_norm, head_position_norm, fig, text_color="blue", radius=0.3)
```
