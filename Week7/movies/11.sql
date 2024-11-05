SELECT title
FROM stars
JOIN ratings ON movies.id = ratings.movie_id
JOIN movies ON stars.movie_id = movies.id
WHERE person_id =
(
    SELECT id
    FROM people
    WHERE name = 'Chadwick Boseman'
)
ORDER BY rating DESC
LIMIT 5;

