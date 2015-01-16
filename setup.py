"""Setup for forum_leaderboard XBlock."""

import os
from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='xblock-leaderboard',
    version='0.2',
    description='An XBlock which lists the top threads of an inline discussion.',
    packages=[
        'forum_leaderboard',
    ],
    install_requires=[
        'XBlock',
        'xblock-utils',
        'ddt',
    ],
    dependency_links=['https://github.com/edx-solutions/xblock-utils/archive/master.tar.gz'],
    entry_points={
        'xblock.v1': [
            'forum_leaderboard = forum_leaderboard:ForumLeaderboardXBlock',
        ]
    },
    package_data=package_data("forum_leaderboard", ["static", "public"]),
)
