"""
Contains a dictionary full of scenarios to test for different discussion situations.
"""

leaderboard_scenarios = [
    {
        'page': 'Empty Discussion',
        'ul': ['No threads with a score are available.'],
        'links': [None],
    },
    {
        'page': 'Many Threads',
        'ul': [
            '29 by user29 (Score: 29)',
            '28 by user28 (Score: 28)',
            '27 by user27 (Score: 27)',
            '26 by user26 (Score: 26)',
            '25 by user25 (Score: 25)',
            '24 by user24 (Score: 24)',
            '23 by user23 (Score: 23)',
            '22 by user22 (Score: 22)',
            '21 by user21 (Score: 21)',
            '20 by user20 (Score: 20)',
            '19 by user19 (Score: 19)',
        ],
        'links': [
            '/courses/dummy_key/discussion/forum/many_threads/threads/29',
            '/courses/dummy_key/discussion/forum/many_threads/threads/28',
            '/courses/dummy_key/discussion/forum/many_threads/threads/27',
            '/courses/dummy_key/discussion/forum/many_threads/threads/26',
            '/courses/dummy_key/discussion/forum/many_threads/threads/25',
            '/courses/dummy_key/discussion/forum/many_threads/threads/24',
            '/courses/dummy_key/discussion/forum/many_threads/threads/23',
            '/courses/dummy_key/discussion/forum/many_threads/threads/22',
            '/courses/dummy_key/discussion/forum/many_threads/threads/21',
            '/courses/dummy_key/discussion/forum/many_threads/threads/20',
            '/courses/dummy_key/discussion/forum/many_threads/threads/19',
        ],
    },
    {
        'page': 'Unvoted Threads',
        'ul': ['No threads with a score are available.'],
        'links': [None],
    },
    {
        'page': 'Varied Voting',
        'ul': [
            '9 by user9 (Score: 9)',
            '8 by user8 (Score: 8)',
            '7 by user7 (Score: 7)',
            '6 by user6 (Score: 6)',
        ],
        'links': [
            '/courses/dummy_key/discussion/forum/varied_voting/threads/9',
            '/courses/dummy_key/discussion/forum/varied_voting/threads/8',
            '/courses/dummy_key/discussion/forum/varied_voting/threads/7',
            '/courses/dummy_key/discussion/forum/varied_voting/threads/6',
        ],
    },
]
