import os
from PIL import Image
import argparse
import glob
import re

def get_image_files_in_current_dir():
    """Obtiene todos los archivos de imagen en el directorio actual"""
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif', '*.tga']
    image_files = []
    
    for extension in image_extensions:
        image_files.extend(glob.glob(extension))
        image_files.extend(glob.glob(extension.upper()))
    
    return sorted(image_files)

def find_image_subdirectories(base_dir):
    """
    Busca en los subdirectorios del primer nivel que contengan archivos de imagen
    Retorna una lista de subdirectorios que contienen imágenes
    """
    image_subdirs = []
    
    try:
        # Obtener todos los elementos en el directorio base
        for item in os.listdir(base_dir):
            item_path = os.path.join(base_dir, item)
            
            # Verificar si es un directorio
            if os.path.isdir(item_path):
                # Buscar archivos de imagen en este subdirectorio
                image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif', '*.tga']
                has_images = False
                
                for extension in image_extensions:
                    # Buscar con extensión normal y en mayúsculas
                    if (glob.glob(os.path.join(item_path, extension)) or 
                        glob.glob(os.path.join(item_path, extension.upper()))):
                        has_images = True
                        break
                
                if has_images:
                    image_subdirs.append(item_path)
    
    except PermissionError:
        print(f"❌ No se pudo acceder a un directorio por falta de permisos")
    except Exception as e:
        print(f"❌ Error al escanear subdirectorios: {e}")
    
    return sorted(image_subdirs)

def clean_filename(name):
    """
    Limpia un nombre para que sea válido como nombre de archivo/carpeta
    Elimina caracteres especiales y reemplaza espacios
    """
    # Caracteres no permitidos en nombres de archivo/carpeta
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    
    # Reemplazar múltiples espacios por un solo guión bajo
    name = re.sub(r'\s+', '_', name.strip())
    
    # Asegurar que no esté vacío después de limpiar
    if not name:
        name = "unnamed"
    
    return name

def get_custom_names(count, item_type):
    """
    Solicita nombres personalizados al usuario para filas o columnas
    """
    names = []
    print(f"\n🏷️  Asignando nombres para {count} {item_type}:")
    print("   (Presiona Enter para usar nombre por defecto)")
    
    for i in range(count):
        while True:
            default_name = f"{item_type[:-1]}_{i}"  # row_0, col_1, etc.
            custom_name = input(f"   {item_type[:-1].capitalize()} {i}: ").strip()
            
            if not custom_name:
                # Usar nombre por defecto si no se ingresa nada
                names.append(default_name)
                print(f"     ✅ Usando: {default_name}")
                break
            else:
                # Limpiar el nombre personalizado
                cleaned_name = clean_filename(custom_name)
                if cleaned_name != custom_name:
                    print(f"     ✅ Nombre limpio: {cleaned_name}")
                
                # Verificar si el nombre ya fue usado
                if cleaned_name in names:
                    print(f"     ❌ Este nombre ya fue usado. Elige otro.")
                    continue
                
                names.append(cleaned_name)
                break
    
    return names

def select_file_from_current_dir():
    """Permite al usuario seleccionar un archivo de imagen del directorio actual"""
    image_files = get_image_files_in_current_dir()
    
    if not image_files:
        print("❌ No se encontraron archivos de imagen en el directorio actual.")
        return None
    
    print("\n📁 Archivos de imagen encontrados en el directorio actual:")
    for i, file in enumerate(image_files, 1):
        print(f"   {i}. {file}")
    
    while True:
        try:
            choice = input(f"\n🔢 Selecciona un archivo (1-{len(image_files)}) o escribe el nombre: ").strip()
            
            # Si es un número, seleccionar por índice
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(image_files):
                    return image_files[index]
                else:
                    print(f"❌ Por favor selecciona un número entre 1 y {len(image_files)}")
            
            # Si es texto, buscar coincidencia exacta
            elif choice in image_files:
                return choice
            
            # Si es "this" o "este", usar el primero
            elif choice.lower() in ['this', 'este', 'actual', 'current']:
                return image_files[0]
            
            else:
                print("❌ Selección inválida. Intenta nuevamente.")
                
        except ValueError:
            print("❌ Por favor ingresa un número válido.")

