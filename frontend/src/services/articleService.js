import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

const handleApiError = (error) => {
  if (error.response?.data?.detail?.error === 'ArticlesNotFoundForCategoryException') {
    return error.response.data.detail.message;
  }
  if (error.response?.data?.detail?.msg) {
    return error.response.data.detail.msg;
  }
  if (error.response?.data?.message) {
    return error.response.data.message;
  }
  return 'An unexpected error occurred';
};

export const submitArticle = async (url) => {
  try {
    const response = await api.post('/articles', { url });
    return response.data;
  } catch (error) {
    throw new Error(handleApiError(error));
  }
};

export const getArticles = async () => {
  try {
    const response = await api.get('/articles');
    const articles = response.data;
    // Sort articles by created_at date, latest first
    return articles.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  } catch (error) {
    throw new Error(handleApiError(error));
  }
};

export const getArticlesByCategory = async (category) => {
  try {
    const response = await api.get(`/articles/category/${category.toLowerCase()}`);
    const articles = Array.isArray(response.data) ? response.data : [];
    // Sort articles by created_at date, latest first
    return articles.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  } catch (error) {
    const errorMessage = handleApiError(error);
    if (error.response?.data?.detail?.error === 'ArticlesNotFoundForCategoryException') {
      return []; // Return empty array instead of throwing error for better UI handling
    }
    throw new Error(errorMessage);
  }
};

export const deleteArticle = async (id) => {
  try {
    await api.delete(`/articles/${id}`);
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to delete article');
  }
};
