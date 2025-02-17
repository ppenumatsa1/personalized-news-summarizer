from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base  # Updated import

# Define separate Base classes for each database
SummaryBase = declarative_base()
TestSummaryBase = declarative_base()


class Article(SummaryBase):
    __tablename__ = "articles"
    __table_args__ = {"schema": "summary", "extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=True)
    url = Column(String, index=True)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    category = Column(String, nullable=False)


class TestArticle(TestSummaryBase):
    """Test article model for testing purposes"""

    __tablename__ = "test_articles"
    __table_args__ = {"schema": "test_summary", "extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=True)
    url = Column(String, index=True)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    category = Column(String, nullable=False)

    # @classmethod
    # def _sa_class_manager(cls):
    #     # This method is required for pytest to properly collect the class
    #     return cls
