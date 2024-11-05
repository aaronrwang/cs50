-- Keep a log of any SQL queries you execute as you solve the mystery.
Query 1:
SELECT * FROM crime_scene_reports WHERE year = 2023 AND month = 7 AND day = 28 AND street = 'Humphrey Street';
Result 1:
-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.

Query 2:
SELECT * FROM interviews WHERE transcript LIKe '%bakery%';
Result 2:
-- Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
-- I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
-- As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.

Query 3:
SELECT name FROM people WHERE id in(SELECT person_id FROM bank_accounts WHERE account_number in(SELECT account_number FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'));
Result 3:
-- Suspects: Kenny, Iman, Benista, Taylor, Brooke, Luca, Diana & Bruce

Query 4:
SELECT * FROM flights WHERE year = 2023 AND month = 7 AND day = 29;
Result 4:
-- ID: 36, origin_airport_id: 8, destination_airport_id: 4  YYYYMMDD: 2023/7/29  TIME: 8:20

Query 5:
SELECT city FROM airports WHERE id = 4;
Result 5:
-- Destionation: New York City

Query 6:
SELECT name FROM people WHERE passport_number in(SELECT passport_number FROM passengers WHERE flight_id = 36);
Result 6:
-- Suspects: Kenny, Sofia, Taylor, Luca, Kelsey, Edward, Bruce & Doris

Query 7:
Query 3 INTERSECT Query 6
Result 7:
-- Suspects: Bruce, Kenny, Luca & Taylor

Query 8:
SELECT name FROM people WHERE phone_number in (SELECT caller FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60);
Result 8:
-- In conjuction with Query 7, Suspects: Kenny, Bruce & Taylor

Query 9:
SELECT name FROM people WHERE phone_number in (SELECT receiver FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60);
Result 9:
-- In conjuction with Query 8, Accomplice Suspect: James, Robin & Jacqueline (respectivelly)

Query 10:
SELECT name FROM people WHERE license_plate in (SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 and activity = 'exit' AND minute > 15 AND minute < 25);
Result 10:
-- In conjuction with Query 8: Suspect: Bruce and thus Accomplice: Robin

Logic:
-- Using INTERSECT for Queries: 3, 6, 8 & 10 suspect = Bruce: Consequently Accomplice is Ben; Tracking earliest flight on 07/29/2023, escape city: New York City
