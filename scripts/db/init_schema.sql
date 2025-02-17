-- SQL script to initialize the schema and tables in the summaries and test_summaries databases

-- Connect to the PostgreSQL server as myuser
\c - myuser

-- Enable the dblink extension
CREATE EXTENSION IF NOT EXISTS dblink;

-- Check if the summaries database exists before creating it
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'summaries') THEN
        PERFORM dblink_exec('dbname=postgres user=myuser', 'CREATE DATABASE summaries');
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'test_summaries') THEN
        PERFORM dblink_exec('dbname=postgres user=myuser', 'CREATE DATABASE test_summaries');
    END IF;
END $$;

-- Connect to the summaries database
\connect summaries

-- Create the summary schema if it does not exist
CREATE SCHEMA IF NOT EXISTS summary;

-- Create the articles table in the summary schema if it does not exist
CREATE TABLE IF NOT EXISTS summary.articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    url VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT NOT NULL,
    category VARCHAR(255) NOT NULL
);

-- Connect to the test_summaries database
\connect test_summaries

-- Create the test_summary schema if it does not exist
CREATE SCHEMA IF NOT EXISTS test_summary;

-- Create the test_articles table in the test_summary schema if it does not exist
CREATE TABLE IF NOT EXISTS test_summary.test_articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    url VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT NOT NULL,
    category VARCHAR(255) NOT NULL
);