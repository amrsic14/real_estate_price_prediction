CREATE DATABASE IF NOT EXISTS real_estate_ads;

USE real_estate_ads;

CREATE TABLE IF NOT EXISTS ads(
   id INT NOT NULL AUTO_INCREMENT,
   price DOUBLE,
   link VARCHAR(200),
   offer_type VARCHAR(10),
   property_type VARCHAR(10),
   city VARCHAR(20),
   municipality VARCHAR(30),
   room_number DOUBLE,
   square_footage DOUBLE,
   heating VARCHAR(20),
   floor VARCHAR(10),
   bathroom_number INT,
   build_year INT,
   elevator BOOLEAN,
   balcony BOOLEAN,
   land_area DOUBLE,
   registered BOOLEAN,
   parking BOOLEAN,
   PRIMARY KEY (id)
);
