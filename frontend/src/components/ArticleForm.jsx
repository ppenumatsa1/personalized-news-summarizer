import React, { useState } from 'react';
import { submitArticle } from '../services/articleService';
import './ArticleForm.css';

const ArticleForm = ({ onArticleSubmitted }) => {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await submitArticle(url);
      setUrl('');
      if (onArticleSubmitted) {
        onArticleSubmitted();
      }
    } catch (err) {
      setError(err.message || 'Failed to submit article');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="article-form">
      <h2>Submit New Article</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter article URL"
          required
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Processing...' : 'Submit'}
        </button>
      </form>
      {error && <div className="error">{error}</div>}
    </div>
  );
};

export default ArticleForm;
