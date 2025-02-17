import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import ArticleList from '../ArticleList';

describe('ArticleList', () => {
  const mockArticles = [
    {
      id: 1,
      title: 'Test Article 1',
      summary: 'Test Summary 1',
      category: 'Technology',
      url: 'https://example.com/1',
    },
    {
      id: 2,
      title: 'Test Article 2',
      summary: 'Test Summary 2',
      category: 'Science',
      url: 'https://example.com/2',
    },
  ];

  it('renders no articles message when empty', () => {
    render(<ArticleList articles={[]} onDelete={() => {}} />);
    expect(screen.getByText(/no articles found/i)).toBeInTheDocument();
  });

  it('renders article list correctly', () => {
    render(<ArticleList articles={mockArticles} onDelete={() => {}} />);
    
    expect(screen.getByText('Test Article 1')).toBeInTheDocument();
    expect(screen.getByText('Test Article 2')).toBeInTheDocument();
    expect(screen.getByText('Technology')).toBeInTheDocument();
    expect(screen.getByText('Science')).toBeInTheDocument();
  });

  it('calls onDelete when delete button is clicked', () => {
    const mockDelete = jest.fn();
    render(<ArticleList articles={mockArticles} onDelete={mockDelete} />);

    const deleteButtons = screen.getAllByText('Delete');
    fireEvent.click(deleteButtons[0]);

    expect(mockDelete).toHaveBeenCalledWith(1);
  });

  it('renders article links correctly', () => {
    render(<ArticleList articles={mockArticles} onDelete={() => {}} />);
    
    const links = screen.getAllByText('Read Original');
    expect(links[0]).toHaveAttribute('href', 'https://example.com/1');
    expect(links[1]).toHaveAttribute('href', 'https://example.com/2');
  });
});
