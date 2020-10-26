"""
cms-stats provides an API to retrieve and fetch
data exported from a CMS database, using psycopg2 and matplotlib

PostgreSQL queries used in analyzer

Copyright 2020, Louis Gombert
Licensed under AGPL-3.0 license
"""

REQ_GET_OBJECT = "SELECT lo_get(( " \
                 "SELECT loid " \
                 "FROM fsobjects " \
                 "INNER JOIN files f on fsobjects.digest = f.digest " \
                 "INNER JOIN submissions s on s.id = f.submission_id " \
                 "WHERE s.id = 162));"

REQ_LOID_EX_SCORE = "SELECT loid, score FROM fsobjects " \
                    "INNER JOIN files ON fsobjects.digest=files.digest " \
                    "INNER JOIN submissions s on s.id = files.submission_id " \
                    "INNER JOIN submission_results sr on s.id = sr.submission_id " \
                    "WHERE sr.dataset_id={problem} " \
                    "AND sr.score >= {score} " \
                    "ORDER BY score DESC, loid;"

REQ_SCOREBOARD = "SELECT p.first_name, p.last_name, sum(p.score) score_tot FROM ( " \
                 "SELECT DISTINCT dataset_id, first_name, last_name, max(score) as score " \
                 "FROM submission_results " \
                 "INNER JOIN submissions s on s.id = submission_results.submission_id " \
                 "INNER JOIN participations p on p.id = s.participation_id " \
                 "INNER JOIN users u on u.id = p.user_id " \
                 "WHERE dataset_id != 5 " \
                 "GROUP BY dataset_id, first_name, last_name " \
                 "ORDER BY dataset_id, max(score) DESC) AS p " \
                 "GROUP BY first_name, last_name " \
                 "ORDER BY score_tot desc;"

REQ_SUBMISSIONS = "SELECT timestamp, dataset_id, language " \
                  "FROM submissions " \
                  "INNER JOIN submission_results sr ON submissions.id = sr.submission_id " \
                  "ORDER BY timestamp;"

REQ_LANGUAGES = "SELECT DISTINCT language " \
                "FROM submissions;"

REQ_LANGUAGES_OCCURENCES = "SELECT DISTINCT language, count(*) as nb_sub " \
                           "FROM submissions " \
                           "GROUP BY language " \
                           "ORDER BY nb_sub DESC;"

REQ_AVG_SCORE_BY_LANG = "SELECT p.dataset_id, avg(p.score) as avg_score, p.language " \
                        "FROM ( " \
                        "SELECT DISTINCT dataset_id, first_name, last_name, language," \
                        "max(score) as score " \
                        "FROM submission_results " \
                        "INNER JOIN submissions s on s.id = submission_results.submission_id " \
                        "INNER JOIN participations p on p.id = s.participation_id " \
                        "INNER JOIN users u on u.id = p.user_id " \
                        "WHERE dataset_id != 5 " \
                        "GROUP BY dataset_id, first_name, last_name, language " \
                        "ORDER BY dataset_id DESC, max(score) DESC) as p " \
                        "GROUP BY language, dataset_id " \
                        "ORDER BY dataset_id, language;"

REQ_FIRST_SUBMISSION_LANG_EX = "SELECT dataset_id, timestamp, language " \
                               "FROM submission_results " \
                               "INNER JOIN submissions s" \
                               "ON s.id = submission_results.submission_id " \
                               "WHERE score = 100 " \
                               "AND dataset_id = {problem} " \
                               "AND language = {language}" \
                               "LIMIT 1;"

REQ_FIRST_SUBS = "SELECT id, timestamp, language, dataset_id FROM submissions " \
                 "INNER JOIN submission_results sr on submissions.id = sr.submission_id " \
                 "WHERE timestamp IN ( " \
                 "SELECT min(timestamp) " \
                 "FROM submission_results " \
                 "INNER JOIN submissions s on s.id = submission_results.submission_id " \
                 "WHERE score = 100 " \
                 "GROUP BY dataset_id, language " \
                 "ORDER BY min(s.timestamp));"