def select_from_subdirectories(base_dir):
    """
    Permite al usuario seleccionar entre subdirectorios que contienen imágenes
    Retorna el directorio seleccionado o None si no hay subdirectorios con imágenes
    """
    print("\n🔍 Escaneando subdirectorios en busca de spritesheets...")
    image_subdirs = find_image_subdirectories(base_dir)
    
    if not image_subdirs:
        print("❌ No se encontraron subdirectorios con archivos de imagen.")
        return None
    
    print("\n📂 Subdirectorios que contienen spritesheets:")
    print("   (Se encontraron imágenes en las siguientes carpetas)")
    
    for i, subdir in enumerate(image_subdirs, 1):
        # Mostrar solo el nombre de la carpeta, no la ruta completa
        dir_name = os.path.basename(subdir)
        print(f"   {i}. {dir_name}/")
    
    print(f"   {len(image_subdirs) + 1}. 🔙 Volver al directorio anterior")
    
    while True:
        try:
            choice = input(f"\n🔢 Selecciona un subdirectorio (1-{len(image_subdirs) + 1}): ").strip()
            
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(image_subdirs):
                    selected_dir = image_subdirs[index]
                    print(f"✅ Directorio seleccionado: {os.path.basename(selected_dir)}/")
                    return selected_dir
                elif index == len(image_subdirs):
                    print("↩️ Volviendo al directorio anterior...")
                    return None
                else:
                    print(f"❌ Por favor selecciona un número entre 1 y {len(image_subdirs) + 1}")
            else:
                print("❌ Por favor ingresa un número válido.")
                
        except ValueError:
            print("❌ Por favor ingresa un número válido.")

