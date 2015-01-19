# Forum Leaderboard XBlock

This XBlock allows you to display an arbitrary number of top scoring threads in an inline discussion.

# Instructions

Add `forum_leaderboard` to your list of modules in the advanced settings for your course.
In a unit where you want to add the leaderboard, click on the advanced button and select *Forum Leaderboard*
from the dropdown. Click the edit button, and paste in the Discussion ID of an inline discussion somewhere in your
course.

An inline discussion's ID is displayed on its studio preview.

# Notes

Because this XBlock relies on the discussion service, it uses dummy functions in the XBlock SDK for testing.

Links to threads do not go to the unit the inline discussion is in, but to the general course discussion page,
opening up the specific thread. This is because inline discussions do not support opening and focusing on a particular
thread on page load.
