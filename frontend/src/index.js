import React from 'react';
import ReactDOM from 'react-dom/client';
import ArticleList from './components/ArticleList';

// Temporary mock data for testing
const mockArticles = [
  {
    id: 1,
    title: "Sample Article",
    category: "Technology",
    summary: "This is a sample article summary for testing the interface.",
    url: "https://example.com"
  }
];

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px' }}>
      <h1>Personalized News Summarizer</h1>
      <ArticleList 
        articles={mockArticles} 
        onDelete={(id) => console.log('Delete article:', id)} 
      />
    </div>
  </React.StrictMode>
);