def get_user_input():
    """Obtiene toda la información necesaria del usuario de forma interactiva"""
    print("🎮 SpriteSheet Splitter - Modo Interactivo")
    print("=" * 50)
    
    # Archivo de entrada
    print("\n📁 Ruta del archivo spritesheet:")
    print("   - Escribe 'this' o 'este' para usar archivos del directorio actual")
    print("   - O ingresa la ruta completa del archivo")
    
    while True:
        input_path = input("👉 ").strip()
        
        if input_path.lower() in ['this', 'este', 'actual', 'current']:
            # Primero verificar si hay archivos de imagen en el directorio actual
            image_files = get_image_files_in_current_dir()
            
            if not image_files:
                # Si no hay imágenes en el directorio actual, buscar en subdirectorios
                current_dir = os.getcwd()
                selected_subdir = select_from_subdirectories(current_dir)
                
                if selected_subdir:
                    # Cambiar al subdirectorio seleccionado
                    os.chdir(selected_subdir)
                    print(f"📂 Cambiado al directorio: {os.getcwd()}")
                    # Ahora seleccionar archivo en el nuevo directorio
                    selected_file = select_file_from_current_dir()
                    if selected_file:
                        input_path = selected_file
                        break
                    else:
                        continue
                else:
                    # El usuario eligió volver o no hay subdirectorios
                    print("❌ No se encontraron archivos de imagen. Intenta nuevamente.")
                    continue
            else:
                # Hay imágenes en el directorio actual
                selected_file = select_file_from_current_dir()
                if selected_file:
                    input_path = selected_file
                    break
                else:
                    continue
        
        # Verificar si la ruta ingresada es un directorio
        if os.path.isdir(input_path):
            # Cambiar al directorio especificado
            original_dir = os.getcwd()
            os.chdir(input_path)
            current_dir = os.getcwd()
            
            # Verificar si hay imágenes en este directorio
            image_files = get_image_files_in_current_dir()
            
            if not image_files:
                # Si no hay imágenes, buscar en subdirectorios
                print(f"📂 El directorio no contiene imágenes directamente.")
                selected_subdir = select_from_subdirectories(current_dir)
                
                if selected_subdir:
                    # Cambiar al subdirectorio seleccionado
                    os.chdir(selected_subdir)
                    print(f"📂 Cambiado al directorio: {os.getcwd()}")
                    # Seleccionar archivo en el nuevo directorio
                    selected_file = select_file_from_current_dir()
                    if selected_file:
                        input_path = selected_file
                        break
                    else:
                        # Volver al directorio original si no se seleccionó archivo
                        os.chdir(original_dir)
                        continue
                else:
                    # Volver al directorio original y pedir nueva entrada
                    os.chdir(original_dir)
                    print("❌ No se encontraron archivos de imagen. Intenta nuevamente.")
                    continue
            else:
                # Hay imágenes en el directorio, seleccionar una
                selected_file = select_file_from_current_dir()
                if selected_file:
                    input_path = selected_file
                    break
                else:
                    os.chdir(original_dir)
                    continue
        
        # Verificar si es un archivo que existe
        if os.path.exists(input_path) and os.path.isfile(input_path):
            # Verificar que sea un archivo de imagen por su extensión
            image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tga']
            file_ext = os.path.splitext(input_path)[1].lower()
            
            if file_ext in image_extensions:
                break
            else:
                print("❌ El archivo seleccionado no es una imagen válida.")
        else:
            print("❌ La ruta no existe. Intenta nuevamente o escribe 'this' para ver archivos disponibles.")
    
    print(f"✅ Archivo seleccionado: {input_path}")
    
    # Columnas y filas
    while True:
        try:
            cols = int(input("\n🔢 Número de columnas en el spritesheet: "))
            rows = int(input("🔢 Número de filas en el spritesheet: "))
            if cols > 0 and rows > 0:
                break
            print("❌ Las columnas y filas deben ser números positivos.")
        except ValueError:
            print("❌ Por favor ingresa números válidos.")
    
    # Prefijo
    prefix = input("\n🏷️  Prefijo para los nombres de archivo (ej: walk, idle, attack): ").strip()
    if not prefix:
        # Usar el nombre del archivo sin extensión como prefijo por defecto
        prefix = os.path.splitext(os.path.basename(input_path))[0]
        print(f"   Usando prefijo por defecto: {prefix}")
    
    # Organización y nombres personalizados
    row_names = None
    col_names = None
    
    print("\n📂 ¿Cómo quieres organizar los frames?")
    print("   1. Todos en una sola carpeta")
    print("   2. Por columnas (cada columna en su propia carpeta)")
    print("   3. Por filas (cada fila en su propia carpeta)")
    print("   4. Por filas y columnas (estructura bidimensional)")
    
    while True:
        org_choice = input("👉 Selecciona (1-4): ").strip()
        if org_choice == '1':
            organize_by = None
            break
        elif org_choice == '2':
            organize_by = 'column'
            # Solicitar nombres personalizados para columnas
            col_names = get_custom_names(cols, "columns")
            break
        elif org_choice == '3':
            organize_by = 'row'
            # Solicitar nombres personalizados para filas
            row_names = get_custom_names(rows, "rows")
            break
        elif org_choice == '4':
            organize_by = 'both'
            # Solicitar nombres personalizados para filas y columnas
            row_names = get_custom_names(rows, "rows")
            col_names = get_custom_names(cols, "columns")
            break
        else:
            print("❌ Selección inválida. Elige 1, 2, 3 o 4.")
    
    # Mostrar vista previa de la estructura de nomenclatura
    if organize_by in ['row', 'both'] and row_names:
        print(f"\n📋 Nombres de filas: {', '.join(row_names)}")
    if organize_by in ['column', 'both'] and col_names:
        print(f"📋 Nombres de columnas: {', '.join(col_names)}")
    
    # Número inicial
    while True:
        start_str = input("\n🔢 Número inicial para los frames [0]: ").strip()
        if not start_str:
            start_number = 0
            break
        try:
            start_number = int(start_str)
            break
        except ValueError:
            print("❌ Por favor ingresa un número válido.")
    
    # Formato
    format_choice = input("\n🖼️  Formato de salida (PNG/JPEG) [PNG]: ").strip().upper()
    if format_choice not in ['PNG', 'JPEG']:
        format_choice = 'PNG'
    
    # Frames vacíos
    keep_empty = input("\n❓ ¿Mantener frames vacíos? (s/N): ").strip().lower()
    remove_empty = keep_empty not in ['s', 'si', 'sí', 'y', 'yes']
    
    return {
        'input_file': input_path,
        'prefix': prefix,
        'cols': cols,
        'rows': rows,
        'organize_by': organize_by,
        'start_number': start_number,
        'format': format_choice,
        'remove_empty': remove_empty,
        'row_names': row_names,
        'col_names': col_names
    }

