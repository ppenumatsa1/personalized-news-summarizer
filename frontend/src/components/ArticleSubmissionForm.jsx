import React, { useState } from 'react';
import { submitArticle } from '../services/articleService';

const ArticleSubmissionForm = ({ onArticleSubmitted }) => {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      if (!url.trim()) {
        throw new Error('Please enter a valid URL');
      }

      const article = await submitArticle(url);
      setUrl('');
      onArticleSubmitted(article);
    } catch (error) {
      setError(error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
      <form onSubmit={handleSubmit}>
        <div className="flex flex-col md:flex-row gap-4">
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter article URL"
            className="flex-grow p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isSubmitting}
          />
          <button
            type="submit"
            disabled={isSubmitting}
            className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 transition-colors"
          >
            {isSubmitting ? 'Submitting...' : 'Submit Article'}
          </button>
        </div>
        {error && <p className="text-red-500 mt-3">{error}</p>}
      </form>
    </div>
  );
};

export default ArticleSubmissionForm;
