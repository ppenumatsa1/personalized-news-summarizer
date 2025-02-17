import React from 'react';

const CATEGORIES = ['general', 'technology', 'business', 'sports', 'entertainment', 'health'];

const CategoryFilter = ({ selectedCategory, onCategoryChange }) => {
  return (
    <div className="bg-white p-4 rounded-lg shadow mb-4">
      <h2 className="text-xl font-semibold mb-3">Filter by Category</h2>
      <div className="flex flex-wrap gap-2">
        <button 
          onClick={() => onCategoryChange(null)}
          className={`px-4 py-2 rounded-full ${
            selectedCategory === null 
              ? 'bg-blue-500 text-white' 
              : 'bg-gray-100 hover:bg-gray-200'
          }`}
        >
          All
        </button>
        {CATEGORIES.map(category => (
          <button
            key={category}
            onClick={() => onCategoryChange(category)}
            className={`px-4 py-2 rounded-full ${
              selectedCategory === category 
                ? 'bg-blue-500 text-white' 
                : 'bg-gray-100 hover:bg-gray-200'
            }`}
          >
            {category.charAt(0).toUpperCase() + category.slice(1)}
          </button>
        ))}
      </div>
    </div>
  );
};

export default CategoryFilter;