def split_spritesheet(input_file, prefix, cols, rows, 
                     start_number=0, format="PNG", remove_empty=True,
                     organize_by=None, row_names=None, col_names=None):
    """
    Divide un spritesheet en frames individuales en la carpeta 'sprites'
    """
    
    # Crear directorio base 'sprites' en la raíz de ejecución
    base_output_dir = "sprites"
    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)
        print(f"\n✅ Carpeta base creada: {base_output_dir}/")
    
    # Abrir la imagen
    try:
        sheet = Image.open(input_file)
        sheet_width, sheet_height = sheet.size
        
        # Calcular dimensiones de cada frame
        frame_width = sheet_width // cols
        frame_height = sheet_height // rows
        
        print(f"\n📊 Spritesheet: {sheet_width}x{sheet_height}")
        print(f"🎬 Frames: {cols}x{rows} -> {frame_width}x{frame_height} cada uno")
        
        frame_count = 0
        saved_count = 0
        
        for row in range(rows):
            for col in range(cols):
                # Calcular coordenadas del frame
                left = col * frame_width
                upper = row * frame_height
                right = left + frame_width
                lower = upper + frame_height
                
                # Recortar el frame
                frame = sheet.crop((left, upper, right, lower))
                
                # Verificar si el frame está vacío (opcional)
                if remove_empty and is_empty_frame(frame):
                    frame_count += 1
                    continue
                
                # Determinar el directorio de salida según la organización
                output_dir = base_output_dir
                
                if organize_by == 'column':
                    # Organizar por columnas
                    col_name = col_names[col] if col_names else f"col_{col}"
                    output_dir = os.path.join(base_output_dir, col_name)
                    
                elif organize_by == 'row':
                    # Organizar por filas
                    row_name = row_names[row] if row_names else f"row_{row}"
                    output_dir = os.path.join(base_output_dir, row_name)
                    
                elif organize_by == 'both':
                    # Organizar bidimensionalmente: filas/columnas
                    row_name = row_names[row] if row_names else f"row_{row}"
                    col_name = col_names[col] if col_names else f"col_{col}"
                    output_dir = os.path.join(base_output_dir, row_name, col_name)
                
                # Crear subdirectorio si es necesario
                if organize_by and not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                # Determinar el nombre del archivo
                if organize_by == 'both':
                    # Para organización bidimensional, incluir ambos nombres
                    frame_number = start_number + saved_count
                    output_file = os.path.join(output_dir, f"{prefix}_{row_names[row] if row_names else f'row_{row}'}_{col_names[col] if col_names else f'col_{col}'}_{frame_number}.{format.lower()}")
                elif organize_by == 'row':
                    # Para organización por filas, incluir nombre de fila
                    frame_number = start_number + saved_count
                    output_file = os.path.join(output_dir, f"{prefix}_{row_names[row] if row_names else f'row_{row}'}_{frame_number}.{format.lower()}")
                elif organize_by == 'column':
                    # Para organización por columnas, incluir nombre de columna
                    frame_number = start_number + saved_count
                    output_file = os.path.join(output_dir, f"{prefix}_{col_names[col] if col_names else f'col_{col}'}_{frame_number}.{format.lower()}")
                else:
                    # Sin organización especial
                    frame_number = start_number + saved_count
                    output_file = os.path.join(output_dir, f"{prefix}_{frame_number}.{format.lower()}")
                
                # Guardar el frame
                frame.save(output_file, format.upper())
                
                # Mostrar mensaje con la ubicación
                relative_path = os.path.relpath(output_file)
                print(f"💾 {relative_path}")
                
                frame_count += 1
                saved_count += 1
        
        # Mostrar resumen de la organización
        print(f"\n📁 Organización: {organize_by if organize_by else 'sin subcarpetas'}")
        print(f"🎉 Proceso completado: {saved_count} frames guardados")
        
        if organize_by:
            print(f"📂 Carpeta base: {base_output_dir}/")
            
            if organize_by == 'column':
                if col_names:
                    print(f"📋 Subcarpetas creadas: {cols} columnas con nombres personalizados")
                    for i, name in enumerate(col_names):
                        print(f"      {i}: {name}")
                else:
                    print(f"📋 Subcarpetas creadas: {cols} columnas (col_0 a col_{cols-1})")
                    
            elif organize_by == 'row':
                if row_names:
                    print(f"📋 Subcarpetas creadas: {rows} filas con nombres personalizados")
                    for i, name in enumerate(row_names):
                        print(f"      {i}: {name}")
                else:
                    print(f"📋 Subcarpetas creadas: {rows} filas (row_0 a row_{rows-1})")
                    
            elif organize_by == 'both':
                print(f"📋 Estructura bidimensional creada:")
                if row_names:
                    print(f"   Filas: {', '.join(row_names)}")
                else:
                    print(f"   Filas: {rows} (row_0 a row_{rows-1})")
                if col_names:
                    print(f"   Columnas: {', '.join(col_names)}")
                else:
                    print(f"   Columnas: {cols} (col_0 a col_{cols-1})")
        
    except Exception as e:
        print(f"❌ Error al procesar el archivo: {e}")

