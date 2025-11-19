import os
from PIL import Image
import argparse
import glob

def get_image_files_in_current_dir():
    """Obtiene todos los archivos de imagen en el directorio actual"""
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif', '*.tga']
    image_files = []
    
    for extension in image_extensions:
        image_files.extend(glob.glob(extension))
        image_files.extend(glob.glob(extension.upper()))
    
    return sorted(image_files)

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

def get_user_input():
    """Obtiene toda la información necesaria del usuario de forma interactiva"""
    print("🎮 SpriteSheet Splitter - Modo Interactivo")
    print("=" * 50)
    
    # Archivo de entrada
    print("\n📁 Ruta del archivo spritesheet:")
    print("   - Escribe 'this' o 'este' para usar archivos del directorio actual")
    print("   - O ingresa la ruta completa del archivo")
    
    while True:
        input_file = input("👉 ").strip()
        
        if input_file.lower() in ['this', 'este', 'actual', 'current']:
            selected_file = select_file_from_current_dir()
            if selected_file:
                input_file = selected_file
                break
            else:
                continue
        
        if os.path.exists(input_file):
            break
        print("❌ El archivo no existe. Intenta nuevamente o escribe 'this' para ver archivos del directorio actual.")
    
    print(f"✅ Archivo seleccionado: {input_file}")
    
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
        prefix = os.path.splitext(os.path.basename(input_file))[0]
        print(f"   Usando prefijo por defecto: {prefix}")
    
    # Organización
    print("\n📂 ¿Cómo quieres organizar los frames?")
    print("   1. Todos en una sola carpeta")
    print("   2. Por columnas (cada columna en su propia carpeta)")
    print("   3. Por filas (cada fila en su propia carpeta)")
    
    while True:
        org_choice = input("👉 Selecciona (1-3): ").strip()
        if org_choice == '1':
            organize_by = None
            break
        elif org_choice == '2':
            organize_by = 'column'
            break
        elif org_choice == '3':
            organize_by = 'row'
            break
        else:
            print("❌ Selección inválida. Elige 1, 2 o 3.")
    
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
        'input_file': input_file,
        'prefix': prefix,
        'cols': cols,
        'rows': rows,
        'organize_by': organize_by,
        'start_number': start_number,
        'format': format_choice,
        'remove_empty': remove_empty
    }

def split_spritesheet(input_file, prefix, cols, rows, 
                     start_number=0, format="PNG", remove_empty=True,
                     organize_by=None):
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
                if organize_by == 'column':
                    output_dir = os.path.join(base_output_dir, f"col_{col}")
                elif organize_by == 'row':
                    output_dir = os.path.join(base_output_dir, f"row_{row}")
                else:
                    output_dir = base_output_dir
                
                # Crear subdirectorio si es necesario
                if organize_by and not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                # Guardar el frame
                frame_number = start_number + saved_count
                output_file = os.path.join(output_dir, f"{prefix}_{frame_number}.{format.lower()}")
                frame.save(output_file, format.upper())
                
                # Mostrar mensaje con la ubicación
                if organize_by:
                    folder_name = os.path.basename(output_dir)
                    print(f"💾 {folder_name}/{prefix}_{frame_number}.{format.lower()}")
                else:
                    print(f"💾 {prefix}_{frame_number}.{format.lower()}")
                
                frame_count += 1
                saved_count += 1
        
        # Mostrar resumen de la organización
        print(f"\n📁 Organización: {organize_by if organize_by else 'sin subcarpetas'}")
        print(f"🎉 Proceso completado: {saved_count} frames guardados")
        
        if organize_by:
            print(f"📂 Carpeta base: {base_output_dir}/")
            if organize_by == 'column':
                print(f"📋 Subcarpetas creadas: {cols} columnas (col_0 a col_{cols-1})")
            else:
                print(f"📋 Subcarpetas creadas: {rows} filas (row_0 a row_{rows-1})")
        
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
