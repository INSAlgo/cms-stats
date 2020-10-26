"""
cms-stats provides an API to retrieve and fetch
data exported from a CMS database, using psycopg2 and matplotlib

Base test, considering a CMS database running on localhost:5432
"""

from cms_stats import CMSAnalyze

analyze = CMSAnalyze(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres"
)

analyze.fetch_cumulative_submissions()
