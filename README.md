# Shipping-Data-Product

An end-to-end data pipeline that extracts, transforms, and exposes Telegram data about Ethiopian medical and cosmetic products. The project leverages Telethon, dbt, YOLOv8, and FastAPI to turn raw Telegram messages into actionable insights.

## Project Overview

This project builds a data product providing analytical insights into Ethiopian medical and cosmetic businesses by scraping public Telegram channels.

### Business Questions Addressed

- What are the top 10 most frequently mentioned medical products across all channels?
- How does the price or availability of a specific product vary across channels?
- Which channels have the most visual content (images of pills, creams, etc.)?
- What are the daily and weekly trends in posting volume for health-related topics?

## Features

- Telegram Scraper: Extract messages, images, views, and forwards using Telethon.
- Data Storage: Raw JSON data stored in a structured Data Lake.
- Data Modeling: Transform raw data into a dimensional star schema using dbt.
- Data Enrichment: Detect objects in images using YOLOv8 and categorize visual content.
- Analytical API: Expose insights through FastAPI endpoints.
- Pipeline Orchestration: Automate tasks using Dagster.

## Project Structure

medical-telegram-warehouse/
├── src/                 # Python scripts for scraping and processing
├── api/                 # FastAPI application
├── data/
│   ├── raw/             # Raw JSON and images
├── logs/                # Scraper and pipeline logs
├── medical_warehouse/   # dbt project
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL
- Telegram API credentials (API ID and API HASH)

### Install Dependencies

```bash
pip install -r requirements.txt
