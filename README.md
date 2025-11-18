# 🎮 SpriteSheet Splitter Tools

Herramientas profesionales para dividir spritesheets en frames individuales, diseñadas específicamente para desarrolladores de videojuegos con libGDX.

## ✨ Características

- **División automática** de spritesheets en frames individuales
- **Múltiples modos de organización**: por columnas, filas o todos juntos
- **Formatos soportados**: PNG, JPEG
- **Detección de frames vacíos**: Opción para eliminar frames transparentes automáticamente
- **Procesamiento por lotes**: Procesa múltiples spritesheets de una vez
- **Salida organizada**: Siempre crea una carpeta `sprites/` limpia y organizada

## 🚀 Instalación Rápida

### Requisitos
- Python 3.6+
- Pillow (PIL)

```bash
# Instalar dependencias
pip install Pillow

# Descargar los scripts
git clone https://github.com/tuusuario/spritesheet-splitter-tools.git
cd spritesheet-splitter-tools
```

## 📖 Uso Básico

### 1. Uso Individual
```bash
# División básica
python split_spritesheet.py player.png walk --cols 8 --rows 2

# Organizar por columnas
python split_spritesheet.py player.png walk --cols 8 --rows 2 --organize-by column

# Organizar por filas
python split_spritesheet.py player.png walk --cols 8 --rows 2 --organize-by row

# Con número inicial personalizado
python split_spritesheet.py enemy.png attack --cols 6 --rows 1 --start 10
```

### 2. Procesamiento por Lotes
```bash
# Edita batch_split.py con tus configuraciones y ejecuta:
python batch_split.py
```

## 🛠 Parámetros Disponibles

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `input` | Archivo spritesheet de entrada | `player.png` |
| `prefix` | Prefijo para los nombres | `walk`, `idle`, `attack` |
| `--cols` | Número de columnas | `8` |
| `--rows` | Número de filas | `2` |
| `--start` | Número inicial | `0` |
| `--format` | Formato de salida | `PNG` |
| `--organize-by` | Organización | `column`, `row` |
| `--keep-empty` | Mantener frames vacíos | (flag) |

## 📁 Estructuras de Salida

### Sin Organización Especial
```
sprites/
├── walk_0.png
├── walk_1.png
├── walk_2.png
└── walk_3.png
```

### Organizado por Columnas
```
sprites/
├── col_0/
│   ├── walk_0.png
│   └── walk_1.png
├── col_1/
│   ├── walk_2.png
│   └── walk_3.png
```

### Organizado por Filas
```
sprites/
├── row_0/
│   ├── walk_0.png
│   └── walk_1.png
└── row_1/
    ├── walk_2.png
    └── walk_3.png
```

## 🎯 Flujo de Trabajo con libGDX

### 1. Preparar Assets
```
spritesheets_raw/
├── player_walk.png    # 8x2 spritesheet
├── player_idle.png    # 4x1 spritesheet
└── enemy_attack.png   # 6x1 spritesheet
```

### 2. Dividir Spritesheets
```bash
python split_spritesheet.py player_walk.png walk --cols 8 --rows 2 --organize-by column
```

### 3. Usar con TexturePacker
```
assets-raw/
└── sprites/           # ← Usar esta carpeta con TexturePacker
    ├── walk_0.png
    ├── walk_1.png
    └── ...
```

### 4. Código en libGDX
```java
// Cargar atlas
TextureAtlas atlas = new TextureAtlas(Gdx.files.internal("game.atlas"));

// Crear animación
Array<AtlasRegion> walkFrames = atlas.findRegions("walk");
Animation<TextureRegion> walkAnim = new Animation<>(0.1f, walkFrames);
```

## 🔧 Configuración Avanzada

### Ejemplo de batch_split.py
```python
SPRITESHEET_CONFIGS = [
    {
        'file': 'player_walk.png',
        'prefix': 'walk',
        'cols': 8,
        'rows': 2,
        'start_number': 0,
        'organize_by': 'column'
    },
    {
        'file': 'player_attack.png', 
        'prefix': 'attack',
        'cols': 6,
        'rows': 3,
        'start_number': 0,
        'organize_by': 'row'
    }
]
```

## 🎨 Casos de Uso Recomendados

### Para Animaciones de Personajes
```bash
# Walk cycle (8 frames, 2 direcciones)
python split_spritesheet.py player_walk.png walk --cols 8 --rows 2 --organize-by row

# Attack combo (6 frames)
python split_spritesheet.py player_attack.png attack --cols 6 --rows 1
```

### Para Efectos Visuales
```bash
# Explosión (5 frames)
python split_spritesheet.py explosion.png explode --cols 5 --rows 1 --keep-empty
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! 

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🆘 Soporte

Si encuentras algún problema:

1. Revisa los [issues](https://github.com/tuusuario/spritesheet-splitter-tools/issues)
2. Crea un nuevo issue con:
   - Tu sistema operativo
   - Versión de Python
   - Comando exacto que usaste
   - Mensaje de error completo

## 🔗 Enlaces Útiles

- [libGDX TexturePacker Documentation](https://libgdx.com/wiki/tools/texture-packer)
- [Pillow (PIL) Documentation](https://pillow.readthedocs.io/)
- [Ejemplos de Spritesheets](https://opengameart.org/)

---

**¿Te ayudaron estas herramientas?** ¡Dale una ⭐ al repositorio!

---

*Desarrollado con ❤️ para la comunidad de libGDX*
