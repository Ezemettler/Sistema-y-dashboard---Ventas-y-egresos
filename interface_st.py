import streamlit as st
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from datetime import date

# Cargar variables de entorno
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Conexión a Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Menú lateral
st.sidebar.title("Menú")
menu_principal = st.sidebar.radio("", ["Ventas", "Egresos"], index=0)

if menu_principal == "Ventas":
    st.title("Ventas")

    if st.button("Nueva Venta"):
        st.session_state["mostrar_formulario"] = True

    if st.session_state.get("mostrar_formulario"):
        st.subheader("Registrar nueva venta")

        # Inicializar valores en session_state si no existen
        if "venta_data" not in st.session_state:
            st.session_state["venta_data"] = {
                "fecha_venta": date.today(),
                "costo_envio": 0,
                "comision": 0,
                "impuestos": 0,
                "descuento": 0,
                "nombre_cliente": "",
                "mail_cliente": "",
                "telefono_cliente": "",
                "direccion_cliente": "",
                "condicion_fiscal": "",
                "dni_cuit": "",
                "facturada": False,
                "id_canal": None,
                "id_forma_pago": None,
                "id_forma_entrega": None,
            }

        if "productos" not in st.session_state:
            st.session_state["productos"] = []

        # Formulario principal para registrar la venta
        with st.form("form_nueva_venta"):
            # Campos de la tabla ventas
            col1, col2 = st.columns(2)
            with col1:
                st.session_state["venta_data"]["fecha_venta"] = st.date_input(
                    "Fecha de la venta", value=st.session_state["venta_data"]["fecha_venta"]
                )
            with col2:
                canales = supabase.table("canales_venta").select("*").execute().data
                if canales:
                    canal_seleccionado = st.selectbox(
                        "Canal de venta",
                        [(canal["id_canal"], canal["nombre_canal"]) for canal in canales],
                        format_func=lambda x: x[1],
                        index=0 if st.session_state["venta_data"]["id_canal"] is None else next(
                            (i for i, canal in enumerate(canales) if canal["id_canal"] == st.session_state["venta_data"]["id_canal"]), 0
                        ),
                    )
                    st.session_state["venta_data"]["id_canal"] = canal_seleccionado[0]
                else:
                    st.warning("No hay canales de venta disponibles.")

            col3, col4 = st.columns(2)
            with col3:
                formas_pago = supabase.table("forma_pago").select("*").execute().data
                if formas_pago:
                    forma_pago_seleccionada = st.selectbox(
                        "Forma de pago",
                        [(fp["id_forma_pago"], fp["forma_pago"]) for fp in formas_pago],
                        format_func=lambda x: x[1],
                        index=0 if st.session_state["venta_data"]["id_forma_pago"] is None else next(
                            (i for i, fp in enumerate(formas_pago) if fp["id_forma_pago"] == st.session_state["venta_data"]["id_forma_pago"]), 0
                        ),
                    )
                    st.session_state["venta_data"]["id_forma_pago"] = forma_pago_seleccionada[0]
                else:
                    st.warning("No hay formas de pago disponibles.")
            with col4:
                formas_entrega = supabase.table("forma_entrega").select("*").execute().data
                if formas_entrega:
                    forma_entrega_seleccionada = st.selectbox(
                        "Forma de entrega",
                        [(fe["id_forma_entrega"], fe["forma_entrega"]) for fe in formas_entrega],
                        format_func=lambda x: x[1],
                        index=0 if st.session_state["venta_data"]["id_forma_entrega"] is None else next(
                            (i for i, fe in enumerate(formas_entrega) if fe["id_forma_entrega"] == st.session_state["venta_data"]["id_forma_entrega"]), 0
                        ),
                    )
                    st.session_state["venta_data"]["id_forma_entrega"] = forma_entrega_seleccionada[0]
                else:
                    st.warning("No hay formas de entrega disponibles.")

            col5, col6 = st.columns(2)
            with col5:
                st.session_state["venta_data"]["costo_envio"] = st.number_input(
                    "Costo de envío", value=st.session_state["venta_data"]["costo_envio"]
                )
            with col6:
                st.session_state["venta_data"]["comision"] = st.number_input(
                    "Comisión", value=st.session_state["venta_data"]["comision"]
                )

            col7, col8 = st.columns(2)
            with col7:
                st.session_state["venta_data"]["impuestos"] = st.number_input(
                    "Impuestos", value=st.session_state["venta_data"]["impuestos"]
                )
            with col8:
                st.session_state["venta_data"]["descuento"] = st.number_input(
                    "Descuento", value=st.session_state["venta_data"]["descuento"]
                )

            col9, col10 = st.columns(2)
            with col9:
                st.session_state["venta_data"]["nombre_cliente"] = st.text_input(
                    "Nombre del cliente", value=st.session_state["venta_data"]["nombre_cliente"]
                )
            with col10:
                st.session_state["venta_data"]["mail_cliente"] = st.text_input(
                    "Correo electrónico", value=st.session_state["venta_data"]["mail_cliente"]
                )

            col11, col12 = st.columns(2)
            with col11:
                st.session_state["venta_data"]["telefono_cliente"] = st.text_input(
                    "Teléfono", value=st.session_state["venta_data"]["telefono_cliente"]
                )
            with col12:
                st.session_state["venta_data"]["direccion_cliente"] = st.text_input(
                    "Dirección", value=st.session_state["venta_data"]["direccion_cliente"]
                )

            col13, col14 = st.columns(2)
            with col13:
                st.session_state["venta_data"]["condicion_fiscal"] = st.text_input(
                    "Condición fiscal", value=st.session_state["venta_data"]["condicion_fiscal"]
                )
            with col14:
                st.session_state["venta_data"]["dni_cuit"] = st.text_input(
                    "DNI/CUIT", value=st.session_state["venta_data"]["dni_cuit"]
                )

            st.session_state["venta_data"]["facturada"] = st.checkbox(
                "¿Facturada?", value=st.session_state["venta_data"]["facturada"]
            )

            # Mostrar los productos ya agregados
            st.markdown("### Productos añadidos")
            if st.session_state["productos"]:
                productos_db = supabase.table("productos").select("id_producto, nombre").execute().data
                productos_dict = {p["id_producto"]: p["nombre"] for p in productos_db}
                
                # Crear encabezados de columnas
                cols_header = st.columns([0.3, 4, 1, 1, 1])
                cols_header[0].markdown("**✓**")  # Checkbox header
                cols_header[1].markdown("**Producto**")
                cols_header[2].markdown("**Cantidad**")
                cols_header[3].markdown("**Precio**")
                cols_header[4].markdown("**Subtotal**")
                
                productos_a_eliminar = []
                
                # Estilo CSS para alinear el checkbox
                st.markdown("""
                    <style>
                        /* Contenedor del checkbox */
                        div[data-testid="column"] > div[data-testid="stCheckbox"] {
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            margin-top: 1.7rem;  /* Ajuste fino de la posición vertical */
                            padding: 0;
                            height: 2.5rem;
                        }
                        /* Etiqueta del checkbox */
                        div[data-testid="stCheckbox"] > label {
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            margin: 0;
                            padding: 0;
                        }
                        /* Input del checkbox */
                        div[data-testid="stCheckbox"] input {
                            margin: 0;
                            padding: 0;
                        }
                    </style>
                """, unsafe_allow_html=True)
                
                for i, producto in enumerate(st.session_state["productos"]):
                    cols = st.columns([0.3, 4, 1, 1, 1])
                    # Checkbox sin espaciador
                    if cols[0].checkbox("", key=f"seleccionar_{i}", label_visibility="collapsed"):
                        productos_a_eliminar.append(i)
                    
                    # Mostrar información del producto
                    nombre_producto = productos_dict.get(producto["id_producto"], "Producto no encontrado")
                    cols[1].text_input("", value=nombre_producto, key=f"id_producto_{i}", disabled=True)
                    cols[2].text_input("", value=str(producto["cantidad"]), key=f"cantidad_{i}", disabled=True)
                    cols[3].text_input("", value=f"${producto['precio_unitario']}", key=f"precio_unitario_{i}", disabled=True)
                    cols[4].text_input("", value=f"${producto['subtotal']}", key=f"subtotal_{i}", disabled=True)
                
                # Calcular y mostrar el total
                total = sum(p["subtotal"] for p in st.session_state["productos"])
                st.markdown("---")
                cols_total = st.columns([5, 2])
                cols_total[1].markdown(f"<h2 style='color: #ffffff; margin: 0;'>Total: ${total}</h2>", unsafe_allow_html=True)
                
                # Botones de acción
                cols_buttons = st.columns([1, 1])
                eliminar = cols_buttons[0].form_submit_button("🗑️ Eliminar seleccionados")
                registrar_venta = cols_buttons[1].form_submit_button("💾 Registrar venta")
                
                # Procesar eliminación si se presionó el botón
                if eliminar and productos_a_eliminar:
                    for idx in sorted(productos_a_eliminar, reverse=True):
                        st.session_state["productos"].pop(idx)
                    st.rerun()
            else:
                st.info("No se han añadido productos aún.")
                registrar_venta = st.form_submit_button("Registrar venta")

            if registrar_venta:
                try:
                    # Convertir la fecha a formato ISO 8601
                    venta_data = st.session_state["venta_data"]
                    venta_data["fecha_venta"] = venta_data["fecha_venta"].isoformat()  # Convertir a string

                    # Calcular el monto total
                    venta_data["monto_total"] = sum(p["subtotal"] for p in st.session_state["productos"])
                    venta_data["estado"] = "aprobada"

                    # Insertar en la tabla ventas
                    venta_insert = supabase.table("ventas").insert(venta_data).execute()

                    if venta_insert.data:
                        id_venta = venta_insert.data[0]["id_venta"]

                        # Insertar productos asociados
                        for producto in st.session_state["productos"]:
                            supabase.table("items_ventas").insert({
                                "id_venta": id_venta,
                                "id_producto": producto["id_producto"],
                                "precio_unitario": int(producto["precio_unitario"]),  # Convertir a entero
                                "cantidad": int(producto["cantidad"]),  # Convertir a entero
                                "subtotal": int(producto["subtotal"]),  # Convertir a entero
                            }).execute()

                        st.success("Venta registrada correctamente.")
                        st.session_state["mostrar_formulario"] = False
                        st.session_state["productos"] = []  # Limpiar productos
                    else:
                        st.error("Error al insertar la venta.")
                except Exception as e:
                    st.error(f"Error: {e}")

        # Formulario independiente para añadir un nuevo producto
        st.markdown("### Añadir nuevo producto")
        with st.form("form_agregar_item"):
            # Ajustamos las proporciones: 4 para producto (más ancho), 1 para cantidad y precio (más estrechos)
            cols = st.columns([4, 1, 1])
            
            # Obtener productos de la base de datos
            productos = supabase.table("productos").select("id_producto, nombre").execute().data
            if productos:
                producto_seleccionado = cols[0].selectbox(
                    "Producto",
                    [(p["id_producto"], p["nombre"]) for p in productos],
                    format_func=lambda x: x[1],  # Mostrar solo el nombre
                    key="nuevo_producto_input"
                )
                id_producto = producto_seleccionado[0]  # Obtener el ID del producto
            else:
                st.warning("No hay productos disponibles.")
                
            nueva_cantidad = cols[1].number_input(
                "Cantidad", 
                min_value=1, 
                step=1, 
                key="nueva_cantidad_input"
            )
            nuevo_precio_unitario = cols[2].number_input(
                "Precio unitario",
                min_value=0,
                step=1,
                format="%d",
                key="nuevo_precio_unitario_input"
            )

            # Botón para añadir el ítem
            form_action = st.form_submit_button("Añadir ítem")

            if form_action:
                # Validar que se haya seleccionado un producto
                if not producto_seleccionado:
                    st.warning("Debe seleccionar un producto.")
                else:
                    # Agregar el nuevo producto a la lista de productos
                    nuevo_subtotal = int(nueva_cantidad * nuevo_precio_unitario)
                    st.session_state["productos"].append({
                        "id_producto": id_producto,  # Guardar el ID del producto
                        "cantidad": int(nueva_cantidad),
                        "precio_unitario": int(nuevo_precio_unitario),
                        "subtotal": nuevo_subtotal,
                    })
                    # Forzar la recarga de la página para mostrar el producto agregado inmediatamente
                    st.rerun()

elif menu_principal == "Egresos":
    st.title("Egresos")
    st.write("Aquí se podrá cargar un egreso.")
