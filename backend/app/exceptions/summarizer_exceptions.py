class ArticleNotFoundException(Exception):
    def __init__(self, article_id: int):
        self.article_id = article_id
        self.message = f"Article with ID {self.article_id} not found."
        super().__init__(self.message)


class InvalidURLException(Exception):
    def __init__(self, url: str):
        self.url = url
        self.message = f"The provided URL '{self.url}' is invalid."
        super().__init__(self.message)


class SummaryGenerationException(Exception):
    def __init__(self, error_details: str):
        self.error_details = error_details
        self.message = (
            f"An error occurred while generating the summary: {error_details}"
        )
        super().__init__(self.message)


class CategoryNotFoundException(Exception):
    def __init__(self, category_name: str):
        self.category_name = category_name
        self.message = f"Category '{self.category_name}' not found."
        super().__init__(self.message)


class ArticlesNotFoundForCategoryException(Exception):
    def __init__(self, category: str):
        self.category = category
        self.message = f"No articles found for category: {self.category}"
        super().__init__(self.message)
