"""
cms-stats provides an API to retrieve and fetch
data exported from a CMS database, using psycopg2 and matplotlib

Copyright 2020, Louis Gombert
Licensed under AGPL-3.0 license
"""

from cms_stats._analyze import CMSAnalyze
from cms_stats._queries import REQ_GET_OBJECT, \
    REQ_LOID_EX_SCORE, \
    REQ_SCOREBOARD, \
    REQ_SUBMISSIONS, \
    REQ_LANGUAGES, \
    REQ_LANGUAGES_OCCURENCES, \
    REQ_AVG_SCORE_BY_LANG, \
    REQ_FIRST_SUBMISSION_LANG_EX, \
    REQ_FIRST_SUBS
