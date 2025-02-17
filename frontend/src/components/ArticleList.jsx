import React, { useState, useEffect } from 'react';
import ArticleSubmissionForm from './ArticleSubmissionForm';
import CategoryFilter from './CategoryFilter';
import { getArticles, getArticlesByCategory, deleteArticle } from '../services/articleService';
import './ArticleList.css';

const CATEGORIES = ['technology', 'business', 'sports', 'entertainment', 'health'];

const ArticleList = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [expandedArticles, setExpandedArticles] = useState(new Set());

  const fetchArticles = async (category = null) => {
    try {
      setLoading(true);
      setError(null);
      const data = category 
        ? await getArticlesByCategory(category)
        : await getArticles();
      // Sort articles by creation date, latest first
      const sortedData = Array.isArray(data) 
        ? data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        : [];
      setArticles(sortedData);
    } catch (err) {
      setError(err.message);
      setArticles([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchArticles(selectedCategory);
  }, [selectedCategory]);

  const handleDelete = async (id) => {
    try {
      await deleteArticle(id);
      await fetchArticles(selectedCategory);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleArticleSubmitted = (newArticle) => {
    // Add new article at the beginning and maintain sort order
    setArticles(prevArticles => {
      const updatedArticles = [newArticle, ...prevArticles];
      return updatedArticles.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    });
  };

  const toggleSummary = (articleId) => {
    setExpandedArticles(prev => {
      const newSet = new Set(prev);
      if (newSet.has(articleId)) {
        newSet.delete(articleId);
      } else {
        newSet.add(articleId);
      }
      return newSet;
    });
  };

  return (
    <div className="container mx-auto p-4 max-w-6xl">
      <div className="mb-8 border-b pb-6">
        <h1 className="text-2xl font-bold mb-4">Submit New Article</h1>
        <ArticleSubmissionForm onArticleSubmitted={handleArticleSubmitted} />
      </div>

      <div className="mb-8">
        <CategoryFilter 
          selectedCategory={selectedCategory} 
          onCategoryChange={setSelectedCategory}
        />
      </div>

      {loading ? (
        <div className="text-center text-gray-600">Loading articles...</div>
      ) : error ? (
        <div className="text-center text-red-500">{error}</div>
      ) : !articles.length ? (
        <div className="text-center text-gray-600">
          {selectedCategory 
            ? `No articles found for category: ${selectedCategory}`
            : 'No articles found'}
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {articles.map((article) => (
            <div key={article.id} className="article-card p-5">
              <div className="flex flex-col h-full">
                <div className="flex-grow">
                  <h3 className="article-title">
                    {article.title}
                  </h3>
                  <div className="article-category mb-3">
                    {article.category}
                  </div>
                  <div className="article-summary-container">
                    <p className={`article-summary ${expandedArticles.has(article.id) ? 'expanded' : ''}`}>
                      {article.summary}
                    </p>
                    {article.summary.length > 200 && (
                      <button
                        onClick={() => toggleSummary(article.id)}
                        className="text-blue-600 text-sm mt-2 hover:text-blue-700"
                      >
                        {expandedArticles.has(article.id) ? 'Show Less' : 'Show More'}
                      </button>
                    )}
                  </div>
                </div>
                
                <div className="article-actions">
                  <a 
                    href={article.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="read-more-btn"
                  >
                    Read Article
                  </a>
                  <button 
                    onClick={() => handleDelete(article.id)}
                    className="delete-btn group"
                    aria-label="Delete article"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ArticleList;
