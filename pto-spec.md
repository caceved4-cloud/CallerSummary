# Especificación de Producto (Product Spec): Rastreador de Vacaciones (PTO Tracker) - MVP

## 1. Visión y Objetivo
Crear una herramienta interna ligera y fácil de usar que permita a los empleados solicitar tiempo libre remunerado (PTO) y a los gerentes aprobar o rechazar estas solicitudes. El objetivo de este Producto Mínimo Viable (MVP) es eliminar el uso de hojas de cálculo manuales y centralizar las solicitudes para evitar conflictos de programación en los equipos.

## 2. Usuarios Objetivo
- **Empleado**: Desea ver su saldo de días disponibles, solicitar días libres y ver el estado de sus solicitudes.
- **Gerente**: Necesita ser notificado de las solicitudes de su equipo, visualizar un calendario para evitar superposiciones y aprobar/rechazar peticiones.
- **Administrador (RRHH)**: Requiere una vista general de todos los saldos y la capacidad de ajustar la cantidad de días anuales por empleado.

## 3. Historias de Usuario Principales (User Stories)
- Como empleado, quiero ver mi saldo actual de días de vacaciones en la pantalla principal para saber cuánto tiempo puedo solicitar.
- Como empleado, quiero un formulario sencillo (fecha de inicio, fecha de fin, motivo) para solicitar tiempo libre.
- Como gerente, quiero ver una lista de solicitudes pendientes de mi equipo para poder aprobarlas o rechazarlas con un solo clic.
- Como gerente, quiero ver un calendario visual de las ausencias aprobadas para asegurar la cobertura del equipo.

## 4. Requisitos Funcionales (Core Features)
- **Autenticación Básica**: Inicio de sesión simple con correo corporativo y contraseña.
- **Dashboard del Empleado**: Tarjeta con el saldo de días y tabla con el historial de solicitudes (Estado: Pendiente, Aprobado, Rechazado).
- **Dashboard del Gerente**: Vista de tabla con solicitudes entrantes y botones de acción rápida (Aprobar/Rechazar).

### Reglas de Negocio
- No se pueden solicitar fechas en el pasado.
- No se pueden solicitar más días de los que se tienen en el saldo.
- Los fines de semana no se descuentan del saldo de vacaciones.

## 5. Modelo de Datos Sugerido (Para Spec-Driven Development)
Para facilitar la generación de código con Claude Code, el sistema requerirá dos entidades principales:

- **User (Usuario)**: id, nombre, email, rol (empleado/gerente), manager_id, saldo_pto.
- **Request (Solicitud)**: id, user_id, fecha_inicio, fecha_fin, estado (pendiente/aprobada/rechazada), motivo.

## 6. Criterios de Éxito
- Los empleados pueden completar una solicitud de PTO en menos de 1 minuto.
- El sistema calcula correctamente los días hábiles solicitados descontándolos del saldo únicamente cuando la solicitud es aprobada por el gerente.