def is_empty_frame(image):
    """Verifica si un frame está completamente vacío/transparente"""
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    pixels = list(image.getdata())
    for pixel in pixels:
        if pixel[3] != 0:
            return False
    return True

def main():
    # Si no hay argumentos, usar modo interactivo
    if len(os.sys.argv) == 1:
        config = get_user_input()
        split_spritesheet(**config)
    else:
        # Modo línea de comandos
        parser = argparse.ArgumentParser(
            description='Divide spritesheets en frames individuales',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''
Ejemplos de uso:
  # Modo interactivo (recomendado):
  python split_spritesheet.py

  # Modo línea de comandos:
  python split_spritesheet.py player.png walk --cols 8 --rows 2
  python split_spritesheet.py enemy.png attack --cols 6 --rows 1 --organize-by column
            '''
        )
        
        parser.add_argument('input', help='Archivo spritesheet de entrada', nargs='?')
        parser.add_argument('prefix', help='Prefijo para los nombres de archivo', nargs='?')
        parser.add_argument('--cols', type=int, help='Número de columnas en el spritesheet')
        parser.add_argument('--rows', type=int, help='Número de filas en el spritesheet')
        parser.add_argument('--start', type=int, default=0, help='Número inicial para los frames')
        parser.add_argument('--format', default='PNG', choices=['PNG', 'JPEG'], help='Formato de salida')
        parser.add_argument('--keep-empty', action='store_true', help='Mantener frames vacíos')
        parser.add_argument('--organize-by', choices=['column', 'row'], help='Organizar frames en subcarpetas')
        
        args = parser.parse_args()
        
        # Validar argumentos para modo línea de comandos
        if not all([args.input, args.prefix, args.cols, args.rows]):
            print("❌ Faltan argumentos. Usa --help para ver la ayuda.")
            return
        
        split_spritesheet(
            args.input,
            args.prefix,
            args.cols,
            args.rows,
            args.start,
            args.format,
            not args.keep_empty,
            args.organize_by
        )

if __name__ == "__main__":
    main()