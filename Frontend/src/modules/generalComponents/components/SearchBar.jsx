import React, { useState, useEffect, useCallback } from 'react';
import styles from "../Styles/SearchBar.module.css";
import iconoBuscar from "../assets/search.svg";
import searchService from '../services/searchService';
import SearchResults from './SearchResults';

/**
 * Componente de barra de búsqueda con resultados en tiempo real.
 * 
 * Este componente proporciona una interfaz de búsqueda completa con:
 * - Búsqueda en tiempo real con debounce
 * - Resultados desplegables
 * - Estados de carga y error
 * - Integración con el servicio de búsqueda del backend
 * 
 * @component
 * 
 * @example
 * // Uso básico en la navegación principal
 * function MainNavigation() {
 *   return (
 *     <nav>
 *       <Logo />
 *       <SearchBar />
 *       <UserMenu />
 *     </nav>
 *   );
 * }
 * 
 * @example
 * // Uso en una página de búsqueda dedicada
 * function SearchPage() {
 *   return (
 *     <div>
 *       <h1>Buscar Música</h1>
 *       <SearchBar />
 *       <SearchFilters />
 *     </div>
 *   );
 * }
 * 
 * @returns {JSX.Element} Elemento JSX de la barra de búsqueda
 * 
 * @author Tu Nombre
 * @since 1.0.0
 */
export function SearchBar() {
    /**
     * Término de búsqueda introducido por el usuario.
     * 
     * @type {string}
     */
    const [searchTerm, setSearchTerm] = useState('');

    /**
     * Resultados de la búsqueda devueltos por el servidor.
     * 
     * @type {Array<Object>}
     */
    const [searchResults, setSearchResults] = useState([]);

    /**
     * Estado de carga durante las peticiones de búsqueda.
     * 
     * @type {boolean}
     */
    const [isLoading, setIsLoading] = useState(false);

    /**
     * Mensaje de error en caso de fallo en la búsqueda.
     * 
     * @type {string|null}
     */
    const [error, setError] = useState(null);

    /**
     * Controla la visibilidad del panel de resultados.
     * 
     * @type {boolean}
     */
    const [showResults, setShowResults] = useState(false);

    /**
     * Número total de resultados encontrados.
     * 
     * @type {number}
     */
    const [totalResults, setTotalResults] = useState(0);

    /**
     * Realiza una búsqueda en el servidor con la consulta proporcionada.
     * 
     * Esta función maneja la lógica completa de búsqueda incluyendo:
     * - Validación de consulta mínima
     * - Estados de carga y error
     * - Procesamiento de resultados
     * - Actualización de la interfaz
     * 
     * @async
     * @param {string} query - Término de búsqueda
     * 
     * @example
     * // Se ejecuta automáticamente con debounce
     * performSearch("mi canción favorita");
     */
    const performSearch = useCallback(async (query) => {
        // Validar consulta mínima
        if (!query || query.length < 2) {
            setSearchResults([]);
            setTotalResults(0);
            setShowResults(false);
            setIsLoading(false);
            return;
        }

        setIsLoading(true);
        setError(null);

        try {
            // Realizar búsqueda a través del servicio
            const response = await searchService.searchSongs(query);
            setSearchResults(response.resultados || []);
            setTotalResults(response.total_resultados || 0);
            setShowResults(true);
        } catch (err) {
            setError(err.message || 'Error al buscar canciones');
            setSearchResults([]);
            setTotalResults(0);
        } finally {
            setIsLoading(false);
        }
    }, []);

    /**
     * Versión con debounce de la función de búsqueda.
     * 
     * Retrasa la ejecución de la búsqueda para evitar demasiadas
     * peticiones al servidor mientras el usuario está escribiendo.
     * 
     * @type {Function}
     */
    const debouncedSearch = useCallback(
        searchService.debounce(performSearch, 300),
        [performSearch]
    );

    /**
     * Efecto que ejecuta la búsqueda cuando cambia el término.
     * 
     * Utiliza la versión con debounce para optimizar las peticiones.
     */
    useEffect(() => {
        debouncedSearch(searchTerm);
    }, [searchTerm, debouncedSearch]);

    /**
     * Maneja los cambios en el input de búsqueda.
     * 
     * @param {Event} e - Evento de cambio del input
     */
    const handleInputChange = (e) => {
        const value = e.target.value;
        setSearchTerm(value);
        
        // Limpiar resultados si el input está vacío
        if (!value.trim()) {
            setShowResults(false);
            setSearchResults([]);
            setTotalResults(0);
        }
    };

    /**
     * Maneja el clic en el botón de búsqueda.
     * 
     * @param {Event} e - Evento de clic del botón
     */
    const handleSearchClick = (e) => {
        e.preventDefault();
        if (searchTerm.trim().length >= 2) {
            setShowResults(true);
        }
    };

    /**
     * Maneja la reproducción de una canción seleccionada.
     * 
     * @param {Object} song - Objeto con datos de la canción
     */
    const handleSongPlay = (song) => {
        console.log('Playing song:', song);
        // TODO: Implementar lógica de reproducción
    };

    /**
     * Cierra el panel de resultados de búsqueda.
     */
    const handleCloseResults = () => {
        setShowResults(false);
    };

    /**
     * Maneja las teclas presionadas en el input de búsqueda.
     * 
     * @param {KeyboardEvent} e - Evento de teclado
     */
    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSearchClick(e);
        }
        if (e.key === 'Escape') {
            setShowResults(false);
        }
    };

    /**
     * Estructura JSX de la barra de búsqueda.
     * 
     * Incluye:
     * - Input de búsqueda con eventos de teclado
     * - Botón de búsqueda con icono
     * - Componente de resultados con estado condicional
     */
    return (
        <>
            {/* Sección central con input y botón de búsqueda */}
            <div className={styles.centerSection}>
                <input
                    type="text"
                    placeholder="Buscar canciones..."
                    className={styles.searchInput}
                    value={searchTerm}
                    onChange={handleInputChange}
                    onKeyPress={handleKeyPress}
                    aria-label="Campo de búsqueda de canciones"
                />
                <button 
                    className={styles.searchButton}
                    onClick={handleSearchClick}
                    disabled={searchTerm.length < 2}
                    aria-label="Ejecutar búsqueda"
                >
                    <img src={iconoBuscar} alt="Buscar logo" />
                </button>
            </div>

            {/* Panel de resultados de búsqueda */}
            <SearchResults
                results={searchResults}
                isLoading={isLoading}
                error={error}
                searchTerm={searchTerm}
                totalResults={totalResults}
                onSongPlay={handleSongPlay}
                onClose={handleCloseResults}
                isVisible={showResults}
            />
        </>
    );
}