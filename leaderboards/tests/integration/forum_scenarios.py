"""
Contains a dictionary full of scenarios to test for different discussion situations.
"""

forum_scenarios = [
    {
        'page': 'Empty Discussion',
        'message': 'There are not yet any discussions with a score.',
        'links': [None],
    },
    {
        'page': 'Many Threads',
        'ol': [
            'Thread 29 by user29 (Score: 29)',
            'Thread 28 by user28 (Score: 28)',
            'Thread 27 by user27 (Score: 27)',
            'Thread 26 by user26 (Score: 26)',
            'Thread 25 by user25 (Score: 25)',
            'Thread 24 by user24 (Score: 24)',
            'Thread 23 by user23 (Score: 23)',
            'Thread 22 by user22 (Score: 22)',
            'Thread 21 by user21 (Score: 21)',
            'Thread 20 by user20 (Score: 20)',
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
        ],
    },
    {
        'page': 'Unvoted Threads',
        'message': 'There are not yet any discussions with a score.',
        'links': [None],
    },
    {
        'page': 'Varied Voting',
        'ol': [
            'Thread 2 by user2 (Score: 8)',
            'Thread 3 by user3 (Score: 6)',
            'Thread 7 by user7 (Score: 6)',
            'Thread 5 by user5 (Score: 5)',
            'Thread 1 by user1 (Score: 4)',
            'Thread 6 by user6 (Score: 4)',
        ],
        'links': [
            '/courses/dummy_key/discussion/forum/varied_voting/threads/2',
            '/courses/dummy_key/discussion/forum/varied_voting/threads/3',
            '/courses/dummy_key/discussion/forum/varied_voting/threads/7',
            '/courses/dummy_key/discussion/forum/varied_voting/threads/5',
            '/courses/dummy_key/discussion/forum/varied_voting/threads/1',
            '/courses/dummy_key/discussion/forum/varied_voting/threads/6',
        ],
    },
]
