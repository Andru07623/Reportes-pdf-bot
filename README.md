# Generador de Reportes PDF 🤖📄

Bot en **Python** que lee datos de ventas desde un archivo **CSV** y genera automáticamente un **reporte en PDF** con resumen, ranking de vendedores y detalle de cada venta.

Es un caso típico de automatización (RPA): tomar datos crudos repetitivos y producir un documento listo para entregar, sin trabajo manual.

---

## ¿Qué hace?

1. Lee las ventas desde un CSV y valida las columnas y los tipos de dato.
2. Calcula totales: facturación total, unidades vendidas y acumulado por vendedor.
3. Genera un PDF con:
   - Resumen general.
   - Ranking de vendedores (de mayor a menor).
   - Tabla con el detalle de cada venta.
   - Encabezado, pie de página y valores en pesos colombianos.

---

## Requisitos

- Python 3.10 o superior
- [fpdf2](https://pypi.org/project/fpdf2/)

```bash
pip install -r requirements.txt
```

---

## Uso

```bash
# Usa el CSV de ejemplo (data/ventas.csv) y crea reporte_ventas.pdf
python reporte.py

# Indicar otro CSV de entrada
python reporte.py mis_ventas.csv

# Indicar entrada y nombre del PDF de salida
python reporte.py mis_ventas.csv informe_febrero.pdf
```

---

## Formato del CSV

El archivo debe tener estas columnas (ver `data/ventas.csv` de ejemplo):

| fecha | vendedor | producto | cantidad | precio_unitario |
|-------|----------|----------|----------|-----------------|
| 2026-02-01 | Laura Gómez | Teclado mecánico | 3 | 120000 |

- `cantidad` debe ser un entero y `precio_unitario` un número.
- Las filas con datos inválidos se avisan y se omiten; el resto sí se procesa.

---

## Estructura

```
reportes-pdf-bot/
├── reporte.py           # Script principal
├── data/
│   └── ventas.csv       # Datos de ejemplo
├── requirements.txt
└── README.md
```
