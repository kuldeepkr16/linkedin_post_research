"""
Configuration module for LinkedIn Post Generator
No paid API keys required - uses free/open-source alternatives
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =============================================================================
# API CONFIGURATION (All FREE options)
# =============================================================================

# Option 1: Groq (FREE - get key from https://console.groq.com/keys)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Option 2: Ollama (FREE - local, no key needed)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Option 3: Google Gemini (FREE tier - get key from https://aistudio.google.com/apikey)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Which provider to use: "groq", "ollama", "gemini", or "template"
AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")

# Groq model (free tier supports these)
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# =============================================================================
# DATA ENGINEERING TOPICS
# =============================================================================

# Keywords for filtering news
NEWS_KEYWORDS = [
    "data engineering",
    "SQL database",
    "PostgreSQL",
    "Apache Spark",
    "Python data",
    "ETL pipeline",
    "data warehouse",
    "dbt data",
    "Snowflake data",
    "Databricks",
    "Apache Kafka",
    "data lakehouse",
    "BigQuery",
    "Redshift",
    "Apache Airflow",
    "data pipeline",
    "QuickSight",
]

# Topics for concept posts
CONCEPT_TOPICS = {
    "sql": {
        "name": "SQL",
        "advanced_concepts": [
            "Window Functions (ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD)",
            "Common Table Expressions (CTEs) and Recursive CTEs",
            "Query Optimization and Execution Plans",
            "Indexing Strategies (B-tree, Hash, GIN, GiST)",
            "Partitioning and Sharding",
            "Transaction Isolation Levels",
            "Materialized Views vs Regular Views",
            "JSON/JSONB Operations in SQL",
            "Pivot and Unpivot Operations",
            "Advanced Joins (LATERAL, CROSS APPLY)",
            "Stored Procedures vs Functions",
            "Database Locking Mechanisms",
            "Query Performance Tuning",
            "Subqueries vs JOINs Performance",
            "NULL Handling and COALESCE",
        ]
    },
    "python": {
        "name": "Python",
        "advanced_concepts": [
            "Generators and Iterators for Memory Efficiency",
            "Context Managers and the 'with' Statement",
            "Decorators and Metaclasses",
            "async/await and Asyncio",
            "Memory Management and Garbage Collection",
            "pandas Performance Optimization",
            "Polars vs Pandas Comparison",
            "Type Hints and Static Analysis",
            "Multiprocessing vs Threading",
            "List Comprehensions vs Generator Expressions",
            "functools (lru_cache, partial, reduce)",
            "collections Module (defaultdict, Counter, deque)",
            "Data Classes and Named Tuples",
            "Property Decorators and Descriptors",
            "Python Profiling and Optimization",
        ]
    },
    "postgres": {
        "name": "PostgreSQL",
        "advanced_concepts": [
            "VACUUM and ANALYZE Operations",
            "WAL (Write-Ahead Logging) Configuration",
            "Connection Pooling with PgBouncer",
            "Logical vs Physical Replication",
            "EXPLAIN ANALYZE Deep Dive",
            "pg_stat Monitoring Views",
            "Table Partitioning Strategies",
            "Full-Text Search Capabilities",
            "PostgreSQL Extensions (PostGIS, pg_trgm)",
            "Row-Level Security Policies",
            "Foreign Data Wrappers",
            "TOAST (The Oversized-Attribute Storage Technique)",
            "pg_dump and pg_restore Best Practices",
            "Index-Only Scans Optimization",
            "Parallel Query Execution",
        ]
    },
    "spark": {
        "name": "Apache Spark",
        "advanced_concepts": [
            "Catalyst Optimizer and Tungsten Engine",
            "Partitioning and Bucketing Strategies",
            "Broadcast Joins vs Shuffle Joins",
            "Spark Memory Management",
            "Data Skew Handling Techniques",
            "Spark SQL vs DataFrame API",
            "Structured Streaming Concepts",
            "Delta Lake and ACID Transactions",
            "Spark Caching and Persistence Levels",
            "UDFs vs Built-in Functions Performance",
            "Adaptive Query Execution (AQE)",
            "Dynamic Partition Pruning",
            "Spark on Kubernetes",
            "Z-Ordering and Data Skipping",
            "Spark Connect Architecture",
        ]
    },
    "quicksight": {
        "name": "AWS QuickSight",
        "advanced_concepts": [
            "SPICE Engine and Data Refresh",
            "Calculated Fields and Parameters",
            "Level-Aware Aggregations (LAA)",
            "Row-Level Security Implementation",
            "Embedding QuickSight Dashboards",
            "Custom Visual Types",
            "Threshold Alerts and Anomaly Detection",
            "ML Insights and Forecasting",
            "Data Source Joins and Blending",
            "Performance Optimization Techniques",
            "Q (Natural Language Queries)",
            "Themes and Custom Branding",
            "API Automation with SDK",
            "VPC Connectivity and Security",
            "Dashboard Versioning and Publishing",
        ]
    },
    "data_engineering": {
        "name": "Data Engineering",
        "advanced_concepts": [
            "Medallion Architecture (Bronze/Silver/Gold)",
            "Data Quality Frameworks",
            "Schema Evolution Strategies",
            "CDC (Change Data Capture) Patterns",
            "Idempotent Pipeline Design",
            "Data Lineage and Cataloging",
            "Slowly Changing Dimensions (SCD Types)",
            "Data Mesh vs Data Lake",
            "Feature Store Architecture",
            "Stream Processing vs Batch Processing",
            "Data Contracts and API Design",
            "Cost Optimization in Cloud Data",
            "Data Governance Best Practices",
            "Real-time Analytics Architecture",
            "DataOps and CI/CD for Data",
        ]
    }
}

# =============================================================================
# POST STYLE CONFIGURATION
# =============================================================================

POST_STYLE = """
Your writing style for LinkedIn posts should be:
- Write in a natural, conversational tone like you're talking to a colleague
- Keep it simple and straightforward - no corporate jargon
- Use short paragraphs with line breaks after each sentence
- Add a new line after periods and commas for readability
- NEVER use emojis or emoticons - keep it clean and professional
- Start with a relatable hook or interesting observation
- Share practical insights from real experience
- Include 2-3 key takeaways as bullet points
- End with a simple question to encourage discussion
- Keep posts between 150-250 words
- Include 3-4 relevant hashtags at the end (no emojis in hashtags)
- Sound like a human sharing knowledge, not a marketing post
"""

# =============================================================================
# FREE NEWS SOURCES (RSS Feeds - No API Key Required)
# =============================================================================

# Google News RSS feeds for data engineering topics
RSS_FEEDS = [
    # Data Engineering
    "https://news.google.com/rss/search?q=data+engineering+when:1d&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=SQL+database+news+when:1d&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=Apache+Spark+when:1d&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=PostgreSQL+when:1d&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=data+pipeline+analytics+when:1d&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=ETL+data+warehouse+when:1d&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=Databricks+Snowflake+when:1d&hl=en-US&gl=US&ceid=US:en",
]

# Reddit RSS feeds (no API needed)
TECH_RSS_FEEDS = [
    "https://www.reddit.com/r/dataengineering/.rss",
    "https://www.reddit.com/r/SQL/.rss",
    "https://www.reddit.com/r/Python/.rss?limit=10",
    "https://www.reddit.com/r/Database/.rss",
]

# Hacker News RSS (data/tech focused)
HACKERNEWS_FEEDS = [
    "https://hnrss.org/newest?q=data+engineering",
    "https://hnrss.org/newest?q=PostgreSQL",
    "https://hnrss.org/newest?q=SQL",
]

# =============================================================================
# OUTPUT SETTINGS
# =============================================================================

OUTPUT_DIR = "output"
POSTS_PER_RUN = 2
CONCEPT_POSTS_PER_RUN = 2

# =============================================================================
# DIGEST CONFIGURATION
# =============================================================================

DIGEST_LIMIT = 10

DIGEST_STYLE = """
You are an objective news summarizer.
Summarize the key points of the article in 2-3 concise sentences.
Do NOT use phrases like "I came across" or "Here's why it matters".
Do NOT use hashtags.
Focus purely on the facts and technical details.
"""
