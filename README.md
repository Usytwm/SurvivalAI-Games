# SurvivalAI-Games

| Nombre                     | Grupo | Github                                       |
| -------------------------- | ----- | -------------------------------------------- |
| Brián Ameht Inclán Quesada | C411  | [@Usytwm](https://github.com/Usytwm)         |
| Eric Lopez Tornas          | C411  | [@EricTornas](https://github.com/EricTornas) |
| Davier Sanchez Bello       | C411  | [@DavierSB](https://github.com/DavierSB)     |

## Descripción del Proyecto

Basado en el modelo clásico SugarScapes de "Growing Artificial Societies", este proyecto explora la formación de agrupaciones y la violencia en sociedades simuladas mediante inteligencia artificial. Nuestro enfoque está en cómo factores como rango de visión, movilidad, herencia de riqueza y ubicación geográfica impactan la supervivencia de agentes en un entorno donde los recursos son limitados y desigualmente distribuidos. Investigamos diversas estrategias de supervivencia y asociación para entender mejor las dinámicas de poder y supervivencia en contextos competitivos, reflejando situaciones de la vida real donde la cooperación y el conflicto juegan roles cruciales.

Para más detalles sobre el proyecto, puede consultar el reporte en el archivo [informe.pdf](https://github.com/Usytwm/SurvivalAI-Games/blob/main/docs/informe.pdf)

## ¿Cómo ejecutarlo?

Para ejecutar el proyecto necesita tener instalada la versión 3.10 de python o superior.

### Configuración inicial

Clona este repositorio en tu máquina local y navega a la carpeta del proyecto. Para configurar el entorno y las dependencias automáticamente, puedes utilizar `make`:

```bash
make setup
```

Este comando configurará un entorno virtual y instalará todas las dependencias necesarias listadas en requirements.txt.

### Ejecutar el proyecto

Para iniciar el juego, simplemente ejecuta el siguiente comando:

```bash
make run
```

### Actualizar dependencias

Si necesitas actualizar el archivo requirements.txt con las nuevas dependencias del proyecto, puedes ejecutar:

```bash
make freeze
```

Esto actualizará el archivo requirements.txt con las bibliotecas actuales del entorno.
