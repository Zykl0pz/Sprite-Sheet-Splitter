from PIL import Image
import os
import glob
import time

# Diccionario de algoritmos disponibles con sus descripciones
ALGORITMOS = {
    '1': {'nombre': 'NEAREST', 'constante': Image.Resampling.NEAREST, 
          'descripcion': 'Sin interpolación. Colores puros, bordes definidos pero pixelados.'},
    '2': {'nombre': 'BOX', 'constante': Image.Resampling.BOX, 
          'descripcion': 'Balanceado. Recomendado para reducir tamaño sin mucho suavizado.'},
    '3': {'nombre': 'LANCZOS', 'constante': Image.Resampling.LANCZOS, 
          'descripcion': 'Alta calidad teórica pero puede suavizar demasiado (el que usabas antes).'},
    '4': {'nombre': 'HAMMING', 'constante': Image.Resampling.HAMMING, 
          'descripcion': 'Similar a Box, buen equilibrio para reducción.'},
    '5': {'nombre': 'BILINEAR', 'constante': Image.Resampling.BILINEAR, 
          'descripcion': 'Suavizado moderado.'},
    '6': {'nombre': 'BICUBIC', 'constante': Image.Resampling.BICUBIC, 
          'descripcion': 'Suavizado avanzado.'}
}

def mostrar_menu_algoritmos():
    """Muestra menú para seleccionar algoritmo de redimensionamiento"""
    print("\n🎨 ALGORITMOS DE REDIMENSIONAMIENTO")
    print("="*70)
    print("Selecciona el algoritmo según el resultado que busques:")
    print("-"*70)
    
    for key, algo in ALGORITMOS.items():
        print(f"{key}. {algo['nombre']:10} → {algo['descripcion']}")
    
    print("7. COMPARAR todos los algoritmos (crea una imagen con cada uno)")
    print("8. RECOMENDACIÓN automática (selecciona el mejor según el caso)")
    print("-"*70)
    
    while True:
        opcion = input("👉 Selecciona algoritmo (1-8): ").strip()
        
        if opcion == '7':
            return 'COMPARAR'
        elif opcion == '8':
            return 'RECOMENDAR'
        elif opcion in ALGORITMOS:
            return opcion
        else:
            print("❌ Opción no válida. Intenta nuevamente.")

def algoritmo_recomendado(tipo_imagen, es_reduccion_grande):
    """Recomienda algoritmo según tipo de imagen y reducción"""
    print("\n🤖 RECOMENDACIÓN AUTOMÁTICA")
    print("-"*70)
    
    if tipo_imagen in ['pixel', 'logo', 'texto']:
        recomendacion = '1'  # NEAREST
        razon = "Imágenes con bordes definidos y colores planos"
    elif es_reduccion_grande:
        recomendacion = '2'  # BOX
        razon = "Reducción grande de tamaño (más de 50%)"
    else:
        recomendacion = '4'  # HAMMING
        razon = "Reducción moderada manteniendo detalles"
    
    print(f"Para tu caso, recomiendo: {ALGORITMOS[recomendacion]['nombre']}")
    print(f"Razón: {razon}")
    print(f"Descripción: {ALGORITMOS[recomendacion]['descripcion']}")
    
    confirmar = input("\n¿Usar este algoritmo? (sí/no): ").strip().lower()
    if confirmar in ['sí', 'si', 's', 'yes', 'y']:
        return recomendacion
    else:
        return mostrar_menu_algoritmos()

def detectar_tipo_imagen(ruta_imagen):
    """Intenta detectar el tipo de imagen para recomendación"""
    try:
        with Image.open(ruta_imagen) as img:
            # Análisis simple basado en modo de color y tamaño
            if img.mode in ['P', 'L']:  # Paleta o escala de grises
                return 'pixel'
            
            # Podría añadirse más lógica aquí
            return 'general'
    except:
        return 'general'

