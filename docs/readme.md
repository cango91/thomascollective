# NOTICE! IMPORTANT! MUST READ! BEFORE MIGRATE:
Make sure you have at least 2 users before running `python3 manage.py migrate`
You can create a second superuser with `python3 manage.py createsuperuser`

# DEV Logs
This document tracks the decisions and notes of the dev team during development.

## Frontend
Materialize is considered to be the main library for front-end styling.

## Backend
**DB name**: 'thomascollective'
```bash
$ createdb thomascollective
$ psql
$ \l # to confirm db was created successfully locally
$ \q # to quit psql shell
```

### Authorization Scheme
To enable different user roles, here is a proposed Scheme using built-in Group permissions logic in Django:
**Superuser**: Creates Railways and Railways' Groups
**Railway User Group**: Each Railway Owner belongs to their respective Railway Group. They can:
+ Add trains (only for their respective Railway Co.)
+ Add routes for trains (of their own Railways)
+ Add schedules to their routes
**Regular User**: Regular users (without any groups assigned, or assigned the Visitor Group?) will have READ-ONLY permissions on trains, routes, schedules. They will have full CRUD on their own tickets/bookingss

`#TODO: Read up on groups and learn implement `

## Varialbe Shorthands

+ Sched → Schedule


## Useful Links
+ [ERD](https://lucid.app/lucidchart/9aa16864-362a-4073-8b12-7755305c9e2e/edit?invitationId=inv_e53fdd8b-770e-4018-8026-a34c5377115b&page=0_0#) on LucidCharts
+ [Trello Board](https://trello.com/b/eUnu8rCY/project-3)
+ [Wireframes](https://app.moqups.com/zydknOceTn1aifT0uORbQN4cT4zzPNKf/edit/page/a73c8837f) on Moqup
+ [Presentation](https://docs.google.com/presentation/d/1u403N_MwglCmDOl0F7XIioxW4kPmkm6t_YmS8srrqQc/edit?usp=sharing) on Google Docs
+ [Materialize Docs](https://materializecss.com/getting-started.html)

## Useful Scripts
+ `pull_merge.sh`: Replace your branch name at the top. Use `source pull_merge.sh` to do the following:
  + `git checkout main`
  + `git pull upstream main`
  + `git push origin main`
  + `git checkout your-branch-name`
  + `git merge main`

+ `seed_trains.py`: Seed your db with multiple trains. Edit the trains array to your liking, then run `python3 seed_trains.py`. It will first check if a train with the same name exists (I'm guessing most of us already have 'Thomas' 😁) if not create a new record