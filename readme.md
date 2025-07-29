# 🔄 Text-to-SQL Converter

> A powerful proof-of-concept that converts natural language questions into executable SQL queries using AI

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)](https://openai.com)
[![Vanna.AI](https://img.shields.io/badge/Vanna.AI-Powered-orange.svg)](https://vanna.ai)
[![SQLite](https://img.shields.io/badge/SQLite-Local%20DB-lightgrey.svg)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Table of Contents

- [🔄 Text-to-SQL Converter](#-text-to-sql-converter)
  - [📋 Table of Contents](#-table-of-contents)
  - [✨ Overview](#-overview)
  - [🎯 Features](#-features)
  - [🏗️ Architecture](#️-architecture)
  - [📦 Prerequisites](#-prerequisites)
  - [🚀 Quick Start](#-quick-start)
  - [💾 Database Schema](#-database-schema)
  - [🔍 Example Queries](#-example-queries)
  - [🌐 Optional Web Interface](#-optional-web-interface)
  - [🔧 Troubleshooting](#-troubleshooting)
  - [📝 Notes](#-notes)
  - [🤝 Contributing](#-contributing)

## ✨ Overview

This proof-of-concept demonstrates an intelligent module that converts natural language questions into executable SQL queries. Built with **Vanna.AI**, **OpenAI's GPT-4o-mini**, and **SQLite**, it provides a seamless bridge between human language and database queries.

### 🎯 Key Capabilities

- **Natural Language Processing**: Transform English questions into SQL
- **Error Recovery**: Intelligent retry logic with query refinement
- **Local Execution**: No external dependencies for vector storage
- **Time-Sensitive Queries**: Handles date-based queries with rolling windows

## 🎯 Features

| Feature | Description |
|---------|-------------|
| 🧠 **AI-Powered** | Uses OpenAI's GPT-4o-mini via Vanna.AI for intelligent query generation |
| 🗄️ **SQLite Integration** | Lightweight, file-based database with mock e-commerce data |
| 🔄 **Smart Error Handling** | Automatic query refinement with up to 3 retry attempts |
| 📊 **Local Vector Storage** | ChromaDB for local embeddings (no external API required) |
| 🌐 **Web Interface** | Optional Flask-based UI for interactive testing |
| ⏰ **Time-Aware** | Intelligent handling of date ranges and temporal queries |

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│  Natural Language │    │   Vanna.AI   │    │   SQLite DB     │
│    Questions      │───▶│   + OpenAI   │───▶│  (ecommerce.db) │
└─────────────────┘    └──────────────┘    └─────────────────┘
                              │                       │
                              ▼                       ▼
                       ┌──────────────┐    ┌─────────────────┐
                       │  ChromaDB    │    │   SQL Results   │
                       │ (Vector Store)│    │   + Metadata    │
                       └──────────────┘    └─────────────────┘
```

## 📦 Prerequisites

- **Python**: Version 3.9 or higher
- **OpenAI API Key**: [Get one here](https://platform.openai.com/api-keys)
- **System**: macOS, Linux, or Windows with Python support

## 🚀 Quick Start

### 1️⃣ Clone and Setup Environment

```bash
# Navigate to your project directory
cd "/Users/rohit/Desktop/text to SQL"

# Create and activate virtual environment
python3 -m venv text-to-sql-env
source text-to-sql-env/bin/activate  # On Windows: text-to-sql-env\Scripts\activate
```

### 2️⃣ Install Dependencies

```bash
pip install vanna openai chromadb flask
```

### 3️⃣ Set Environment Variables

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your_openai_api_key_here"

# Disable tokenizers parallelism (prevents warnings)
export TOKENIZERS_PARALLELISM=false

# Verify setup
echo $OPENAI_API_KEY
```

### 4️⃣ Initialize Database

Run the database setup script:

```bash
python setup_database.py
```

This creates `ecommerce.db` with sample data.

### 5️⃣ Run the Text-to-SQL Converter

```bash
python text_to_sql_local.py
```

## 💾 Database Schema

### 📊 Tables Overview

#### `orders` Table
| Column | Type | Description |
|--------|------|-------------|
| `order_id` | TEXT (PK) | Unique order identifier |
| `user_id` | TEXT | Foreign key to users table |
| `product_id` | TEXT | Product identifier |
| `city` | TEXT | City where order was placed |
| `order_date` | DATETIME | Order timestamp |
| `quantity` | INTEGER | Number of items ordered |

#### `users` Table
| Column | Type | Description |
|--------|------|-------------|
| `user_id` | TEXT (PK) | Unique user identifier |
| `username` | TEXT | User's display name |

### 📈 Sample Data

- **5 orders** spanning July 20-25, 2025
- **4 orders** in Bangalore, **1 order** in Mumbai
- **2 users**: Alice (4 orders), Bob (1 order)

## 🔍 Example Queries

### Query 1: Top Products by City and Time Range
```
❓ Question: "Show the top 10 products sold in Bangalore in the last 7 days."

🔍 Generated SQL:
SELECT product_id, SUM(quantity) AS total_quantity
FROM orders
WHERE city = 'Bangalore' AND order_date >= datetime('now', '-7 days')
GROUP BY product_id
ORDER BY total_quantity DESC
LIMIT 10;

📊 Expected Results:
[
  ('123e4567-e89b-12d3-a456-426614174003', 4),
  ('123e4567-e89b-12d3-a456-426614174000', 2),
  ('123e4567-e89b-12d3-a456-426614174004', 1),
  ('123e4567-e89b-12d3-a456-426614174001', 1)
]
```

### Query 2: User Purchase Patterns
```
❓ Question: "List users who made more than 3 purchases in a month."

🔍 Generated SQL:
SELECT u.user_id, u.username
FROM users u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date >= datetime('now', '-30 days')
GROUP BY u.user_id, u.username
HAVING COUNT(o.order_id) > 3;

📊 Expected Results:
[('6ba7b810-9dad-11d1-80b4-00c04fd430c8', 'alice')]
```

## 🌐 Optional Web Interface

Enable the Flask web interface for interactive testing:

1. **Uncomment the Flask code** in `text_to_sql_local.py`:
```python
from vanna.flask import VannaFlaskApp
app = VannaFlaskApp(vanna)
app.run()
```

2. **Install Flask** (if not already installed):
```bash
pip install flask
```

3. **Access the interface**:
```
🌐 Open: http://localhost:8080
```

## 🔧 Troubleshooting

### 🔑 API Key Issues
```bash
# Verify your API key is set
echo $OPENAI_API_KEY

# If empty, export it again
export OPENAI_API_KEY="your_actual_api_key"
```

### 🗄️ Database Issues
```bash
# Check if database file exists
ls -la ecommerce.db

# Verify data
sqlite3 ecommerce.db "SELECT COUNT(*) FROM orders;"
sqlite3 ecommerce.db "SELECT COUNT(*) FROM users;"
```

### 🐛 SQL Generation Issues
If queries fail consistently:

1. **Retrain with specific examples**:
```python
vanna.train(
    question="Your specific question",
    sql="SELECT * FROM table WHERE condition;"
)
```

2. **Check error logs** for specific SQL syntax issues

### ⚡ Rate Limiting
If hitting OpenAI rate limits:
```python
# Increase sleep time in retry logic
time.sleep(2)  # Instead of time.sleep(1)
```

## 📝 Notes

### 📅 Date Alignment
- Mock data spans **July 20-25, 2025**
- Current reference date: **July 29, 2025, 07:23 AM IST**
- 7-day and 30-day rolling windows are properly calibrated

### 🔄 Error Recovery
The system includes intelligent error handling:
```
Attempt 1 → SQL Generation → Execution
    ↓ (if error)
Error Analysis → Query Refinement → Retry
    ↓ (if still error)
Final Attempt → Success or Failure Report
```

### 🚀 Scalability Considerations
- **Development**: SQLite (current)
- **Production**: Consider PostgreSQL, MySQL, or ClickHouse
- **Vector Storage**: ChromaDB (local) → Pinecone/Weaviate (production)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

<div align="center">

**Made with ❤️ using Vanna.AI and OpenAI**

[🔗 Vanna.AI Documentation](https://vanna.ai/) | [🔗 OpenAI API](https://platform.openai.com/) | [🔗 Report Issues](../../issues)

</div>