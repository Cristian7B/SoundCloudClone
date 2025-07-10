import React, { useState } from 'react';
import styles from '../Styles/AudioCard.module.css';
import playIcon from '../assets/play.svg';
import pauseIcon from '../assets/pause.svg';
import likeIcon from '../assets/like.svg';
import repostIcon from '../assets/repost.svg';
import copyIcon from '../assets/copy.svg';
import sendIcon from '../assets/send.svg';

export function AudioCard({
  userAvatar,
  userName,
  trackTitle,
  albumCover,
  timeAgo,
  likes,
  reposts,
  plays,
  comments,
  tags = [],
  isPlaying = false,
  onPlayPause,
  onLike,
  onRepost,
  onCopy,
}) {
  const [isLiked, setIsLiked] = useState(false);
  const [isReposted, setIsReposted] = useState(false);
  const [commentText, setCommentText] = useState('');

  const handleLike = () => {
    setIsLiked(!isLiked);
    onLike && onLike();
  };

  const handleRepost = () => {
    setIsReposted(!isReposted);
    onRepost && onRepost();
  };

  const handleCommentSubmit = (e) => {
    e.preventDefault();
    if (commentText.trim()) {
      setCommentText('');
    }
  };

  return (
    <div className={styles.audioCard}>
      {/* Header */}
      <div className={styles.header}>
        <img 
          src={userAvatar} 
          alt={`${userName} avatar`} 
          className={styles.userAvatar} 
        />
        <div className={styles.userInfo}>
          <span className={styles.userName}>{userName}</span>
          <span className={styles.timeAgo}>posteó una pista hace {timeAgo}</span>
        </div>
        {tags.length > 0 && (
          <div className={styles.tags}>
            {tags.map((tag, index) => (
              <span key={index} className={styles.tag}>
                #{tag}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Main Content */}
      <div className={styles.mainContent}>
        <div className={styles.albumCover}>
          <img src={albumCover} alt={trackTitle} />
        </div>
        
        <div className={styles.trackInfo}>
          <div className={styles.playSection}>
            <button 
              className={styles.playButton}
              onClick={onPlayPause}
            >
              <img 
                src={isPlaying ? pauseIcon : playIcon} 
                alt={isPlaying ? 'Pause' : 'Play'} 
              />
            </button>
            <div className={styles.trackDetails}>
              <h3 className={styles.artistName}>{userName}</h3>
              <h4 className={styles.trackTitle}>{trackTitle}</h4>
            </div>
          </div>
          
          {/* Placeholder para la onda de audio */}
          <div className={styles.waveformPlaceholder}>
            <div className={styles.waveformBars}>
              {Array.from({ length: 100 }).map((_, index) => (
                <div 
                  key={index} 
                  className={styles.waveformBar}
                  style={{
                    height: `${Math.random() * 40 + 10}px`,
                    backgroundColor: index < 30 ? '#ff5500' : '#555555'
                  }}
                />
              ))}
            </div>
            <div className={styles.timeStamps}>
              <span>0:00</span>
              <span>3:45</span>
            </div>
          </div>
        </div>
      </div>

      {/* Comment Section */}
      <div className={styles.commentSection}>
        <img 
          src={userAvatar} 
          alt="Your avatar" 
          className={styles.commentAvatar} 
        />
        <form onSubmit={handleCommentSubmit} className={styles.commentForm}>
          <input
            type="text"
            placeholder="Escribe un comentario"
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
            className={styles.commentInput}
          />
          <button type="submit" className={styles.sendButton}>
            <img src={sendIcon} alt="Send" />
          </button>
        </form>
      </div>

      {/* Actions */}
      <div className={styles.actions}>
        <button 
          className={`${styles.actionButton} ${isLiked ? styles.liked : ''}`}
          onClick={handleLike}
        >
          <img src={likeIcon} alt="Like" />
          <span>{likes}</span>
        </button>
        
        <button 
          className={`${styles.actionButton} ${isReposted ? styles.reposted : ''}`}
          onClick={handleRepost}
        >
          <img src={repostIcon} alt="Repost" />
          <span>{reposts}</span>
        </button>
        
        <button className={styles.actionButton} onClick={onCopy}>
          <img src={copyIcon} alt="Copy link" />
        </button>
        
        <div className={styles.stats}>
          <span className={styles.plays}>
            <span className={styles.playIcon}>▶</span>
            {plays}
          </span>
          <span className={styles.comments}>
            <span className={styles.commentIcon}>💬</span>
            {comments}
          </span>
        </div>
      </div>
    </div>
  );
}