import axios from 'axios';
import { submitArticle, getArticles, getArticlesByCategory, deleteArticle } from '../articleService';

jest.mock('axios');

describe('articleService', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('submitArticle', () => {
    it('submits article successfully', async () => {
      const mockResponse = { data: { id: 1, title: 'Test Article' } };
      axios.post.mockResolvedValueOnce(mockResponse);

      const result = await submitArticle('https://example.com');
      expect(result).toEqual(mockResponse.data);
    });

    it('handles submission error', async () => {
      axios.post.mockRejectedValueOnce({ response: { data: { detail: 'Invalid URL' } } });

      await expect(submitArticle('invalid-url')).rejects.toThrow('Invalid URL');
    });
  });

  describe('getArticles', () => {
    it('fetches articles successfully', async () => {
      const mockArticles = [{ id: 1, title: 'Article 1' }];
      axios.get.mockResolvedValueOnce({ data: mockArticles });

      const result = await getArticles();
      expect(result).toEqual(mockArticles);
    });

    it('handles fetch error', async () => {
      axios.get.mockRejectedValueOnce({ response: { data: { detail: 'Failed to fetch' } } });

      await expect(getArticles()).rejects.toThrow('Failed to fetch');
    });
  });

  // Add more test cases for other service functions
});
