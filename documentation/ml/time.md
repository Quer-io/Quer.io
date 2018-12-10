# Handling dates and times with Querio

Many databases contain dates and times, stored as
objects in a the format of the database system.
These can be very important to handle in where-clauses.
For example, an online store might want to find information regarding purchases in March, or on Sundays.

Querio cannot compute month or day names from the
timestamps the database contains, but if the database
contains the day or month names, they are handled
just like any categorical data. Creating a view
with day or month names is simple and doesn't
interfere with the rest of the database.

Let's create such a view in PostgreSQL.
The example database contains a table person with
the following columns:
| Column | Type |
| --- | --- |
| id | integer |
| income | numeric |
| height | numeric |
| date_of_birth | date |

For our queries, we need a table like the
this:
| Column | Type |
| --- | --- |
| id | integer |
| income | numeric |
| height | numeric |
| weekday | varchar |

The this statement creates this view with a
weekday column containing the day of the week the
person was born.
```sql
CREATE OR REPLACE VIEW querio_view AS (
    SELECT height, income,
    TRIM(TO_CHAR(date_of_birth, 'day')) AS weekday
    FROM person
);
```
The view can be used instead of a table when creating
querio models. In case we needed the month they were
born on replace 'day', with 'month' in the
preciding statement.
```sql
CREATE OR REPLACE VIEW querio_view AS (
    SELECT height, income,
    TRIM(TO_CHAR(date_of_birth, 'month')) AS weekday
    FROM person
);
```
The ```TO_CHAR``` function of PostgreSQL contains
many more formats it can simplify the timestamp to,
see it's
[documentation](https://www.postgresql.org/docs/9.5/functions-formatting.html)
for full details. The string returned by
```TO_CHAR``` can contain trailing spaces. The
```TRIM``` function removes them.
