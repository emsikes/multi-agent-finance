"""
Database Service Module

Handles connection to Azure PostgreSQL

Uses SQLAlchemy for table definitions and CRUD operations
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone

from src.shared.config import settings


Base = declarative_base()

# Table schema


class FinancialReport(Base):
    """
    Table and columnd definition for reports_log
    """
    __tablename__ = "reports_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DatabaseService:
    """
    Database Manager 
    """

    def __init__(self):
        # Connect to Azure Postgres
        db_url = settings.azure_postgres_connection_string

        if db_url and db_url.startswith("postgres://"):
            # Ensure current format compatible with SqlAlchemy
            db_url - db_url.replace("postgres://", "postgresql://", 1)

            self.engine = create_engine(db_url)
            self.SessionLocal = sessionmaker(bind=self.engine)

            # Create tables
            Base.metadata.create_all(bind=self.engine)

    def save_report(self, ticker: str, content: str):
        """
        Save the new analysis report to the database
        """
        session = self.SessionLocal()
        try:
            new_report = FinancialReport(ticker=ticker, content=content)
            session.add(new_report)
            session.commit()
            print(
                f"Saved report for {ticker} to Database: (ID: {new_report.id})")
        except Exception as e:
            print(f"Error writing report for {ticker} to database: {e}")
            session.rollback()
        finally:
            session.close()
