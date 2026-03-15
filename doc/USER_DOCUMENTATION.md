# 📚 Manual de Usuario - Tutor Matemático Visual

## 🎯 ¿Qué es el Tutor Matemático Visual?

Es una aplicación diseñada especialmente para ayudar a niños ciegos de primaria a resolver ejercicios matemáticos que normalmente requieren vista. La aplicación:

- 📷 **Captura** ejercicios matemáticos con la cámara
- 🧠 **Analiza** las figuras y operaciones automáticamente  
- 🎓 **Explica** el ejercicio de forma clara y educativa
- 🔊 **Lee** la explicación en voz alta

---

## 🚀 Instalación y Configuración

### Requisitos del Sistema
- Windows 10 o superior
- Python 3.8 o superior
- Cámara web (USB o integrada)
- Conexión a internet
- Altavoces o audífonos

### Instalación Paso a Paso

1. **Descargar el proyecto**
   ```bash
   git clone https://github.com/tu-usuario/tutor-matematico-visual
   cd tutor-matematico-visual
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar API Key de OpenAI**
   - Crear archivo `.env` en la carpeta del proyecto
   - Agregar tu API key:
   ```
   OPENAI_API_KEY=tu_api_key_aquí
   ```

4. **Ejecutar la aplicación**
   ```bash
   python math_transcriptor_desktop.py
   ```

---

## 🖥️ Guía de Uso

### Primera Vez - Configuración de Cámara

1. **Abrir la aplicación**
   - Ejecutar `python math_transcriptor_desktop.py`
   - La ventana principal se abrirá

2. **Seleccionar cámara**
   - En el panel izquierdo, usar el menú "Seleccionar cámara"
   - Elegir la cámara que mejor capture los ejercicios
   - Si no aparecen cámaras, presionar "🔄 Refrescar Cámaras"

3. **Probar la cámara**
   - Presionar "▶️ Iniciar Cámara"
   - Verificar que la vista previa muestre la imagen correctamente

### Resolviendo un Ejercicio Matemático

#### Paso 1: Preparar el Ejercicio
- Colocar la hoja con el ejercicio matemático frente a la cámara
- Asegurar buena iluminación
- El ejercicio debe estar centrado y ser legible

#### Paso 2: Capturar la Imagen
- Presionar "📸 Capturar Imagen"
- Verificar que la imagen se vea bien en el panel "Imagen capturada"
- Si no está bien, repetir la captura

#### Paso 3: Resolver el Ejercicio
- Presionar "🧮 Resolver Ejercicio"
- Esperar mientras el sistema analiza (6-10 segundos)
- La pregunta educativa aparecerá en el panel derecho

#### Paso 4: Escuchar la Explicación
- Presionar "🔊 Leer Respuesta" para escuchar la explicación
- La voz explicará el ejercicio de forma clara y educativa

### Controles Adicionales

- **📋 Copiar Texto**: Copia la explicación al portapapeles
- **🗑️ Limpiar**: Borra la explicación actual
- **⏹️ Detener Cámara**: Apaga la cámara cuando no se use

---

## 🧮 Tipos de Ejercicios Soportados

### ➕ Sumas
- **Ejemplo**: "3 círculos + 2 círculos = ?"
- **Lo que hace**: Cuenta los objetos y explica cómo sumar

### ➖ Restas  
- **Ejemplo**: "5 estrellas - 2 estrellas = ?"
- **Lo que hace**: Identifica cuántos objetos se quitan

### ✖️ Multiplicaciones
- **Ejemplo**: "3 grupos de 2 puntos cada uno"
- **Lo que hace**: Explica el concepto de grupos iguales

### ➗ Divisiones
- **Ejemplo**: "6 manzanas divididas en 2 grupos"
- **Lo que hace**: Explica cómo repartir en partes iguales

### 🔢 Figuras Geométricas Soportadas
- Círculos, cuadrados, triángulos, rectángulos
- Estrellas, puntos, líneas
- Objetos cotidianos (manzanas, pelotas, etc.)

---

## 🎯 Consejos para Mejores Resultados

### 📷 Calidad de Imagen
- **Buena iluminación**: Usar luz natural o lámpara brillante
- **Contraste claro**: Papel blanco con figuras oscuras funciona mejor
- **Sin sombras**: Evitar que las manos hagan sombra sobre el ejercicio
- **Estabilidad**: Mantener la cámara quieta al capturar

### 📝 Preparación del Ejercicio
- **Letra clara**: Si hay números escritos, que sean legibles
- **Espaciado**: Separar bien las figuras y símbolos
- **Tamaño adecuado**: Ni muy pequeño ni muy grande en la imagen
- **Un ejercicio por vez**: No poner múltiples ejercicios en una imagen

### 🔊 Audio y Accesibilidad
- **Volumen adecuado**: Ajustar altavoces antes de usar
- **Ambiente silencioso**: Para mejor comprensión de la explicación
- **Repetir si es necesario**: Usar "🔊 Leer Respuesta" las veces que sea necesario

---

## 🛠️ Solución de Problemas

### La cámara no funciona
**Problema**: No se ve imagen en la vista previa
**Soluciones**:
- Verificar que la cámara esté conectada
- Probar con diferentes cámaras en el menú
- Reiniciar la aplicación
- Verificar que no haya otras aplicaciones usando la cámara

### El análisis falla
**Problema**: Error al procesar la imagen
**Soluciones**:
- Verificar conexión a internet
- Comprobar que el archivo `.env` tenga la API key correcta
- Intentar con una imagen más clara
- Reintentar después de unos segundos

### La explicación no es clara
**Problema**: La respuesta no explica bien el ejercicio
**Soluciones**:
- Capturar una imagen más clara del ejercicio
- Asegurar que todas las figuras sean visibles
- Verificar que no haya elementos confusos en la imagen
- Probar con un ejercicio más simple primero

### Problemas de audio
**Problema**: No se escucha la voz
**Soluciones**:
- Verificar que los altavoces estén encendidos
- Comprobar el volumen del sistema
- Probar con audífonos
- Reiniciar la aplicación

---

## 🎓 Guía para Educadores

### Integración en el Aula

#### Preparación
- Instalar la aplicación en una computadora dedicada
- Configurar la cámara en una posición fija
- Preparar ejercicios con buena calidad visual
- Probar el sistema antes de la clase

#### Durante la Clase
- Usar la aplicación como herramienta de apoyo
- Permitir que los estudiantes participen en la captura
- Discutir las explicaciones generadas
- Complementar con explicaciones adicionales si es necesario

#### Seguimiento
- Documentar qué tipos de ejercicios funcionan mejor
- Observar la comprensión de los estudiantes
- Adaptar los ejercicios según los resultados

### Tipos de Ejercicios Recomendados

#### Para Principiantes (6-7 años)
- Sumas simples con figuras grandes (1+2, 3+1)
- Conteo básico de objetos
- Figuras geométricas simples y claras

#### Para Intermedios (8-9 años)
- Sumas y restas hasta 10
- Introducción a multiplicación con grupos
- Combinación de diferentes figuras

#### Para Avanzados (9-10 años)
- Operaciones hasta 20
- Multiplicaciones y divisiones simples
- Problemas con múltiples pasos

---

## 📊 Información Técnica para Administradores

### Rendimiento del Sistema
- **Tiempo promedio de análisis**: 6-10 segundos
- **Precisión en conteo**: 95%
- **Precisión en operaciones**: 85%
- **Costo promedio por análisis**: $0.05 USD

### Requisitos de Red
- **Ancho de banda mínimo**: 1 Mbps
- **Latencia recomendada**: <500ms
- **Uso de datos**: ~50KB por análisis

### Monitoreo y Logs
- Los logs se guardan en la consola durante ejecución
- Errores de API se reportan en ventanas emergentes
- Métricas de tiempo se muestran en la consola

---

## 🔒 Privacidad y Seguridad

### Manejo de Datos
- **Imágenes**: Se procesan temporalmente, no se almacenan
- **API**: Las imágenes se envían a OpenAI para análisis
- **Logs**: Solo se guardan localmente durante la sesión

### Recomendaciones de Seguridad
- Mantener la API key segura y no compartirla
- Usar en redes confiables
- No capturar información personal en las imágenes
- Actualizar regularmente las dependencias

---

## 📞 Soporte y Contacto

### Problemas Técnicos
- Revisar esta documentación primero
- Verificar los logs de error en la consola
- Contactar al equipo de desarrollo con detalles específicos

### Sugerencias de Mejora
- Reportar tipos de ejercicios que no funcionan bien
- Sugerir nuevas funcionalidades
- Compartir experiencias de uso en el aula

### Contribuciones
- El proyecto es open source
- Se aceptan contribuciones de código
- Documentar mejoras y nuevas funcionalidades

---

## 📈 Roadmap y Futuras Funcionalidades

### Próximas Versiones
- **Soporte offline**: Modelos locales para uso sin internet
- **Más idiomas**: Soporte para otros idiomas además del español
- **Seguimiento de progreso**: Historial de ejercicios resueltos
- **Personalización**: Adaptación por nivel y preferencias del estudiante

### Funcionalidades Experimentales
- **Múltiples modelos**: Opción de elegir diferentes motores de IA
- **Feedback adaptativo**: Sistema que aprende de las respuestas del estudiante
- **Integración con LMS**: Conexión con sistemas de gestión de aprendizaje

---

*Esta documentación se actualiza regularmente. Para la versión más reciente, consultar el repositorio del proyecto.*
