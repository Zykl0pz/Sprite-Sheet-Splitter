from PIL import Image
import os
import glob

def mostrar_imagenes_directorio():
    """Muestra todas las imágenes en el directorio actual"""
    # Extensiones de imagen comunes
    extensiones = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff', '*.webp']
    
    print("\n" + "="*60)
    print("IMÁGENES DISPONIBLES EN EL DIRECTORIO ACTUAL")
    print("="*60)
    
    imagenes = []
    for extension in extensiones:
        imagenes.extend(glob.glob(extension))
        imagenes.extend(glob.glob(extension.upper()))  # Para extensiones en mayúsculas
    
    if not imagenes:
        print("❌ No se encontraron imágenes en el directorio actual.")
        print("   Asegúrate de que haya archivos con extensiones: .jpg, .png, .gif, etc.")
        return []
    
    print(f"📁 Directorio: {os.getcwd()}")
    print(f"📊 Total de imágenes encontradas: {len(imagenes)}")
    print("-"*60)
    
    for i, imagen in enumerate(imagenes, 1):
        try:
            with Image.open(imagen) as img:
                ancho, alto = img.size
                tamano_kb = os.path.getsize(imagen) / 1024
                print(f"{i:2d}. {imagen:30} → {ancho:4d} x {alto:4d} px ({tamano_kb:.1f} KB)")
        except:
            print(f"{i:2d}. {imagen:30} → ERROR al leer la imagen")
    
    print("="*60)
    return imagenes

def seleccionar_imagenes(imagenes):
    """Permite al usuario seleccionar múltiples imágenes"""
    if not imagenes:
        return []
    
    print("\n🔍 SELECCIÓN DE IMÁGENES")
    print("-"*40)
    print("Instrucciones:")
    print("  • Ingresa los números separados por comas (ej: 1,3,5)")
    print("  • Para un rango, usa guión (ej: 1-5)")
    print("  • Para seleccionar todas, escribe: todas")
    print("  • Para cancelar, escribe: salir")
    print("-"*40)
    
    while True:
        seleccion = input("👉 ¿Qué imágenes deseas redimensionar? ").strip().lower()
        
        if seleccion == "salir":
            return []
        
        if seleccion == "todas":
            return imagenes
        
        try:
            indices = []
            partes = seleccion.replace(" ", "").split(",")
            
            for parte in partes:
                if "-" in parte:
                    # Es un rango
                    inicio, fin = map(int, parte.split("-"))
                    indices.extend(range(inicio, fin + 1))
                else:
                    # Es un número individual
                    indices.append(int(parte))
            
            # Validar índices
            imagenes_seleccionadas = []
            for indice in indices:
                if 1 <= indice <= len(imagenes):
                    imagenes_seleccionadas.append(imagenes[indice-1])
                else:
                    print(f"⚠️  Advertencia: El número {indice} está fuera de rango")
            
            if not imagenes_seleccionadas:
                print("❌ No seleccionaste ninguna imagen válida. Intenta nuevamente.")
                continue
            
            # Mostrar confirmación
            print("\n✅ Imágenes seleccionadas:")
            for img in imagenes_seleccionadas:
                print(f"   • {img}")
            
            confirmar = input("\n¿Confirmar selección? (sí/no): ").strip().lower()
            if confirmar in ['sí', 'si', 's', 'yes', 'y']:
                return imagenes_seleccionadas
            else:
                print("🔁 Reiniciando selección...\n")
                
        except ValueError:
            print("❌ Formato incorrecto. Por favor, usa números separados por comas o rangos.")
        except Exception as e:
            print(f"❌ Error: {e}")

def obtener_dimensiones():
    """Obtiene las dimensiones deseadas del usuario"""
    print("\n📏 CONFIGURACIÓN DE DIMENSIONES")
    print("-"*40)
    print("Instrucciones:")
    print("  • Ingresa solo números (sin 'px' ni otras unidades)")
    print("  • Para mantener la relación de aspecto, deja uno en blanco")
    print("  • Para cancelar, deja ambos en blanco")
    print("-"*40)
    
    while True:
        try:
            ancho_str = input("👉 Ancho deseado (en píxeles): ").strip()
            
            if not ancho_str and not input("👉 Alto deseado (en píxeles): ").strip():
                return None, None  # Cancelar
            
            alto_str = input("👉 Alto deseado (en píxeles): ").strip()
            
            # Validar entradas
            ancho = int(ancho_str) if ancho_str else None
            alto = int(alto_str) if alto_str else None
            
            if ancho is not None and ancho <= 0:
                print("❌ El ancho debe ser un número positivo.")
                continue
            if alto is not None and alto <= 0:
                print("❌ El alto debe ser un número positivo.")
                continue
            if ancho is None and alto is None:
                print("❌ Debes especificar al menos una dimensión.")
                continue
            
            return ancho, alto
            
        except ValueError:
            print("❌ Por favor, ingresa solo números válidos.")
        except Exception as e:
            print(f"❌ Error: {e}")

