# TALLER ABP - Elaborado por Jose Rafael Correa

**Estudiante de Ingeniería Informática**  
**Asignatura:** DISEÑO DE APLICACIONES PARA MÓVILES_B2A_27106590_20262

---

## SITUACIÓN PROBLEMA
**Control de Inventarios y Alertas de Stock Bajo para Pequeños Comercios**  
* **Situación:** Una tienda de abarrotes lleva su inventario en un cuaderno o en hojas de cálculo locales, lo que genera pérdidas por desabastecimiento de productos populares o productos vencidos, sin que el dueño reciba alertas a tiempo.
* **La Solución en la Nube:** Diseñamos una API ligera alojada en la nube conectada a una base de datos liviana, que permita registrar productos, actualizar cantidades y enviar notificaciones o consultas rápidas mediante un panel web o móvil.

---

## 1. RESUMEN DEL PROBLEMA
- **Situación actual:** La tienda de abarrotes gestiona su inventario de forma manual en cuadernos u hojas de cálculo locales.
- **Consecuencias:** Esto provoca pérdidas económicas significativas debido al desabastecimiento de productos populares, falta de control en las cantidades reales y ausencia de alertas oportunas antes de que los artículos se agoten.

## 2. SOLUCIÓN TECNOLÓGICA
Desarrollo de una aplicación web ligera y moderna basada en **Flask (Python)** y **SQLite** que centraliza la información y automatiza el control:
- **Registro de Productos:** Permite dar de alta nuevos artículos especificando nombre, stock y precio, además de enviar notificaciones y actualizar existencias en tiempo real mediante métodos HTTP (`GET`, `POST`, `PUT`, `DELETE`).
- **Módulo de Inventario:** Una interfaz visual integrada que muestra de manera dinámica todos los productos registrados, indicando la cantidad disponible y su estado logístico (**Óptimo** o **Crítico**).
- **Sistema Automatizado de Vigilancia (`/alertas/stock-bajo`):** Monitorea de forma continua las existencias y filtra automáticamente aquellos productos cuyo stock se encuentra por debajo del umbral de seguridad (< 5 unidades).

## 3. DIAGRAMA DE ARQUITECTURA
La arquitectura del sistema sigue un modelo cliente-servidor ligero de tres capas:

```text
[ Cliente / Panel Web Futurista ]
       │  (Peticiones HTTP / Fetch API)
       ▼
[ Servidor API Flask (Python) ]
       │  (Consultas SQL / SQLite Driver)
       ▼
[ Base de Datos Relacional (database.db) ]
```

- **Capa de Presentación:** Interfaz HTML/CSS incrustada con JavaScript moderno (`fetch`) para la actualización dinámica de tablas sin recargar la página.
- **Capa de Lógica (API):** Endpoints en Flask que procesan las solicitudes (Registro y gestión de productos).
- **Capa de Datos:** Base de datos relacional local (`database.db`) gestionada mediante `sqlite3` con persistencia automática de registros.

## 4. RESULTADOS OBTENIDOS
- **Eliminación del papel:** Transición exitosa de los registros manuales a una base de datos digital estructurada y segura.
- **Automatización de alertas:** Reducción del riesgo de desabastecimiento gracias al módulo de vigilancia que destaca de inmediato los productos con stock crítico en color rojo.
- **Optimización operativa:** El comerciante cuenta con una herramienta centralizada y rápida para registrar, auditar y modificar su inventario en segundos, mejorando la toma de decisiones comerciales.

## 5. INSTRUCCIONES DE DESPLIEGUE
1. **Instalar dependencias:** Ejecuta `pip install flask` en tu terminal.
2. **Ejecutar la aplicación:** Inicia el servidor ejecutando `python app.py`.
3. **Acceder al sistema:** Abre tu navegador web e ingresa a la URL `http://localhost:5000`.
