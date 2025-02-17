"""
Helper Functions for Article Summarization Service.

This module provides utility functions for article scraping and AI-powered
summarization using Azure OpenAI services.
"""

import json
import re
from newspaper import Article as NewspaperArticle
from backend.app.logs.summarizer_logging import logger
from backend.app.core.summarizer_config import settings
from openai import AzureOpenAI


def scrape_article(url: str) -> dict:
    """
    Scrape article content from a given URL.

    Args:
        url (str): URL of the article to scrape

    Returns:
        dict: Contains 'title' and 'text' of the article

    Raises:
        Exception: If article scraping fails
    """
    try:
        article = NewspaperArticle(url)
        article.download()
        article.parse()
        logger.info(f"Article scraped successfully: {url}")
        logger.info(f"Title: {article.title}")
        return {"title": article.title, "text": article.text}
    except Exception as e:
        logger.error(f"Failed to fetch article from {url}: {e}")
        raise Exception("Failed to fetch article")


def generate_summary_classify_article(content: str) -> dict:
    """
    Generate a summary and classify an article using Azure OpenAI.

    Args:
        content (str): Article content to summarize and classify

    Returns:
        dict: Contains 'summary' and 'category' of the article

    Raises:
        json.JSONDecodeError: If API response parsing fails
        ValueError: If response structure is invalid
        Exception: For other failures
    """
    try:
        client = AzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_version=settings.AZURE_OPENAI_API_VERSION,
        )
        prompt = """
        Analyze the following article and provide ONLY a JSON response with a summary and category(e.g., Technology, Sports, Business, Entertainment, Health, or General).
        The response must be valid JSON with no additional text before or after.

        Article:
        {}

        Response format:
        {{
          "summary": "Brief summary of the news article",
          "category": "Relevant category"
        }}
        """.format(
            content
        )

        response = client.chat.completions.create(
            model=settings.AZURE_OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        # Clean and extract response text
        response_text = response.choices[0].message.content.strip()
        logger.debug(f"Raw response: {response_text}")

        # Try to find JSON in the response
        json_match = re.search(r"(\{[\s\S]*\})", response_text)
        if not json_match:
            raise json.JSONDecodeError(
                "No JSON object found in response", response_text, 0
            )

        clean_json = json_match.group(1)
        data = json.loads(clean_json)

        # Validate response structure
        if not isinstance(data, dict) or not all(
            k in data for k in ["summary", "category"]
        ):
            raise ValueError("Invalid response structure")

        logger.info("Article summary and classification generated successfully")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error. Raw response: {response_text}")
        logger.error(f"JSON error details: {str(e)}")
        raise Exception("Failed to parse summary and category")
    except Exception as e:
        logger.error(f"Failed to generate summary and classify article: {str(e)}")
        raise
