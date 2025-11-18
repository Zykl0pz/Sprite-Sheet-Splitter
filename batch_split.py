import os
from split_spritesheet import batch_split_spritesheets

# Configuración para múltiples spritesheets
SPRITESHEET_CONFIGS = [
    {
        'file': 'player_idle.png',
        'prefix': 'idle',
        'cols': 4,
        'rows': 1,
        'start_number': 0,
        'organize_by': None  # Sin organización especial
    },
    {
        'file': 'player_walk.png', 
        'prefix': 'walk',
        'cols': 8,
        'rows': 2,
        'start_number': 0,
        'organize_by': 'column'  # Organizar por columnas
    },
    {
        'file': 'player_attack.png',
        'prefix': 'attack', 
        'cols': 6,
        'rows': 3,
        'start_number': 0,
        'organize_by': 'row'  # Organizar por filas
    },
    {
        'file': 'enemy_walk.png',
        'prefix': 'walk',
        'cols': 6,
        'rows': 1,
        'start_number': 0,
        'organize_by': None
    }
]

def main():
    print("🚀 Iniciando procesamiento por lotes de spritesheets")
    print("📁 Todos los frames se guardarán en: sprites/")
    print()
    
    # Verificar que los archivos existan
    missing_files = []
    for config in SPRITESHEET_CONFIGS:
        if not os.path.exists(config['file']):
            missing_files.append(config['file'])
    
    if missing_files:
        print("❌ Archivos faltantes:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n💡 Coloca los archivos en la misma carpeta que este script")
        return
    
    # Procesar todos los spritesheets
    batch_split_spritesheets(SPRITESHEET_CONFIGS)
    
    print("\n" + "="*50)
    print("✅ ¡Procesamiento por lotes completado!")
    print("📁 Revisa la carpeta 'sprites/' para ver los resultados")

if __name__ == "__main__":
    main()
