import React from 'react';
import { MusicCard } from './MusicCard';
import styles from '../Styles/SearchResults.module.css';

const SearchResults = ({ 
  results, 
  isLoading, 
  error, 
  searchTerm, 
  totalResults,
  onSongPlay,
  onClose,
  isVisible 
}) => {
  if (!isVisible) return null;

  return (
    <div className={styles.searchResultsOverlay} onClick={onClose}>
      <div className={styles.searchResultsContainer} onClick={(e) => e.stopPropagation()}>
        <div className={styles.searchHeader}>
          <h3>Resultados de búsqueda</h3>
          <button className={styles.closeButton} onClick={onClose}>
            ×
          </button>
        </div>

        {searchTerm && (
          <div className={styles.searchInfo}>
            <p>Buscando: <strong>"{searchTerm}"</strong></p>
            {totalResults > 0 && (
              <p className={styles.resultCount}>
                {totalResults} resultado{totalResults !== 1 ? 's' : ''} encontrado{totalResults !== 1 ? 's' : ''}
              </p>
            )}
          </div>
        )}

        <div className={styles.resultsContent}>
          {isLoading && (
            <div className={styles.loadingContainer}>
              <div className={styles.loadingSpinner}></div>
              <p>Buscando canciones...</p>
            </div>
          )}

          {error && (
            <div className={styles.errorContainer}>
              <p className={styles.errorMessage}>
                Error al buscar: {error}
              </p>
            </div>
          )}

          {!isLoading && !error && results.length === 0 && searchTerm && (
            <div className={styles.noResultsContainer}>
              <p className={styles.noResultsMessage}>
                No se encontraron canciones para "{searchTerm}"
              </p>
              <p className={styles.noResultsSubtext}>
                Intenta con otros términos de búsqueda
              </p>
            </div>
          )}

          {!isLoading && !error && results.length > 0 && (
            <div className={styles.resultsGrid}>
              {results.map((song) => (
                <MusicCard
                  key={song.cancion_id}
                  coverImage={song.imagen_url || '/default-cover.jpg'}
                  title={song.titulo}
                  subtitle={`${song.album_titulo || 'Album'} • ${song.genero || 'Sin género'}`}
                  soundcloudUrl={song.archivo_url || `/song/${song.cancion_id}`}
                  onPlay={() => onSongPlay && onSongPlay(song)}
                  className={styles.searchMusicCard}
                />
              ))}
            </div>
          )}
        </div>

        {!isLoading && !error && results.length > 10 && (
          <div className={styles.moreResultsFooter}>
            <p>Mostrando los primeros resultados</p>
            <button className={styles.viewAllButton}>
              Ver todos los resultados
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchResults;
