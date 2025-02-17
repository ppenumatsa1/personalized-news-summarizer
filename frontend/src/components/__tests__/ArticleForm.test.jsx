import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ArticleForm from '../ArticleForm';
import { submitArticle } from '../../services/articleService';

jest.mock('../../services/articleService');

describe('ArticleForm', () => {
  const mockOnArticleSubmit = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders the form correctly', () => {
    render(<ArticleForm onArticleSubmit={mockOnArticleSubmit} />);
    expect(screen.getByPlaceholderText(/enter article url/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument();
  });

  it('handles successful submission', async () => {
    const mockArticle = { id: 1, title: 'Test Article' };
    submitArticle.mockResolvedValueOnce(mockArticle);

    render(<ArticleForm onArticleSubmit={mockOnArticleSubmit} />);

    const input = screen.getByPlaceholderText(/enter article url/i);
    const submitButton = screen.getByRole('button', { name: /submit/i });

    fireEvent.change(input, { target: { value: 'https://example.com' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(submitArticle).toHaveBeenCalledWith('https://example.com');
      expect(mockOnArticleSubmit).toHaveBeenCalledWith(mockArticle);
      expect(input.value).toBe('');
    });
  });

  it('displays error message on submission failure', async () => {
    const errorMessage = 'Failed to submit article';
    submitArticle.mockRejectedValueOnce(new Error(errorMessage));

    render(<ArticleForm onArticleSubmit={mockOnArticleSubmit} />);

    const input = screen.getByPlaceholderText(/enter article url/i);
    const submitButton = screen.getByRole('button', { name: /submit/i });

    fireEvent.change(input, { target: { value: 'https://example.com' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });
});
