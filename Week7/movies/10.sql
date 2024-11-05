SELECT DISTINCT name
FROM people
JOIN ratings ON directors.movie_id = ratings.movie_id
JOIN directors ON people.id = directors.person_id
WHERE rating >= 9.0;
