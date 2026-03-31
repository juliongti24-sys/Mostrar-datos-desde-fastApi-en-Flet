import flet as ft
from typing import Any
from app.services.transacciones_api_productos import list_products,get_product,create_product, update_product, delete_product
from app.components.popup import show_popup, show_popup_auto_close, show_snackbar, confirm_dialog
from app.components.error import ApiError, api_error_to_text
from app.styles.estilos import Colors, Textos_estilos, Card
from app.views.nuevo_editar import formulario_nuevo_editar_producto #Se agrega la ventana de nuevo/editar


def products_view(page:ft.Page) -> ft.Control:
    def inicio_nuevo_producto(_e):
        #Se crea la función para transferir al formulario de nuevo producto
        async def crear_nuevo_producto (data:dict): #Esta función se lleva a la ventana para capturar
            try:
                #Se conecta a transacciones_api_productos.py para crear en la BD un nuevo produto
                create_product(data)
                await show_snackbar(page, "Éxito", "Producto creado.", bgcolor=Colors.SUCCESS)
                await actualizar_data()
            except ApiError as ex:
                await show_popup(page, "Error", api_error_to_text(ex))
            except Exception as ex:
                await show_snackbar(page, "Error", str(ex), bgcolor=Colors.DANGER)
        #Se llama a la función para abrir la ventana y poder capturar los datos,
        #regresa 3 funciones (dlg, open_ y close), se ejecuta open_()
        dlg, open_, close = formulario_nuevo_editar_producto(page, on_submit=crear_nuevo_producto, initial=None)
        open_() #Abre la ventana
        ############ FIN nuevo producto ##############
    btn_nuevo = ft.Button("Nuevo producto", icon=ft.Icons.ADD,on_click=inicio_nuevo_producto)

    rows_data:list [dict [str, Any]]=[]
    total_items=0
    total_text = ft. Text("Total de productos: (cargando...)", style=Textos_estilos.H4)
    #Encabezados
    columnas=[
    ft.DataColumn(label=ft.Text("Nombre", style=Textos_estilos.H4)),
    ft.DataColumn(label=ft.Text("Cantidad", style= Textos_estilos.H4)),
    ft.DataColumn(label=ft.Text("Ingreso", style=Textos_estilos.H4)),
    ft.DataColumn(label=ft.Text("Min", style=Textos_estilos.H4)),
    ft.DataColumn(label=ft.Text("Max", style=Textos_estilos.H4))
    ]


    #Se definen las filas de la tabla
    #Cada data.append agrega
    data=[]
    data.append(
        ft.DataRow(
            cells=[
            ft.DataCell(ft.Text("nombre1...")),
            ft.DataCell(ft.Text("cantidad1...")),
            ft.DataCell(ft.Text("ingreso1...")),
            ft.DataCell(ft.Text("min1...")),
            ft.DataCell(ft.Text("max1...")),
                ]
            )
        )

    #Se crea la tabla con los encabezados (columnas) y los datos de prueba (data)
    tabla =  ft.DataTable(
    columns=columnas,
    rows=data,
    width=900,
    heading_row_height=60,
    heading_row_color=Colors.BG,
    data_row_max_height=60,
    data_row_min_height=48
    )
    # return tabla

    async def actualizar_data():
        nonlocal rows_data, total_items
        try:
            data = list_products(limit=500, offset=0)
            
            # --- LA MAGIA ESTÁ AQUÍ ---
            # Validamos qué tipo de dato nos mandó el backend
            if isinstance(data, list):
                # Si es una lista directa de productos
                rows_data = data
                total_items = len(data)
            elif isinstance(data, dict):
                # Si es un diccionario con la estructura {"items": [...], "total": X}
                rows_data = data.get("items", [])
                total_items = int(data.get("total", 0))
            else:
                rows_data = []
                total_items = 0
            # ---------------------------

            total_text.value = f"Total de productos: {total_items}"
            actualizar_filas()
            
        except Exception as ex:
            print(f"🔥 Error en actualizar_data: {ex}")
            await show_snackbar(page, "Error al cargar datos", str(ex), bgcolor=Colors.DANGER)
    def actualizar_filas():
        nuevas_filas=[]
        for p in rows_data:
            nuevas_filas.append(
                ft.DataRow(
                    cells=[
                    ft.DataCell(ft.Text(p.get("name", ""))),
                    ft.DataCell(ft.Text(str(p.get("quantity", "")))),
                    ft.DataCell(ft.Text(p.get("ingreso_date", "") or "")),
                    ft.DataCell(ft.Text(str(p.get("min_stock", "")))),
                    ft.DataCell(ft.Text(str(p.get("max_stock", "")))),
                    ]
                )
            )
        tabla.rows = nuevas_filas
        page.update()
    page.run_task(actualizar_data)
    contenido = ft.Column (
        #expand=True,
        spacing=30,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            btn_nuevo,
            total_text,
            ft.Container(content=tabla)
            ]
        )
    tarjeta = ft. Container(content=contenido, **Card.tarjeta)
    return tarjeta
