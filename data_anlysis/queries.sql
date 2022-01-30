# 2. a

SELECT COUNT(*) as number_of_ads, offer_type
FROM ads
GROUP BY offer_type

# 2. b

SELECT COUNT(*) as number_of_selling_properties, city
FROM ads
WHERE offer_type = 'prodaja'
GROUP BY city
ORDER BY number_of_selling_properties DESC

# 2. c

SELECT COUNT(*) as number_of_properties, registered, property_type
FROM ads
GROUP BY registered, property_type

# 2. d

(SELECT *
FROM ads
WHERE property_type = 'kuce' AND offer_type = 'prodaja'
ORDER BY price DESC
LIMIT 30)
UNION
(SELECT *
FROM ads
WHERE property_type = 'stanovi' AND offer_type = 'prodaja'
ORDER BY price DESC
LIMIT 30)

# 2. e

(SELECT *
FROM ads
WHERE property_type = 'kuce'
ORDER BY square_footage DESC
LIMIT 100)
UNION
(SELECT *
FROM ads
WHERE property_type = 'stanovi'
ORDER BY square_footage DESC
LIMIT 100)

# 2. f

SELECT *
FROM ads
WHERE offer_type = 'prodaja' AND build_year = 2020
ORDER BY price DESC

SELECT *
FROM ads
WHERE offer_type = 'izdavanje' AND build_year = 2020
ORDER BY price DESC

# 2. g

# List properties ordered by room count
SELECT *
FROM ads
ORDER BY room_number DESC
LIMIT 30

# List flats ordered by square footage
SELECT *
FROM ads
WHERE property_type = 'stanovi'
ORDER BY square_footage DESC
LIMIT 30

# List houses ordered by land area
SELECT *
FROM ads
WHERE property_type = 'kuce'
ORDER BY land_area DESC
LIMIT 30