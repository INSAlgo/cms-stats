"""
cms-stats provides an API to retrieve and fetch
data exported from a CMS database, using psycopg2 and matplotlib

Base test, considering a CMS database running on localhost:5432,
and a contest with 6 distincts problems
"""

from cms_stats import CMSAnalyze

analyze = CMSAnalyze(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres"
)

# Exports the first perfect solution to problem 3 written in Haskell
analyze.export_program(
    analyze.get_loid_from_sub(
        analyze.get_first_perfect_sub(problem=3, language='Haskell / ghc')[0]
    )  # , to_stdout=True
)

for pb in range(1, 6+1):
    # Displays avg score by language for each problem
    analyze.fetch_avg_score_by_lang(pb)

    # Display hour of first submission for each problem
    sub = analyze.get_first_perfect_sub(pb)
    if sub:
        print(
            f"Première soumission parfaite pour le problème {pb} à "
            f"{sub[3].hour + 2}:{sub[3].minute}:{sub[3].minute} en {sub[2]}"
        )

    # Displays the evolutions of perfect submissions over time for this problem
    analyze.fetch_resolutions_by_problem(pb)