def redimensionar_con_algoritmo(ruta_entrada, ruta_salida, ancho, alto, algoritmo_key):
    """Redimensiona una imagen usando un algoritmo específico"""
    try:
        with Image.open(ruta_entrada) as img:
            algoritmo = ALGORITMOS[algoritmo_key]
            
            print(f"\n🔄 Redimensionando con {algoritmo['nombre']}...")
            tiempo_inicio = time.time()
            
            img_redimensionada = img.resize((ancho, alto), algoritmo['constante'])
            
            # Posprocesamiento opcional: enfoque ligero
            if algoritmo_key in ['2', '4']:  # Solo para BOX y HAMMING
                aplicar_enfoque = input("¿Aplicar filtro de enfoque suave para más nitidez? (sí/no): ").strip().lower()
                if aplicar_enfoque in ['sí', 'si', 's', 'yes', 'y']:
                    from PIL import ImageFilter
                    img_redimensionada = img_redimensionada.filter(ImageFilter.SHARPEN)
                    print("   ✓ Filtro de enfoque aplicado")
            
            # Calcular relación de aspecto original vs nuevo
            ancho_orig, alto_orig = img.size
            relacion_ancho = ancho / ancho_orig
            relacion_alto = alto / alto_orig
            
            img_redimensionada.save(ruta_salida, optimize=True, quality=95)
            
            tiempo_fin = time.time()
            
            return {
                'exito': True,
                'algoritmo': algoritmo['nombre'],
                'tiempo': tiempo_fin - tiempo_inicio,
                'relacion': min(relacion_ancho, relacion_alto),
                'ruta_salida': ruta_salida,
                'tamano_orig': (ancho_orig, alto_orig),
                'tamano_nuevo': (ancho, alto)
            }
            
    except Exception as e:
        return {
            'exito': False,
            'error': str(e)
        }

def comparar_algoritmos(ruta_imagen, ancho, alto):
    """Crea versiones con todos los algoritmos para comparar"""
    print("\n🔬 CREANDO VERSIÓN CON CADA ALGORITMO")
    print("="*70)
    
    nombre_base, extension = os.path.splitext(ruta_imagen)
    resultados = []
    
    for key, algoritmo in ALGORITMOS.items():
        print(f"\n📊 Probando {algoritmo['nombre']}...")
        ruta_salida = f"{nombre_base}_{algoritmo['nombre']}_{ancho}x{alto}{extension}"
        
        resultado = redimensionar_con_algoritmo(ruta_imagen, ruta_salida, ancho, alto, key)
        
        if resultado['exito']:
            resultados.append(resultado)
            print(f"   ✓ Creado: {os.path.basename(ruta_salida)}")
            print(f"   ⏱️  Tiempo: {resultado['tiempo']:.2f}s")
        else:
            print(f"   ✗ Error: {resultado['error']}")
    
    # Mostrar resumen comparativo
    print("\n" + "="*70)
    print("RESUMEN DE COMPARACIÓN")
    print("="*70)
    
    for resultado in resultados:
        relacion_porcentaje = resultado['relacion'] * 100
        print(f"{resultado['algoritmo']:10} → {resultado['tiempo']:.2f}s, "
              f"Reducción al {relacion_porcentaje:.1f}%")
    
    print(f"\n📍 Todas las versiones guardadas en: {os.path.dirname(os.path.abspath(ruta_imagen))}")
    print("   Abre las imágenes para comparar visualmente la nitidez.")

def mostrar_imagenes_directorio():
    """Muestra imágenes disponibles en el directorio actual"""
    extensiones = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff', '*.webp']
    imagenes = []
    
    for ext in extensiones:
        imagenes.extend(glob.glob(ext))
        imagenes.extend(glob.glob(ext.upper()))
    
    if not imagenes:
        print("\n❌ No se encontraron imágenes.")
        return []
    
    print(f"\n📁 Directorio: {os.getcwd()}")
    print(f"📊 Imágenes encontradas: {len(imagenes)}")
    print("-"*70)
    
    for i, img in enumerate(imagenes, 1):
        try:
            with Image.open(img) as img_obj:
                ancho, alto = img_obj.size
                tamano_kb = os.path.getsize(img) / 1024
                modo = img_obj.mode
                print(f"{i:3d}. {os.path.basename(img):30} {ancho:4d}x{alto:<4d} "
                      f"{modo:5} {tamano_kb:7.1f} KB")
        except:
            print(f"{i:3d}. {os.path.basename(img):30} ERROR al leer")
    
    return imagenes

