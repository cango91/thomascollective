# The Thomas Collective
## Dynamic Table Demonstration
Hey folks, I added in a new_app (without touching our main_app) to demonstrate the dynamic table (a.k.a. the devilish proposal) and how it would look on our proj.

Please don't pull/merge this branch, it is just for demonstration.
(It also has a `seed_trains.py` which you can use with `python3 seed_trains.py` to seed your database with ~50 trains. This script I can push to our dev branch if y'all would like)

To view the dynamic table in action, git clone this repo (should be no need to `migrate` since you already have the db and migrations done), `python3 manage.py runserver` and navigate to `http://localhost:8000/dynamic` (didn't add a link to our `base.html` on purpose)

Be seeing y'all, take care.
