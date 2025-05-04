import streamlit as st
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Verificar si las credenciales están configuradas
if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Error: Las credenciales de Supabase no están configuradas correctamente.")
else:
    # Conexión a Supabase
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        st.success("Conexión a Supabase exitosa.")
    except Exception as e:
        st.error(f"Error al conectar con Supabase: {e}")

    # Menú principal
    st.sidebar.title("Menú")
    menu_principal = st.sidebar.radio("", ["Ventas", "Egresos"], index=0)

    if menu_principal == "Ventas":
        st.title("Ventas")

        # Filtros de fechas
        st.subheader("Filtrar Ventas")
        fecha_inicio = st.date_input("Fecha de inicio")
        fecha_fin = st.date_input("Fecha de fin")
        if st.button("Aplicar Filtros"):
            try:
                # Construir la consulta con los filtros de fechas
                query = supabase.table("ventas").select("*")
                if fecha_inicio and fecha_fin:
                    query = query.gte("fecha_venta", fecha_inicio.strftime("%Y-%m-%d")).lte("fecha_venta", fecha_fin.strftime("%Y-%m-%d"))
                response = query.execute()

                if response.data:
                    ventas = pd.DataFrame(response.data)
                    st.session_state["ventas"] = ventas  # Guardar las ventas en el estado de la sesión
                    st.dataframe(ventas)
                else:
                    st.write("No se encontraron ventas con los filtros aplicados.")
            except Exception as e:
                st.error(f"Error al filtrar las ventas: {e}")

        # Listado de ventas
        st.subheader("Listado de Ventas")
        if "ventas" in st.session_state:
            ventas = st.session_state["ventas"]
            selected_index = st.selectbox("Selecciona una venta para editar o eliminar", ventas.index, format_func=lambda x: f"Venta ID: {ventas.loc[x, 'id_venta']} - {ventas.loc[x, 'nombre_cliente']}")
        else:
            st.write("No hay ventas cargadas.")

        # Botones de acción
        st.subheader("Acciones")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Nueva Venta"):
                st.session_state["accion"] = "nueva"
        with col2:
            if st.button("Editar Venta"):
                if "ventas" in st.session_state and "accion" not in st.session_state:
                    st.session_state["accion"] = "editar"
                    st.session_state["venta_seleccionada"] = ventas.loc[selected_index]
                else:
                    st.warning("Selecciona una venta para editar.")
        with col3:
            if st.button("Eliminar Venta"):
                if "ventas" in st.session_state and "accion" not in st.session_state:
                    st.session_state["accion"] = "eliminar"
                    st.session_state["venta_seleccionada"] = ventas.loc[selected_index]
                else:
                    st.warning("Selecciona una venta para eliminar.")

        # Acciones según el botón seleccionado
        if "accion" in st.session_state:
            if st.session_state["accion"] == "nueva":
                st.title("Nueva Venta")
                # Aquí implementaremos el formulario para registrar una nueva venta
                with st.form("form_registrar_venta"):
                    fecha_venta = st.date_input("Fecha de la venta")
                    id_canal = st.selectbox("Canal de venta", ["1 - Online", "2 - Presencial"])  # Ejemplo, ajustar con datos reales
                    id_forma_pago = st.selectbox("Forma de pago", ["1 - Efectivo", "2 - Tarjeta", "3 - Transferencia"])  # Ejemplo
                    id_forma_entrega = st.selectbox("Forma de entrega", ["1 - Envío", "2 - Retiro en tienda"])  # Ejemplo
                    descuento = st.number_input("Descuento (%)", min_value=0.0, step=0.01)
                    comision = st.number_input("Comisión (%)", min_value=0.0, step=0.01)
                    impuestos = st.number_input("Impuestos (%)", min_value=0.0, step=0.01)
                    costo_envio = st.number_input("Costo de envío", min_value=0.0, step=0.01)
                    monto_total = st.number_input("Monto total", min_value=0.0, step=0.01)
                    facturada = st.checkbox("¿Facturada?")
                    nombre_cliente = st.text_input("Nombre del cliente")
                    mail_cliente = st.text_input("Correo electrónico del cliente")
                    telefono_cliente = st.text_input("Teléfono del cliente")
                    direccion_cliente = st.text_input("Dirección del cliente")
                    condicion_fiscal = st.text_input("Condición fiscal")
                    dni_cuit = st.text_input("DNI/CUIT")
                    creado_por = st.text_input("Creado por")
                    submit_button = st.form_submit_button("Registrar Venta")

                    if submit_button:
                        try:
                            response = supabase.table("ventas").insert({
                                "fecha_venta": str(fecha_venta),
                                "id_canal": int(id_canal.split(" - ")[0]),
                                "id_forma_pago": int(id_forma_pago.split(" - ")[0]),
                                "id_forma_entrega": int(id_forma_entrega.split(" - ")[0]),
                                "descuento": descuento,
                                "comision": comision,
                                "impuestos": impuestos,
                                "costo_envio": costo_envio,
                                "monto_total": monto_total,
                                "facturada": facturada,
                                "nombre_cliente": nombre_cliente,
                                "mail_cliente": mail_cliente,
                                "telefono_cliente": telefono_cliente,
                                "direccion_cliente": direccion_cliente,
                                "condicion_fiscal": condicion_fiscal,
                                "dni_cuit": dni_cuit,
                                "creado_por": creado_por
                            }).execute()
                            st.success("Venta registrada exitosamente.")
                            st.session_state["accion"] = None  # Resetear la acción
                        except Exception as e:
                            st.error(f"Error al registrar la venta: {e}")

            elif st.session_state["accion"] == "editar":
                st.title("Editar Venta")
                venta = st.session_state["venta_seleccionada"]
                st.write(f"Editar venta ID: {venta['id_venta']}")
                # Aquí puedes implementar el formulario para editar la venta

            elif st.session_state["accion"] == "eliminar":
                st.title("Eliminar Venta")
                venta = st.session_state["venta_seleccionada"]
                st.write(f"Eliminar venta ID: {venta['id_venta']}")
                # Aquí puedes implementar la lógica para eliminar la venta

    elif menu_principal == "Egresos":
        st.title("Egresos")
        st.write("Aquí se implementarán las funciones relacionadas con egresos.")