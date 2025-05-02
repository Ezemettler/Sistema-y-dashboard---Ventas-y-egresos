-- Tabla: Canales de venta
CREATE TABLE canales_venta (
  id_canal SERIAL PRIMARY KEY,
  nombre_canal TEXT NOT NULL
);

-- Tabla: Forma de pago
CREATE TABLE forma_pago (
  id_forma_pago SERIAL PRIMARY KEY,
  forma_pago TEXT NOT NULL
);

-- Tabla: Forma de entrega
CREATE TABLE forma_entrega (
  id_forma_entrega SERIAL PRIMARY KEY,
  forma_entrega TEXT NOT NULL
);

-- Tabla: Productos
CREATE TABLE productos (
  id_producto SERIAL PRIMARY KEY,
  nombre TEXT NOT NULL,
  unidad_medida TEXT NOT NULL
);

-- Tabla: Precio productos
CREATE TABLE precio_productos (
  id_precio SERIAL PRIMARY KEY,
  id_producto INT REFERENCES productos(id_producto),
  fecha_desde DATE NOT NULL,
  precio_venta NUMERIC NOT NULL
);

-- Tabla: Costo productos
CREATE TABLE costo_productos (
  id_costo SERIAL PRIMARY KEY,
  id_producto INT REFERENCES productos(id_producto),
  fecha_desde DATE NOT NULL,
  costo_unitario NUMERIC NOT NULL
);

-- Tabla: Ventas
CREATE TABLE ventas (
  id_venta SERIAL PRIMARY KEY,
  fecha_venta DATE NOT NULL,
  id_canal INT REFERENCES canales_venta(id_canal),
  id_forma_pago INT REFERENCES forma_pago(id_forma_pago),
  id_forma_entrega INT REFERENCES forma_entrega(id_forma_entrega),
  descuento NUMERIC DEFAULT 0,
  comision NUMERIC DEFAULT 0,
  impuestos NUMERIC DEFAULT 0,
  costo_envio NUMERIC DEFAULT 0,
  monto_total INT NOT NULL,
  facturada BOOLEAN DEFAULT FALSE,
  nombre_cliente TEXT,
  mail_cliente TEXT,
  telefono_cliente TEXT,
  direccion_cliente TEXT,
  condicion_fiscal TEXT,
  dni_cuit TEXT
);

-- Tabla: Items ventas
CREATE TABLE items_ventas (
  id_item_venta SERIAL PRIMARY KEY,
  id_venta INT REFERENCES ventas(id_venta),
  id_producto INT REFERENCES productos(id_producto),
  precio_unitario NUMERIC NOT NULL,
  cantidad INTEGER NOT NULL,
  costo_unitario NUMERIC NOT NULL,
  subtotal NUMERIC NOT NULL
);

-- Tabla: Proveedores
CREATE TABLE proveedores (
  id_proveedor SERIAL PRIMARY KEY,
  nombre TEXT NOT NULL,
  telefono TEXT
);

-- Tabla: Categorías de egresos
CREATE TABLE categorias_egresos (
  id_categoria SERIAL PRIMARY KEY,
  nombre_categoria TEXT NOT NULL
);

-- Tabla: Egresos
CREATE TABLE egresos (
  id_egreso SERIAL PRIMARY KEY,
  fecha_egreso DATE NOT NULL,
  id_categoria INT REFERENCES categorias_egresos(id_categoria),
  id_proveedor INT REFERENCES proveedores(id_proveedor),
  monto_total NUMERIC
);

-- Tabla: Items egreso
CREATE TABLE items_egreso (
  id_item_egreso SERIAL PRIMARY KEY,
  id_egreso INT REFERENCES egresos(id_egreso),
  concepto TEXT NOT NULL,
  precio_unitario NUMERIC NOT NULL,
  cantidad INTEGER NOT NULL,
  subtotal NUMERIC NOT NULL
);



-- Agregar campo creado_por a cada tabla
alter table canales_venta add column creado_por uuid;
alter table forma_pago add column creado_por uuid;
alter table forma_entrega add column creado_por uuid;
alter table productos add column creado_por uuid;
alter table precio_productos add column creado_por uuid;
alter table costo_productos add column creado_por uuid;
alter table ventas add column creado_por uuid;
alter table items_ventas add column creado_por uuid;
alter table proveedores add column creado_por uuid;
alter table categorias_egresos add column creado_por uuid;
alter table egresos add column creado_por uuid;
alter table items_egreso add column creado_por uuid;


