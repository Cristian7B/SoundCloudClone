# Upload Module

Este módulo contiene los componentes para subir canciones y crear playlists en la aplicación SoundCloud Clone.

## Componentes

### 1. UploadSongDialog
Diálogo modal para subir nuevas canciones.

**Props:**
- `isOpen` (boolean): Controla si el diálogo está visible
- `onClose` (function): Función que se ejecuta al cerrar el diálogo
- `onSuccess` (function): Función que se ejecuta cuando la canción se sube exitosamente

**Campos del formulario:**
- Título* (requerido)
- Descripción (opcional)
- URL del archivo de audio* (requerido)
- URL de la imagen de portada (opcional)
- Duración (opcional)
- Género (opcional)
- Álbum (opcional)

### 2. CreatePlaylistDialog
Diálogo modal para crear nuevas playlists.

**Props:**
- `isOpen` (boolean): Controla si el diálogo está visible
- `onClose` (function): Función que se ejecuta al cerrar el diálogo
- `onSuccess` (function): Función que se ejecuta cuando la playlist se crea exitosamente

**Campos del formulario:**
- Título* (requerido)
- Descripción (opcional)
- URL de la imagen de portada (opcional)
- Es pública (checkbox, por defecto true)

### 3. UploadButtons
Componente que contiene botones para abrir los diálogos de subida.

### 4. UploadPage
Página completa que incluye los botones de subida y información sobre las funcionalidades.

## Uso

### Uso básico de los diálogos:

```jsx
import { UploadSongDialog, CreatePlaylistDialog } from '../modules/upload';

function MyComponent() {
  const [showSongDialog, setShowSongDialog] = useState(false);
  const [showPlaylistDialog, setShowPlaylistDialog] = useState(false);

  const handleSongSuccess = (songData) => {
    console.log('Canción creada:', songData);
    // Actualizar estado, mostrar notificación, etc.
  };

  const handlePlaylistSuccess = (playlistData) => {
    console.log('Playlist creada:', playlistData);
    // Actualizar estado, mostrar notificación, etc.
  };

  return (
    <div>
      <button onClick={() => setShowSongDialog(true)}>
        Subir Canción
      </button>
      <button onClick={() => setShowPlaylistDialog(true)}>
        Crear Playlist
      </button>

      <UploadSongDialog
        isOpen={showSongDialog}
        onClose={() => setShowSongDialog(false)}
        onSuccess={handleSongSuccess}
      />

      <CreatePlaylistDialog
        isOpen={showPlaylistDialog}
        onClose={() => setShowPlaylistDialog(false)}
        onSuccess={handlePlaylistSuccess}
      />
    </div>
  );
}
```

### Uso de los botones integrados:

```jsx
import { UploadButtons } from '../modules/upload';

function MyComponent() {
  return (
    <div>
      <UploadButtons />
    </div>
  );
}
```

### Uso de la página completa:

```jsx
import { UploadPage } from '../modules/upload';

function App() {
  return <UploadPage />;
}
```

## APIs

Los componentes se conectan a las siguientes APIs:

- **POST** `/api/contenido/canciones/` - Para crear canciones
- **POST** `/api/contenido/playlists/` - Para crear playlists

## Características

- ✅ Diseño dark theme consistente con el resto de la aplicación
- ✅ Validación de formularios
- ✅ Manejo de errores
- ✅ Estados de carga
- ✅ Responsive design
- ✅ Animaciones suaves
- ✅ Accesibilidad (teclado, ARIA)
- ✅ Efectos visuales modernos (glassmorphism, gradientes)

## Estilos

Los componentes utilizan CSS Modules para encapsulación de estilos:

- `UploadDialog.module.css` - Estilos para los diálogos
- `UploadButtons.module.css` - Estilos para los botones
- `UploadPage.module.css` - Estilos para la página completa

Todos los estilos siguen el tema dark de la aplicación con colores principales:
- Fondo: #1a1a1a
- Texto: #ffffff
- Acento: #ff5500 (naranja)
- Bordes: #333333
