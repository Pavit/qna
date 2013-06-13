CHANGELOG
6/11/2013

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