-- Crear políticas RLS para permitir insertar solo si el usuario logueado coincide con el campo creado_por

-- Canales de venta
create policy "Insertar canales de ventas como usuario autenticado"
on canales_venta for insert
to authenticated
with check (auth.uid() = creado_por);

-- Forma de pago
create policy "Insertar formas de pago como usuario autenticado"
on forma_pago for insert
to authenticated
with check (auth.uid() = creado_por);

-- Forma de entrega
create policy "Insertar formas de entrega como usuario autenticado"
on forma_entrega for insert
to authenticated
with check (auth.uid() = creado_por);

-- Productos
create policy "Insertar productos como usuario autenticado"
on productos for insert
to authenticated
with check (auth.uid() = creado_por);

-- Precio de productos
create policy "Insertar precio de productos como usuario autenticado"
on precio_productos for insert
to authenticated
with check (auth.uid() = creado_por);

-- Costo de productos
create policy "Insertar costo de productos como usuario autenticado"
on costo_productos for insert
to authenticated
with check (auth.uid() = creado_por);

-- Ventas
create policy "Insertar ventas como usuario autenticado"
on ventas for insert
to authenticated
with check (auth.uid() = creado_por);

-- Items de ventas
create policy "Insertar items de ventas como usuario autenticado"
on items_ventas for insert
to authenticated
with check (auth.uid() = creado_por);

-- Proveedores
create policy "Insertar proveedores como usuario autenticado"
on proveedores for insert
to authenticated
with check (auth.uid() = creado_por);

-- Categorias de egresos
create policy "Insertar categoria de egresos como usuario autenticado"
on categorias_egresos for insert
to authenticated
with check (auth.uid() = creado_por);

-- Egresos
create policy "Insertar egresos como usuario autenticado"
on egresos for insert
to authenticated
with check (auth.uid() = creado_por);

-- Items de egreso
create policy "Insertar items de egresos como usuario autenticado"
on items_egreso for insert
to authenticated
with check (auth.uid() = creado_por);



-- Crear políticas RLS para permitir leer solo si el usuario logueado coincide con el campo creado_por

-- Canales de venta
create policy "Leer canales de ventas como usuario autenticado"
on canales_venta for select
to authenticated
using (auth.uid() = creado_por);

-- Forma de pago
create policy "Leer formas de pago como usuario autenticado"
on forma_pago for select
to authenticated
using (auth.uid() = creado_por);

-- Forma de entrega
create policy "Leer formas de entrega como usuario autenticado"
on forma_entrega for select
to authenticated
using (auth.uid() = creado_por);

-- Productos
create policy "Leer productos como usuario autenticado"
on productos for select
to authenticated
using (auth.uid() = creado_por);

-- Precio de productos
create policy "Leer precio de productos como usuario autenticado"
on precio_productos for select
to authenticated
using (auth.uid() = creado_por);

-- Costo de productos
create policy "Leer costo de productos como usuario autenticado"
on costo_productos for select
to authenticated
using (auth.uid() = creado_por);

-- Ventas
create policy "Leer ventas como usuario autenticado"
on ventas for select
to authenticated
using (auth.uid() = creado_por);

-- Items de ventas
create policy "Leer items de ventas como usuario autenticado"
on items_ventas for select
to authenticated
using (auth.uid() = creado_por);

-- Proveedores
create policy "Leer proveedores como usuario autenticado"
on proveedores for select
to authenticated
using (auth.uid() = creado_por);

-- Categorias de egresos
create policy "Leer categoria de egresos como usuario autenticado"
on categorias_egresos for select
to authenticated
using (auth.uid() = creado_por);

-- Egresos
create policy "Leer egresos como usuario autenticado"
on egresos for select
to authenticated
using (auth.uid() = creado_por);

-- Items de egreso
create policy "Leer items de egresos como usuario autenticado"
on items_egreso for select
to authenticated
using (auth.uid() = creado_por);


-- Modificar el campo costo_unitario de la tabla items_ventas para que acepte NULL
ALTER TABLE items_ventas
ALTER COLUMN costo_unitario DROP NOT NULL;
