"""Genera un reporte de ventas en PDF a partir de un archivo CSV.

Uso:
    python reporte.py                      # usa data/ventas.csv
    python reporte.py otras_ventas.csv     # usa otro archivo
    python reporte.py ventas.csv salida.pdf
"""

import csv
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from fpdf import FPDF

# Columnas que el CSV debe traer sí o sí
COLUMNAS = ["fecha", "vendedor", "producto", "cantidad", "precio_unitario"]


def leer_ventas(ruta_csv):
    ruta = Path(ruta_csv)
    if not ruta.exists():
        raise FileNotFoundError(f"No encontré el archivo: {ruta}")

    with ruta.open(encoding="utf-8") as f:
        lector = csv.DictReader(f)

        faltan = [c for c in COLUMNAS if c not in (lector.fieldnames or [])]
        if faltan:
            raise ValueError(f"Al CSV le faltan columnas: {', '.join(faltan)}")

        ventas = []
        # empieza en 2 porque la fila 1 es el encabezado
        for i, fila in enumerate(lector, start=2):
            try:
                cantidad = int(fila["cantidad"])
                precio = float(fila["precio_unitario"])
            except ValueError:
                print(f"  ⚠ Fila {i} ignorada: cantidad o precio no son números")
                continue

            ventas.append({
                "fecha": fila["fecha"].strip(),
                "vendedor": fila["vendedor"].strip(),
                "producto": fila["producto"].strip(),
                "cantidad": cantidad,
                "precio": precio,
                "total": cantidad * precio,
            })

    if not ventas:
        raise ValueError("El CSV no tiene filas válidas para reportar.")
    return ventas


def resumir(ventas):
    """Devuelve totales generales y el acumulado por vendedor."""
    total_general = sum(v["total"] for v in ventas)
    unidades = sum(v["cantidad"] for v in ventas)

    por_vendedor = defaultdict(float)
    for v in ventas:
        por_vendedor[v["vendedor"]] += v["total"]

    # de mayor a menor venta
    ranking = sorted(por_vendedor.items(), key=lambda x: x[1], reverse=True)

    return {
        "total_general": total_general,
        "unidades": unidades,
        "num_ventas": len(ventas),
        "ranking": ranking,
    }


def pesos(valor):
    """Formatea un número como pesos colombianos: 1234567 -> $1.234.567"""
    return "$" + f"{valor:,.0f}".replace(",", ".")


class ReportePDF(FPDF):
    def header(self):
        self.set_fill_color(21, 101, 192)  # azul
        self.rect(0, 0, self.w, 22, style="F")
        self.set_y(6)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "Reporte de Ventas", align="C")
        self.ln(20)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")


def generar_pdf(ventas, resumen, salida):
    pdf = ReportePDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"Generado el {datetime.now():%d/%m/%Y %H:%M}", ln=True)
    pdf.ln(2)

    # --- Resumen ---
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Resumen", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"Ventas registradas: {resumen['num_ventas']}", ln=True)
    pdf.cell(0, 6, f"Unidades vendidas: {resumen['unidades']}", ln=True)
    pdf.cell(0, 6, f"Total facturado: {pesos(resumen['total_general'])}", ln=True)
    pdf.ln(4)

    # --- Ranking de vendedores ---
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Ventas por vendedor", ln=True)
    pdf.set_font("Helvetica", "", 10)
    for vendedor, total in resumen["ranking"]:
        pdf.cell(100, 6, vendedor)
        pdf.cell(0, 6, pesos(total), ln=True)
    pdf.ln(4)

    # --- Detalle ---
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Detalle", ln=True)

    encabezados = ["Fecha", "Vendedor", "Producto", "Cant.", "Total"]
    anchos = [25, 40, 55, 15, 35]

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(230, 230, 230)
    for titulo, ancho in zip(encabezados, anchos):
        pdf.cell(ancho, 7, titulo, border=1, fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    for v in ventas:
        pdf.cell(anchos[0], 6, v["fecha"], border=1)
        pdf.cell(anchos[1], 6, v["vendedor"], border=1)
        pdf.cell(anchos[2], 6, v["producto"][:30], border=1)
        pdf.cell(anchos[3], 6, str(v["cantidad"]), border=1, align="R")
        pdf.cell(anchos[4], 6, pesos(v["total"]), border=1, align="R")
        pdf.ln()

    pdf.output(salida)


def main():
    entrada = sys.argv[1] if len(sys.argv) > 1 else "data/ventas.csv"
    salida = sys.argv[2] if len(sys.argv) > 2 else "reporte_ventas.pdf"

    print(f"Leyendo {entrada} ...")
    ventas = leer_ventas(entrada)
    resumen = resumir(ventas)

    print(f"Generando {salida} ...")
    generar_pdf(ventas, resumen, salida)

    print(f"✓ Listo: {salida} ({resumen['num_ventas']} ventas, "
          f"{pesos(resumen['total_general'])})")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
