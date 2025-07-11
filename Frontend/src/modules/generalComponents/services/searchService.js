const API_BASE_URL = 'http://127.0.0.1:8000/api/contenido'; 
class SearchService {
  async searchSongs(query) {
    try {
      if (!query || query.length < 2) {
        return {
          termino_busqueda: query,
          total_resultados: 0,
          resultados: []
        };
      }

      const response = await fetch(`${API_BASE_URL}/canciones/buscar/?q=${encodeURIComponent(query)}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Error en la búsqueda');
      }

      return data;
    } catch (error) {
      console.error('Error searching songs:', error);
      throw error;
    }
  }

  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }
}

export default new SearchService();
