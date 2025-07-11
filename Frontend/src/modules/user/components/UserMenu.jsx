import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import UserProfile from './UserProfile';
import AuthModal from './AuthModal';
import { useAuthModal } from '../hooks/useAuthModal';
import styles from '../Styles/UserMenu.module.css';

const UserMenu = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const {
    isAuthModalOpen,
    authMode,
    openLoginModal,
    openRegisterModal,
    closeAuthModal,
  } = useAuthModal();

  const handleLogout = async () => {
    try {
      await logout();
      setShowDropdown(false);
    } catch (error) {
      console.error('Error during logout:', error);
    }
  };

  const handleProfileClick = () => {
    setShowProfile(true);
    setShowDropdown(false);
  };

  if (showProfile) {
    return (
      <UserProfile onClose={() => setShowProfile(false)} />
    );
  }

  if (!isAuthenticated) {
    return (
      <>
        <div className={styles.authButtons}>
          <p 
            onClick={openLoginModal}
            className={styles.loginButton}
          >
            Iniciar sesión
          </p>
        </div>
        
        <AuthModal
          isOpen={isAuthModalOpen}
          onClose={closeAuthModal}
          initialMode={authMode}
        />
      </>
    );
  }

  return (
    <div className={styles.userMenuContainer}>
      <div className={styles.userInfo}>
        <div 
          className={styles.userAvatar}
          onClick={() => setShowDropdown(!showDropdown)}
        >
          {user?.first_name?.[0]?.toUpperCase() || 'U'}
        </div>
        
        {showDropdown && (
          <div className={styles.dropdown}>
            <div className={styles.dropdownHeader}>
              <div className={styles.userDetails}>
                <span className={styles.userName}>
                  {user?.first_name} {user?.last_name}
                </span>
                <span className={styles.userEmail}>@{user?.username}</span>
              </div>
            </div>
            
            <div className={styles.dropdownMenu}>
              <button 
                onClick={handleProfileClick}
                className={styles.menuItem}
              >
                Ver perfil
              </button>
              <button 
                onClick={() => console.log('Configuración')}
                className={styles.menuItem}
              >
                Configuración
              </button>
              <div className={styles.divider}></div>
              <button 
                onClick={handleLogout}
                className={`${styles.menuItem} ${styles.logoutItem}`}
              >
                Cerrar sesión
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UserMenu;
