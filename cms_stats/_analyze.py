"""
cms-stats provides an API to retrieve and fetch
data exported from a CMS database, using psycopg2 and matplotlib

Main class used for connexion, querying and analysis

Copyright 2020, Louis Gombert
Licensed under AGPL-3.0 license
"""

import os
import psycopg2
import matplotlib.pyplot as plt
import matplotlib as mpl

from cms_stats._queries import REQ_LOID_EX_SCORE, \
    REQ_SCOREBOARD, \
    REQ_SUBMISSIONS, \
    REQ_LANGUAGES, \
    REQ_LANGUAGES_OCCURENCES, \
    REQ_FIRST_SUBMISSION_LANG_EX, \
    REQ_GET_OBJECT, REQ_AVG_SCORE_BY_LANG, REQ_SUBMISSIONS_PROBLEM


class CMSAnalyze:
    """
    main class to instantiate to begin analysis
    """

    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

    def get_object(self, loid):
        """
        Retrives an postgres large_object given its loid
        :param loid: id of the object
        :return: the object as a psycopg2 lobject
        """
        return self.conn.lobject(loid)

    def get_loid_from_sub(self, submission_id):
        """
        Retrieves an large_object representing the code given a submission id
        :param submission_id primary key of the submission
        :return the program code object loid
        """
        self.cursor.execute(REQ_GET_OBJECT.format(sub_id=submission_id))
        return self.cursor.fetchone()[0]

    def get_loids_score_pb(self, problem_id, score=0):
        """
        Retrives the loids of the solutions of a given problem
        :param problem_id: unique problem identifier
        :param score: minimum score of the submissions
        :return: list of tuples with the form (id, score)
        """
        self.cursor.execute(REQ_LOID_EX_SCORE.format(problem=problem_id, score=score))
        return self.cursor.fetchall()

    def export_program(self, loid, name="export", folder=".", to_stdout=False):
        """
        Exports a submission program in a file
        :param loid: id of the object to export
        :param name: name given to the file exported
        :param folder: export location
        :param to_stdout: export to stdout instead of file
        """
        obj = self.conn.lobject(loid)

        if to_stdout:
            print(obj.read())
            return

        if not os.path.exists(folder):
            os.makedirs(folder)

        obj.export(os.path.join(folder, name))

    def export_code_pb(self, problem_id, score_min=0):
        """
        Exports the submissions code of a given problem
        :param problem_id: unique problem identifier
        :param score_min: minimum score of the submissions
        """
        for code in self.get_loids_score_pb(problem_id, score_min):
            self.export_program(
                loid=code[0],
                folder=os.path.join(os.getcwd(), f"ex{problem_id}"),
                name=f"score_{code[1]}_id_{code[0]}"
            )

    def get_leaderboard(self):
        """
        Returns the full leaderboard of the contest
        :return: List of tuples like ('firstname', 'lastname', score)
        """
        self.cursor.execute(REQ_SCOREBOARD)
        return self.cursor.fetchall()

    def fetch_leaderboard(self, interval=50, max_score=600):
        """
        displays the current score repartition of the contest as a bar plot
        :param interval
        :param max_score
        """
        leaderboard = self.get_leaderboard()
        categories = [f"{x}-{x + interval}" for x in range(0, max_score, interval)]
        results = [len(list(filter(lambda x, sc=score: sc <= x[2] < sc + interval, leaderboard)))
                   for score in range(0, max_score, interval)]

        _, axis = plt.subplots()
        axis.set_xlabel("Score final")
        axis.set_ylabel("Nombre de participants")
        axis.bar(categories, results)
        axis.legend()

        plt.show()

    def get_submissions(self):
        """
        Returns the full submission list with language and timestamps
        :return: List of tuples like (timestamp, problem, language)
        """
        self.cursor.execute(REQ_SUBMISSIONS)
        return self.cursor.fetchall()

    def fetch_cumulative_submissions(self):
        """
        Displays submissions as a cumulative histogram
        """
        subs = self.get_submissions()
        timestamps = [time[0].timestamp() for time in subs]

        mpl.style.use('seaborn')
        _, axis = plt.subplots()

        plt.xticks([1602687747, 1602690931, 1602695098])
        axis.set_xticklabels(["0h", "1h", "2h"])

        axis.set_title('Cumul des soumissions')
        axis.set_xlabel("Durée du concours")
        axis.set_ylabel("Nombre de soumissions")

        axis.hist(timestamps, cumulative=True, bins=500, color='coral')
        plt.show()

    def get_languages(self):
        """
        Returns all languages used in submissions
        :return: list of languages as a list of strings
        """
        self.cursor.execute(REQ_LANGUAGES)
        return [lang[0] for lang in self.cursor.fetchall()]

    def get_language_occurence(self):
        """
        Return languages and the number of submissions in this language
        :return: list of tuples (language, nb_occurences)
        """
        self.cursor.execute(REQ_LANGUAGES_OCCURENCES)
        return self.cursor.fetchall()

    def fetch_languages(self):
        """
        Displays language usage in submissions as a pie chart
        """
        lang_occ = self.get_language_occurence()
        langs = [lang[0] for lang in lang_occ]
        occs = [lang[1] for lang in lang_occ]

        _, axis = plt.subplots()
        wedges, _, _ = axis.pie(occs,
                                autopct=lambda pct: f"{round(pct,1)}%",
                                labels=langs)
        axis.legend(
            wedges, langs,
            title="Langages",
            loc="center left",
            bbox_to_anchor=(1.2, 0, 0.5, 1)
        )

        plt.show()

    def get_first_perfect_sub(self, problem, language="%"):
        """
        Returns information about the first perfect submission for a specific problem,
        and language if specified
        :param problem: problem unique identifier
        :param language: language as a string
        :return: 1 tuple like (submission_id, problem, language, timestamp)
        """
        self.cursor.execute(REQ_FIRST_SUBMISSION_LANG_EX.format(problem=problem, language=language))
        first = self.cursor.fetchall()
        return first[0] if first else ()    # If the problem hasn't been solved (yet)

    def fetch_avg_score_by_lang(self, problem):
        self.cursor.execute(REQ_AVG_SCORE_BY_LANG.format(problem=problem))

        print(f"Scores moyens pour le problème {problem} : ")
        for lang in self.cursor.fetchall():
            print(f"{lang[1]}: {round(lang[0])}pts")
        print()

    def fetch_resolutions_by_problem(self, problem):
        """
        Displays the evolution of cumulative perfect submissions over time
        """
        self.cursor.execute(REQ_SUBMISSIONS_PROBLEM.format(problem=problem))
        subs = self.cursor.fetchall()

        timestamps = [time[0].timestamp() for time in subs]

        mpl.style.use('seaborn')
        _, axis = plt.subplots()

        plt.xticks([1602687747, 1602690931, 1602695098])
        axis.set_xticklabels(["0h", "1h", "2h"])

        axis.set_title(f'Cumul des résolutions du problème {problem}')
        axis.set_xlabel("Durée du concours")
        axis.set_ylabel("Nombre de résolutions avec un score de 100")

        axis.hist(timestamps, cumulative=True, bins=500, color='coral')
        plt.show()
