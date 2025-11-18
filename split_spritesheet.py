import os
from PIL import Image
import argparse

def split_spritesheet(input_file, prefix, cols, rows, 
                     start_number=0, format="PNG", remove_empty=True,
                     organize_by=None):
    """
    Divide un spritesheet en frames individuales en la carpeta 'sprites'
    
    Args:
        input_file: Ruta al spritesheet
        prefix: Prefijo para los nombres de archivo
        cols: Número de columnas
        rows: Número de filas  
        start_number: Número inicial para la numeración
        format: Formato de salida (PNG, JPEG)
        remove_empty: Eliminar frames completamente vacíos/transparentes
        organize_by: None, 'column', o 'row' para organizar en subcarpetas
    """
    
    # Crear directorio base 'sprites' en la raíz de ejecución
    base_output_dir = "sprites"
    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)
        print(f"✅ Carpeta base creada: {base_output_dir}/")
    
    # Verificar que el archivo de entrada existe
    if not os.path.exists(input_file):
        print(f"❌ Error: El archivo {input_file} no existe")
        return
    
    # Abrir la imagen
    try:
        sheet = Image.open(input_file)
        sheet_width, sheet_height = sheet.size
        
        # Calcular dimensiones de cada frame
        frame_width = sheet_width // cols
        frame_height = sheet_height // rows
        
        print(f"📊 Spritesheet: {sheet_width}x{sheet_height}")
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
                    print(f"⏭️  Frame {frame_count} vacío - omitiendo")
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
                    print(f"💾 Guardado: {folder_name}/{prefix}_{frame_number}.{format.lower()}")
                else:
                    print(f"💾 Guardado: {prefix}_{frame_number}.{format.lower()}")
                
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
    # Convertir a RGBA si no lo es
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Obtener datos de píxeles
    pixels = list(image.getdata())
    
    # Verificar si todos los píxeles son transparentes
    for pixel in pixels:
        if pixel[3] != 0:  # Si algún píxel no es transparente
            return False
    return True

def batch_split_spritesheets(configs):
    """Procesa múltiples spritesheets automáticamente en la carpeta 'sprites'"""
    for config in configs:
        input_file = config['file']
        
        print(f"\n{'='*50}")
        print(f"🔄 Procesando: {input_file}")
        print(f"{'='*50}")
        
        split_spritesheet(
            input_file,
            config['prefix'],
            config['cols'],
            config['rows'],
            config.get('start_number', 0),
            config.get('format', 'PNG'),
            config.get('remove_empty', True),
            config.get('organize_by', None)
        )

def main():
    parser = argparse.ArgumentParser(
        description='Divide spritesheets en frames individuales en la carpeta "sprites"',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Ejemplos de uso:
  # Organización normal (todos los frames en una carpeta)
  python split_spritesheet.py player.png player_walk --cols 8 --rows 2

  # Organizar por columnas
  python split_spritesheet.py player.png player_walk --cols 8 --rows 2 --organize-by column

  # Organizar por filas  
  python split_spritesheet.py player.png player_walk --cols 8 --rows 2 --organize-by row

  # Con número inicial personalizado
  python split_spritesheet.py enemy.png enemy_attack --cols 6 --rows 1 --start 10

  # Mantener frames vacíos
  python split_spritesheet.py effects.png explosion --cols 5 --rows 1 --keep-empty
        '''
    )
    
    parser.add_argument('input', help='Archivo spritesheet de entrada')
    parser.add_argument('prefix', help='Prefijo para los nombres de archivo (ej: player_walk)')
    parser.add_argument('--cols', type=int, required=True, help='Número de columnas en el spritesheet')
    parser.add_argument('--rows', type=int, required=True, help='Número de filas en el spritesheet')
    parser.add_argument('--start', type=int, default=0, help='Número inicial para los frames (por defecto: 0)')
    parser.add_argument('--format', default='PNG', choices=['PNG', 'JPEG'], help='Formato de salida (por defecto: PNG)')
    parser.add_argument('--keep-empty', action='store_true', help='Mantener frames vacíos (por defecto: se eliminan)')
    parser.add_argument('--organize-by', choices=['column', 'row'], 
                       help='Organizar frames en subcarpetas por columna o fila')
    
    args = parser.parse_args()
    
    split_spritesheet(
        args.input,
        args.prefix,
        args.cols,
        args.rows,
        args.start,
        args.format,
        not args.keep_empty,  # Invertir porque remove_empty=True por defecto
        args.organize_by
    )

if __name__ == "__main__":
    main()
