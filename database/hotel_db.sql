/* **********************************
Project Step 5 DDQ
GROUP 95 - Hotel of Hotels
Leon Samuel, Edward Yeow
********************************** */

/*Refreshes our database*/
DROP
    TABLE IF EXISTS customers;
DROP
    TABLE IF EXISTS rooms;
DROP
    TABLE IF EXISTS orders;
DROP
    TABLE IF EXISTS ordered_rooms;
DROP 
    TABLE IF EXISTS distributors;

/*Table for tracking customer data*/
CREATE TABLE customers (
  customer_id int(11) NOT NULL AUTO_INCREMENT UNIQUE,
  first_name varchar(255) NOT NULL,
  last_name varchar(255) NOT NULL,
  email varchar(255) NOT NULL,
  PRIMARY KEY (customer_id)
);

/*Sample values/data for starters*/
INSERT INTO customers(first_name, last_name, email) 
VALUES 
    ('Jenny', 'Fromdabloc', 'jfromda@email.com'),
    ('Jennifer', 'Ofel', 'jofel@gmail.com'),
    ('Mary', 'Polk', 'mpolk@email.com'),
    ('Stephanie', 'Koi', 'skoi@email.com');

/*Table to track current room distributors in the system*/
CREATE TABLE distributors (
  distributor_id int(11) NOT NULL AUTO_INCREMENT UNIQUE,
  distributor_name varchar(255) NOT NULL,
  distributor_phone varchar(255) NOT NULL,
  PRIMARY KEY (distributor_id)
);

/*Sample values/data for starters*/
INSERT INTO distributors(distributor_name, distributor_phone)
VALUES 
    ('Hotel Five', '8055558976'), 
    ('Hilton', '5555555555'), 
    ('Big Yellow House', '8185557322');


/*Table for tracking room data*/
CREATE TABLE rooms (
  room_id int(11) NOT NULL AUTO_INCREMENT UNIQUE,
  distributor_id int(11),
  distributor_name varchar(255) NOT NULL,
  beds int(11) NOT NULL,
  city varchar(255) NOT NULL,
  state varchar(255) NOT NULL,
  price float(11) NOT NULL,
  PRIMARY KEY (room_id)
);

/*Sample values/data for starters*/
INSERT INTO rooms(distributor_id, distributor_name, beds, city, state, price)
VALUES 
    (1, 'Hilton', 2, 'Phoenix', 'CA', 43.65 ), 
    (2, 'Hotel Five', 2, 'Minneapolis', 'MN', 109.87), 
    (3, 'Big Yellow House', 1, 'Goleta', 'CA', 78.96);


/*Table to track current orders in the system*/
CREATE TABLE orders (
    order_id int(11) NOT NULL AUTO_INCREMENT UNIQUE,
    customer_id int(11) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    PRIMARY KEY (order_id)
);

/*Sample values/data for starters*/
INSERT INTO orders(customer_id, start_date, end_date)
VALUES 
    (1, '2021-09-23', '2021-09-25'), 
    (2, '2021-06-17', '2021-06-20'), 
    (3, '2021-03-03', '2021-03-05');


/*Table to track rooms part of current orders in the system. Encompasses the many to many relationship link between rooms and orders*/
CREATE TABLE ordered_rooms (
  room_id int(11) NOT NULL,
  order_id int(11) NOT NULL,
  total_price float(11) NOT NULL
);


/*Sample values/data for starters. Users won't have to manually input price, will use below queries to calculate total price from foreign keys*/
INSERT INTO ordered_rooms(room_id, order_id, total_price) 
VALUES 
    (1, 1, 0), /*Initializing total_price values as 0, below queries will calculate actual price*/
    (2, 2, 0), 
    (3, 3, 0);


UPDATE ordered_rooms
SET total_price = (SELECT rooms.price FROM rooms WHERE rooms.room_id = ordered_rooms.room_id); /*First updates price from foreign key for rooms; adds individual price first*/

UPDATE ordered_rooms
SET total_price = ordered_rooms.total_price * (SELECT DATEDIFF(orders.end_date, orders.start_date) FROM orders WHERE orders.order_id = ordered_rooms.order_id); /*Multiplies single room price by number of days in the order*/


/*Separate queries to insert foreign keys. Foreign key definitions within CREATE queries were causing some errors*/
ALTER TABLE rooms
ADD FOREIGN KEY (distributor_id) REFERENCES distributors (distributor_id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE orders
ADD FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE ordered_rooms
    ADD FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE CASCADE ON UPDATE CASCADE,
    ADD FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE ON UPDATE CASCADE;