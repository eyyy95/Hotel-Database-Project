/* **********************************
Project Step 5 DMQ
GROUP 95 - Hotel of Hotels
Leon Samuel, Edward Yeow
********************************** */

/* First queries to select all columns of all tables within our database:*/
SELECT * FROM customers;
SELECT * FROM rooms;
SELECT * FROM orders;
SELECT * FROM distributors;
SELECT * FROM ordered_rooms;

/*Queries to insert data into respective data tables. All the data fields will be populated by the form on the web app. Auto incremented IDs not included*/
INSERT INTO customers (first_name, last_name, email)
VALUES (:first_name, :last_name, :email);
INSERT INTO rooms (distributor_id, distributor_name, beds, city, [state], price)
VALUES (:distributor_id, :distributor_name, :beds, :city, :state, :price);
INSERT INTO orders (customer_id, [start_date], end_date)
VALUES (:customer_id, :start_date, :end_date);
INSERT INTO ordered_rooms(room_id, order_id, total_price)
VALUES (:room_id, :order_id, :total_price);
INSERT INTO distributors(distributor_name, distributor_phone)
VALUES (:distributor_name, :distributor_phone);

/*Queries to delete individual rows of data from respective tables*/
DELETE FROM customers WHERE customer_id = :customer_id;
DELETE FROM rooms WHERE room_id = :room_id;
DELETE FROM orders WHERE order_id = :order_id;
DELETE FROM distributors WHERE distributor_id = :distributor_id;
/*Separate query to delete an ordered room entity. Identifies the entity through matching foreign keys, as opposed to primary keys like the previous 4 entities*/
DELETE FROM ordered_rooms WHERE order_id = :order_id AND room_id = :room_id

/*Queries to update individual rows of data based on user input*/
UPDATE customers SET first_name = :first_name, last_name = :last_name, email = :email WHERE customer_id = :customer_id;
UPDATE rooms SET distributor_id = :distributor_id, distributor_name = :distributor_name, beds = :beds, city = :city, state = :state, price = :price WHERE room_id = :room_id;
UPDATE orders SET customer_id = :customer_id, start_date = :start_date, end_date = :end_date WHERE order_id = order_id;
UPDATE distributors SET distributor_name = :distributor_name, distributor_phone = :distributor_phone WHERE distributor_id = :distributor_id;
/*Similar query logic to the delete statement for composite entity*/
UPDATE ordered_rooms SET room_id = :room_id, order_id = :order_id, total_price = :total_price WHERE order_id = :order_id AND room_id = :room_id;