def seleccionar_imagenes(imagenes):
    """Permite seleccionar imágenes interactivamente"""
    print("\n🎯 SELECCIÓN DE IMÁGENES")
    print("-"*70)
    print("Opciones: números (1,3,5), rangos (1-5), 'todas', o 'salir'")
    
    while True:
        seleccion = input("\n👉 Selecciona imágenes: ").strip().lower()
        
        if seleccion == 'salir':
            return []
        elif seleccion == 'todas':
            return imagenes
        
        seleccionadas = []
        try:
            partes = seleccion.replace(' ', '').split(',')
            for parte in partes:
                if '-' in parte:
                    inicio, fin = map(int, parte.split('-'))
                    seleccionadas.extend(imagenes[i-1] for i in range(inicio, fin+1) if 1 <= i <= len(imagenes))
                else:
                    idx = int(parte)
                    if 1 <= idx <= len(imagenes):
                        seleccionadas.append(imagenes[idx-1])
            
            if seleccionadas:
                print(f"\n✅ Seleccionadas: {len(seleccionadas)} imágenes")
                for img in seleccionadas[:5]:  # Mostrar máximo 5
                    print(f"   • {os.path.basename(img)}")
                if len(seleccionadas) > 5:
                    print(f"   ... y {len(seleccionadas)-5} más")
                
                confirmar = input("\n¿Continuar? (sí/no): ").strip().lower()
                if confirmar in ['sí', 'si', 's', 'yes', 'y']:
                    return seleccionadas
        except:
            print("❌ Formato incorrecto. Intenta nuevamente.")

def obtener_dimensiones():
    """Obtiene dimensiones deseadas del usuario"""
    print("\n📏 CONFIGURAR DIMENSIONES")
    print("-"*70)
    
    while True:
        try:
            ancho_str = input("Ancho deseado (píxeles, Enter para auto): ").strip()
            alto_str = input("Alto deseado (píxeles, Enter para auto): ").strip()
            
            if not ancho_str and not alto_str:
                print("⚠️  Debes especificar al menos una dimensión")
                continue
            
            ancho = int(ancho_str) if ancho_str else None
            alto = int(alto_str) if alto_str else None
            
            if (ancho and ancho <= 0) or (alto and alto <= 0):
                print("❌ Las dimensiones deben ser números positivos")
                continue
            
            # Calcular la dimensión faltante si es necesario
            if ancho and not alto:
                print("🔍 Alto calculado automáticamente (mantiene proporción)")
            elif alto and not ancho:
                print("🔍 Ancho calculado automáticamente (mantiene proporción)")
            
            return ancho, alto
            
        except ValueError:
            print("❌ Ingresa solo números válidos")

def procesar_imagenes(imagenes, ancho, alto, algoritmo_seleccionado):
    """Procesa todas las imágenes seleccionadas"""
    resultados = []
    
    for i, ruta_imagen in enumerate(imagenes, 1):
        print(f"\n{'='*70}")
        print(f"🖼️  PROCESANDO {i}/{len(imagenes)}: {os.path.basename(ruta_imagen)}")
        print(f"{'='*70}")
        
        # Detectar tipo de imagen para recomendaciones
        tipo = detectar_tipo_imagen(ruta_imagen)
        
        # Determinar si es reducción grande
        with Image.open(ruta_imagen) as img:
            ancho_orig, alto_orig = img.size
            es_reduccion_grande = (ancho and ancho < ancho_orig * 0.5) or (alto and alto < alto_orig * 0.5)
        
        # Seleccionar algoritmo final
        if algoritmo_seleccionado == 'RECOMENDAR':
            algoritmo_final = algoritmo_recomendado(tipo, es_reduccion_grande)
        else:
            algoritmo_final = algoritmo_seleccionado
        
        if algoritmo_final == 'COMPARAR':
            comparar_algoritmos(ruta_imagen, 
                               ancho or int(ancho_orig * 0.5), 
                               alto or int(alto_orig * 0.5))
            resultados.append({'comparacion': True})
            continue
        
        # Procesar imagen individual
        nombre, ext = os.path.splitext(ruta_imagen)
        algoritmo_nombre = ALGORITMOS[algoritmo_final]['nombre']
        ruta_salida = f"{nombre}_{algoritmo_nombre}_{ancho or 'auto'}x{alto or 'auto'}{ext}"
        
        # Calcular dimensiones finales si alguna es None
        ancho_final = ancho
        alto_final = alto
        
        if ancho and not alto:
            proporcion = ancho / ancho_orig
            alto_final = int(alto_orig * proporcion)
        elif alto and not ancho:
            proporcion = alto / alto_orig
            ancho_final = int(ancho_orig * proporcion)
        
        resultado = redimensionar_con_algoritmo(ruta_imagen, ruta_salida, 
                                              ancho_final, alto_final, algoritmo_final)
        
        if resultado['exito']:
            resultados.append(resultado)
            print(f"\n✅ ÉXITO: {os.path.basename(ruta_salida)}")
            print(f"   Algoritmo: {resultado['algoritmo']}")
            print(f"   De: {resultado['tamano_orig'][0]}x{resultado['tamano_orig'][1]}")
            print(f"   A: {resultado['tamano_nuevo'][0]}x{resultado['tamano_nuevo'][1]}")
            print(f"   Tiempo: {resultado['tiempo']:.2f}s")
        else:
            print(f"\n❌ ERROR: {resultado['error']}")
            resultados.append({'error': True})
    
    return resultados

