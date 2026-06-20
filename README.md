# MiniERP - Sistemas de Gestión Empresarial

## Fase 1: Análisis y Modelado de Datos

---

### 1.1 Justificación del Modelo

#### Entidades Maestras (app: `core`)

Las entidades maestras son aquellas que representan datos de referencia estables, que no cambian frecuentemente y que son consultados por otras entidades.

- **Cliente**: Representa a las personas o empresas que realizan pedidos. Es un dato maestro porque existe de forma independiente y es referenciado por los pedidos. Tiene un campo natural único: el `nif`.
- **Producto**: Representa los artículos que se pueden vender. Es un dato maestro porque existe de forma independiente y es referenciado por las líneas de pedido. Tiene un campo natural único: el `sku` (Stock Keeping Unit).
- **EstadoPedido**: Representa los posibles estados por los que puede pasar un pedido (BORRADOR, CONFIRMADO, FACTURADO, COBRADO). Es un dato maestro porque es una tabla de referencia que no cambia.

#### Entidades Transaccionales (app: `ventas`)

Las entidades transaccionales registran operaciones del negocio que ocurren en el tiempo y dependen de las entidades maestras.

- **Pedido**: Representa la cabecera de una venta realizada a un cliente. Es transaccional porque se genera cada vez que un cliente realiza un pedido, y depende de las entidades maestras `Cliente` y `EstadoPedido`.
- **LíneaPedido**: Representa cada uno de los productos incluidos en un pedido, con su cantidad y precio unitario. Es transaccional porque depende del `Pedido` y del `Producto`.

---

#### Relaciones y Cardinalidades

| Relación | Cardinalidad | Descripción |
|---|---|---|
| Cliente → Pedido | 1:N | Un Cliente puede tener N Pedidos, pero cada Pedido pertenece a un solo Cliente |
| EstadoPedido → Pedido | 1:N | Un EstadoPedido puede aplicarse a N Pedidos, pero cada Pedido tiene un solo Estado |
| Pedido → LíneaPedido | 1:N | Un Pedido tiene N Líneas, pero cada Línea pertenece a un solo Pedido |
| Producto → LíneaPedido | 1:N | Un Producto puede aparecer en N Líneas, pero cada Línea referencia a un solo Producto |

---

#### Políticas ON_DELETE justificadas

- `Pedido.cliente` → `RESTRICT`: No se puede eliminar un Cliente si tiene pedidos asociados, para preservar el historial de ventas.
- `Pedido.estado` → `RESTRICT`: No se puede eliminar un EstadoPedido si hay pedidos con ese estado.
- `LineaPedido.pedido` → `CASCADE`: Si se elimina un Pedido, sus Líneas se eliminan también, ya que no tienen sentido sin la cabecera.
- `LineaPedido.producto` → `RESTRICT`: No se puede eliminar un Producto si aparece en alguna línea de pedido.

---

### 1.2 Diagrama Entidad-Relación

```
┌─────────────────────┐         ┌──────────────────────┐
│       CLIENTE       │         │     ESTADOPEDIDO     │
│─────────────────────│         │──────────────────────│
│ PK  id (auto)       │         │ PK  id (auto)        │
│ UQ  nif             │         │ UQ  nombre (choices) │
└──────────┬──────────┘         └──────────┬───────────┘
           │ 1                             │ 1
           │                               │
           │ N                             │ N
           │                               │
┌──────────┴───────────────────────────────┴───────────┐
│                        PEDIDO                        │
│──────────────────────────────────────────────────────│
│ PK  id (auto)                                        │
│ FK  cliente_id  ──────────────────► CLIENTE(id)      │
│ FK  estado_id   ──────────────────► ESTADOPEDIDO(id) │
│     fecha                                            │
└──────────────────────────┬───────────────────────────┘
                           │ 1
                           │
                           │ N
┌──────────────────────────┴───────────────────────────┐
│                      LINEAPEDIDO                     │
│──────────────────────────────────────────────────────│
│ PK  id (auto)                                        │
│ FK  pedido_id   ──────────────────► PEDIDO(id)       │
│ FK  producto_id ──────────────────► PRODUCTO(id)     │
│     cantidad    (CHECK: > 0)                         │
│     precio_unitario                                  │
└──────────────────────────────────────────────────────┘
                           │ N
                           │
                           │ 1
┌─────────────────────┐    │
│       PRODUCTO      ├────┘
│─────────────────────│
│ PK  id (auto)       │
│ UQ  sku             │
│     nombre          │
│     precio          │
└─────────────────────┘
```

**Leyenda:**
- `PK` = Clave Primaria (Primary Key)
- `FK` = Clave Foránea (Foreign Key)
- `UQ` = Restricción UNIQUE
- `CHECK` = Restricción a nivel de base de datos


---

## Segunda Evaluación - Nuevas Funcionalidades

### Fase 2.2 - KPI: Tasa de Conversión CRM

La **Tasa de Conversión** mide el porcentaje de oportunidades que terminan
en venta cerrada respecto al total de oportunidades registradas.

**Fórmula:**
Tasa de Conversión = (Oportunidades en etapa "CERRADA_GANADA" / Total de Oportunidades) x 100

**Cómo se calcularía con el modelo:**
```python
from crm.models import Oportunidad

total = Oportunidad.objects.count()
ganadas = Oportunidad.objects.filter(etapa='CERRADA_GANADA').count()
tasa_conversion = (ganadas / total * 100) if total > 0 else 0
print(f"Tasa de conversión: {tasa_conversion:.2f}%")
```

**Ejemplo:** Si tenemos 10 oportunidades y 3 están en "Cerrada Ganada",
la tasa de conversión es del 30%.