SELECT DISTINCT name
FROM people
JOIN movies ON stars.movie_id = movies.id
JOIN stars ON people.id = stars.person_id
WHERE year = 2004
ORDER BY birth ASC;