def menu_principal():
    """Menú principal del programa"""
    print("\n" + "="*70)
    print("🖼️  REDIMENSIONADOR AVANZADO CON CONTROL DE NITIDEZ")
    print("="*70)
    
    while True:
        print("\n📋 MENÚ PRINCIPAL:")
        print("1. Redimensionar imágenes (completo)")
        print("2. Ver imágenes en directorio actual")
        print("3. Probar algoritmos en una imagen de ejemplo")
        print("4. Salir")
        print("-"*70)
        
        opcion = input("👉 Selecciona opción (1-4): ").strip()
        
        if opcion == '1':
            # Flujo completo
            imagenes = mostrar_imagenes_directorio()
            if not imagenes:
                continue
            
            seleccionadas = seleccionar_imagenes(imagenes)
            if not seleccionadas:
                print("❌ No se seleccionaron imágenes")
                continue
            
            ancho, alto = obtener_dimensiones()
            if not ancho and not alto:
                print("❌ No se especificaron dimensiones")
                continue
            
            print("\n" + "="*70)
            print("⚙️  CONFIGURACIÓN DE CALIDAD")
            print("="*70)
            algoritmo = mostrar_menu_algoritmos()
            
            print(f"\n🎯 RESUMEN DE OPERACIÓN:")
            print(f"   • Imágenes: {len(seleccionadas)}")
            print(f"   • Dimensiones: {'Auto' if not ancho else f'{ancho}px'} x "
                  f"{'Auto' if not alto else f'{alto}px'}")
            if algoritmo in ['COMPARAR', 'RECOMENDAR']:
                print(f"   • Algoritmo: {algoritmo}")
            elif algoritmo in ALGORITMOS:
                print(f"   • Algoritmo: {ALGORITMOS[algoritmo]['nombre']}")
            
            confirmar = input("\n¿Ejecutar redimensionamiento? (sí/no): ").strip().lower()
            if confirmar in ['sí', 'si', 's', 'yes', 'y']:
                resultados = procesar_imagenes(seleccionadas, ancho, alto, algoritmo)
                
                # Mostrar resumen final
                exitos = sum(1 for r in resultados if 'exito' in r and r['exito'])
                comparaciones = sum(1 for r in resultados if 'comparacion' in r)
                
                print("\n" + "="*70)
                print("🎉 PROCESO COMPLETADO")
                print("="*70)
                print(f"✓ Imágenes procesadas: {len(seleccionadas)}")
                print(f"✓ Redimensionadas exitosamente: {exitos}")
                if comparaciones > 0:
                    print(f"✓ Comparaciones creadas: {comparaciones}")
                print(f"\n📁 Los archivos están en: {os.getcwd()}")
        
        elif opcion == '2':
            mostrar_imagenes_directorio()
        
        elif opcion == '3':
            # Modo prueba rápida
            print("\n🔧 MODO PRUEBA RÁPIDA")
            print("-"*70)
            
            imagenes = mostrar_imagenes_directorio()
            if imagenes:
                print(f"\nSe usará la primera imagen para prueba: {imagenes[0]}")
                
                with Image.open(imagenes[0]) as img:
                    ancho_orig, alto_orig = img.size
                    ancho_prueba = ancho_orig // 2
                    alto_prueba = alto_orig // 2
                
                print(f"Tamaño prueba: {ancho_prueba}x{alto_prueba} (50% del original)")
                
                confirmar = input("\n¿Crear comparación con todos los algoritmos? (sí/no): ")
                if confirmar in ['sí', 'si', 's', 'yes', 'y']:
                    comparar_algoritmos(imagenes[0], ancho_prueba, alto_prueba)
        
        elif opcion == '4':
            print("\n👋 ¡Hasta pronto!")
            break
        
        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    # Verificar dependencias
    try:
        from PIL import Image, ImageFilter
    except ImportError:
        print("❌ ERROR: Necesitas instalar Pillow")
        print("   Ejecuta: pip install pillow")
        exit(1)
    
    # Ejecutar programa
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")