def redimensionar_imagen(ruta_entrada, ancho_deseado, alto_deseado):
    """Redimensiona una imagen y devuelve la ruta de salida"""
    try:
        with Image.open(ruta_entrada) as img:
            # Obtener dimensiones originales
            ancho_original, alto_original = img.size
            
            # Si solo se especifica una dimensión, mantener relación de aspecto
            if ancho_deseado and not alto_deseado:
                proporcion = ancho_deseado / ancho_original
                alto_deseado = int(alto_original * proporcion)
            elif alto_deseado and not ancho_deseado:
                proporcion = alto_deseado / alto_original
                ancho_deseado = int(ancho_original * proporcion)
            
            # Redimensionar la imagen
            img_redimensionada = img.resize((ancho_deseado, alto_deseado), Image.Resampling.LANCZOS)
            
            # Crear nombre de archivo para la salida
            nombre, extension = os.path.splitext(ruta_entrada)
            ruta_salida = f"{nombre}_{ancho_deseado}x{alto_deseado}{extension}"
            
            # Evitar sobreescribir si ya existe
            contador = 1
            while os.path.exists(ruta_salida):
                ruta_salida = f"{nombre}_{ancho_deseado}x{alto_deseado}_{contador}{extension}"
                contador += 1
            
            # Guardar la imagen redimensionada
            img_redimensionada.save(ruta_salida)
            
            return {
                'entrada': ruta_entrada,
                'salida': ruta_salida,
                'original': (ancho_original, alto_original),
                'nuevo': (ancho_deseado, alto_deseado),
                'error': None
            }
            
    except Exception as e:
        return {
            'entrada': ruta_entrada,
            'salida': None,
            'error': str(e)
        }

def mostrar_resumen(resultados):
    """Muestra un resumen de las operaciones realizadas"""
    print("\n" + "="*60)
    print("RESUMEN DE OPERACIÓN")
    print("="*60)
    
    exitosas = [r for r in resultados if not r['error']]
    fallidas = [r for r in resultados if r['error']]
    
    if exitosas:
        print(f"✅ IMÁGENES REDIMENSIONADAS EXITOSAMENTE ({len(exitosas)}):")
        print("-"*60)
        for resultado in exitosas:
            print(f"📄 {resultado['entrada']}")
            print(f"   Original: {resultado['original'][0]}x{resultado['original'][1]} px")
            print(f"   Nuevo:    {resultado['nuevo'][0]}x{resultado['nuevo'][1]} px")
            print(f"   Guardado: {resultado['salida']}")
            print()
    
    if fallidas:
        print(f"❌ IMÁGENES CON ERROR ({len(fallidas)}):")
        print("-"*60)
        for resultado in fallidas:
            print(f"📄 {resultado['entrada']}")
            print(f"   Error: {resultado['error']}")
            print()

def menu_principal():
    """Menú principal del programa"""
    print("\n" + "="*60)
    print("REDIMENSIONADOR DE IMÁGENES INTERACTIVO")
    print("="*60)
    
    while True:
        print("\n📋 MENÚ PRINCIPAL:")
        print("1. Seleccionar imágenes y redimensionar")
        print("2. Mostrar imágenes en el directorio actual")
        print("3. Cambiar directorio de trabajo")
        print("4. Salir del programa")
        print("-"*40)
        
        opcion = input("👉 Selecciona una opción (1-4): ").strip()
        
        if opcion == "1":
            # Paso 1: Mostrar imágenes disponibles
            imagenes = mostrar_imagenes_directorio()
            if not imagenes:
                continue
            
            # Paso 2: Seleccionar imágenes
            imagenes_seleccionadas = seleccionar_imagenes(imagenes)
            if not imagenes_seleccionadas:
                print("❌ Operación cancelada.")
                continue
            
            # Paso 3: Obtener dimensiones
            ancho, alto = obtener_dimensiones()
            if ancho is None and alto is None:
                print("❌ Operación cancelada.")
                continue
            
            # Confirmar antes de procesar
            print(f"\n⚠️  CONFIRMACIÓN FINAL")
            print(f"   Imágenes a redimensionar: {len(imagenes_seleccionadas)}")
            print(f"   Dimensiones: {'Auto' if not ancho else f'{ancho}px'} x {'Auto' if not alto else f'{alto}px'}")
            confirmar = input("\n¿Continuar con el redimensionamiento? (sí/no): ").strip().lower()
            
            if confirmar not in ['sí', 'si', 's', 'yes', 'y']:
                print("❌ Operación cancelada.")
                continue
            
            # Paso 4: Procesar imágenes
            print("\n⏳ Procesando imágenes...")
            resultados = []
            for i, imagen in enumerate(imagenes_seleccionadas, 1):
                print(f"   Procesando {i}/{len(imagenes_seleccionadas)}: {imagen}")
                resultado = redimensionar_imagen(imagen, ancho, alto)
                resultados.append(resultado)
            
            # Paso 5: Mostrar resultados
            mostrar_resumen(resultados)
            
            # Preguntar si quiere hacer otra operación
            continuar = input("¿Deseas realizar otra operación? (sí/no): ").strip().lower()
            if continuar not in ['sí', 'si', 's', 'yes', 'y']:
                print("👋 ¡Hasta pronto!")
                break
        
        elif opcion == "2":
            mostrar_imagenes_directorio()
        
        elif opcion == "3":
            nuevo_directorio = input("👉 Ingresa la ruta del nuevo directorio: ").strip()
            if os.path.isdir(nuevo_directorio):
                os.chdir(nuevo_directorio)
                print(f"✅ Directorio cambiado a: {nuevo_directorio}")
            else:
                print(f"❌ El directorio '{nuevo_directorio}' no existe.")
        
        elif opcion == "4":
            print("👋 ¡Hasta pronto!")
            break
        
        else:
            print("❌ Opción no válida. Por favor, selecciona 1-4.")

if __name__ == "__main__":
    # Verificar que Pillow esté instalado
    try:
        from PIL import Image
    except ImportError:
        print("❌ ERROR: Pillow no está instalado.")
        print("   Instálalo con: pip install pillow")
        exit(1)
    
    # Ejecutar el programa
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")