CHANGELOG

----------------6/28/2013-------------------------------------------------------
Modified previous questions graph to new layout.

Known bugs:
1. Text doesn't display well at 0% or 100%

2. For answers greater than 30+ characters, space allocation is lacking.


----------------6/23/2013-------------------------------------------------------

Styled Typeahead.js. Replaced Foundation CSS. Also added shit like dropdowns, restyled some things.

Known Bugs:

1. Typeahead dropdown is not on top when the layout is shrunken (i.e. in responsive mobile mode).

2. Signup modal from login dropdown doesn't work.

3. Heading in "Previous Question" box is currently invisible.

----------------6/22/2013-------------------------------------------------------

In the midst of my coke bender I forgot to update the changelog. So here's are the recent changes
made by Cho and I:

1. I found a snippet that allows ajax views rendering individual blocks.  See questions/utils.py.
      - This means that view_question is now obsolete.
      - When a vote is clicked, the current_question.html template is called again, which would
      normally result in double nav bars, but the snippet only re-renders the current_block question
      in the template.
      - One drawback is that the scripts referenced in base don't propragate down into the re-rendered
      block, so I have the jquery script tag in there.
      - This should suffice until the next version of the site.  Django 1.5 has some changes that may
      help us out with this issue.

2. JQueryUI Autocomplete ditched for Typeahead.js.  It still looks like butt^2 so it will
      need to be styled and whatnot.

3. Tooltip for SUBMIT and PROFILE links if you're not logged in.

4. Some javascript moved from base.html into app.js for tidiness.



----------------6/15/2013-------------------------------------------------------

Removed django-social-auth plug-in and manually added facebook login using the javascript sdk.

TO DO:
      -additional permissions
      -further testing



----------------6/11/2013-------------------------------------------------------

Added some model properties to make pulling info faster and cleaner.

=============================

For questions..

q.registered_vote_count
q.anonymous_vote_count
q.total_vote_count

=============================

For answers...

a.registered_vote_count
a.anonymous_vote_count

No changes for getting total votes of an answer:
a.votes.count() [no property added for total votes since Vote is child model]

=============================

For userprofile objects..

u.total_votes [tally the grand total of votes for a user's submissions]

*************************************
