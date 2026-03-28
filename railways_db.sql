INSERT INTO trains(train_number, train_name, train_type, source, destination, total_seats)
VALUES
(12001,'Rajdhani Express','Superfast','Delhi','Mumbai',500),
(12002,'Shatabdi Express','Superfast','Delhi','Chandigarh',300),
(12003,'Duronto Express','Superfast','Kolkata','Delhi',400),
(12004,'Garib Rath','Express','Patna','Delhi',350),
(12005,'Vande Bharat','Semi-High Speed','Varanasi','Delhi',250),
(12006,'Humsafar Express','Express','Patna','Bangalore',450),
(12007,'Jan Shatabdi','Express','Delhi','Lucknow',320),
(12008,'Intercity Express','Passenger','Patna','Kolkata',280),
(12009,'Tejas Express','Premium','Mumbai','Goa',350),
(12010,'Sampark Kranti','Express','Patna','Delhi',400);
INSERT INTO passengers(passenger_name, age, gender, phone, email)
VALUES
('Rahul Sharma',28,'Male','9876543210','rahul@gmail.com'),
('Priya Singh',25,'Female','9876543211','priya@gmail.com'),
('Amit Kumar',35,'Male','9876543212','amit@gmail.com'),
('Neha Verma',22,'Female','9876543213','neha@gmail.com'),
('Ravi Raj',30,'Male','9876543214','raviraj@gmail.com'),
('Anjali Kumari',27,'Female','9876543215','anjali@gmail.com'),
('Suresh Yadav',40,'Male','9876543216','suresh@gmail.com'),
('Pooja Mishra',26,'Female','9876543217','pooja@gmail.com'),
('Vikash Gupta',31,'Male','9876543218','vikash@gmail.com'),
('Kiran Patel',29,'Female','9876543219','kiran@gmail.com');
INSERT INTO bookings(passenger_id, train_id, coach_number, seat_number, booking_status, payment_status, fare, journey_date, booking_date)
VALUES
(1,1,'A1','21','Confirmed','Paid',2500,'2026-03-20',NOW()),
(2,2,'B2','15','Confirmed','Paid',1200,'2026-03-21',NOW()),
(3,3,'C1','30','Waiting','Pending',1800,'2026-03-22',NOW()),
(4,4,'D3','12','Confirmed','Paid',900,'2026-03-23',NOW()),
(5,5,'A2','05','Confirmed','Paid',1500,'2026-03-24',NOW()),
(6,6,'B1','18','Cancelled','Refunded',2200,'2026-03-25',NOW()),
(7,7,'S1','45','Confirmed','Paid',700,'2026-03-26',NOW()),
(8,8,'S2','33','Waiting','Pending',650,'2026-03-27',NOW()),
(9,9,'P1','11','Confirmed','Paid',3200,'2026-03-28',NOW()),
(10,10,'S3','28','Confirmed','Paid',1100,'2026-03-29',NOW());
SELECT * FROM trains;
SELECT * FROM passengers;
SELECT * FROM bookings;
SELECT * FROM tickets;
INSERT INTO trains(train_name, source, destination, total_seats, train_type)
VALUES
('Rajdhani Express','Delhi','Mumbai',500,'Superfast'),
('Shatabdi Express','Delhi','Chandigarh',300,'Express'),
('Duronto Express','Kolkata','Delhi',400,'Superfast'),
('Garib Rath','Patna','Delhi',350,'Express'),
('Vande Bharat','Varanasi','Delhi',250,'Semi High Speed'),
('Humsafar Express','Patna','Bangalore',450,'AC Express'),
('Tejas Express','Mumbai','Goa',320,'Luxury'),
('Intercity Express','Lucknow','Kanpur',280,'Passenger'),
('Jan Shatabdi','Bhopal','Delhi',300,'Express'),
('Sampark Kranti','Patna','Delhi',420,'Superfast');
INSERT INTO passengers(name, age, gender, phone, email)
VALUES
('Rahul Sharma',28,'Male','9876541111','rahul@gmail.com'),
('Priya Singh',25,'Female','9876541112','priya@gmail.com'),
('Amit Kumar',35,'Male','9876541113','amit@gmail.com'),
('Neha Verma',22,'Female','9876541114','neha@gmail.com'),
('Ravi Raj',30,'Male','9876541115','ravi@gmail.com'),
('Anjali Kumari',27,'Female','9876541116','anjali@gmail.com'),
('Karan Mehta',32,'Male','9876541117','karan@gmail.com'),
('Sneha Das',24,'Female','9876541118','sneha@gmail.com'),
('Rohit Singh',31,'Male','9876541119','rohit@gmail.com'),
('Pooja Sharma',26,'Female','9876541120','pooja@gmail.com'),
('Arjun Gupta',29,'Male','9876541121','arjun@gmail.com'),
('Meera Iyer',34,'Female','9876541122','meera@gmail.com');
INSERT INTO bookings(passenger_id, train_id, seat_number, coach_number, booking_status, booking_date, travel_date, fare)
VALUES
(1,1,'21','A1','Confirmed',NOW(),'2026-04-01',1500),
(2,2,'15','B2','Confirmed',NOW(),'2026-04-02',1200),
(3,3,'30','C1','Waiting',NOW(),'2026-04-03',1800),
(4,4,'12','D3','Confirmed',NOW(),'2026-04-04',900),
(5,5,'05','A2','Confirmed',NOW(),'2026-04-05',2000),
(6,6,'18','B1','Cancelled',NOW(),'2026-04-06',1700),
(7,7,'11','A3','Confirmed',NOW(),'2026-04-07',2200),
(8,8,'08','C2','Confirmed',NOW(),'2026-04-08',700),
(9,9,'19','D1','Waiting',NOW(),'2026-04-09',1300),
(10,10,'25','B3','Confirmed',NOW(),'2026-04-10',1600),
(11,3,'09','A1','Confirmed',NOW(),'2026-04-11',1900),
(12,4,'16','C1','Confirmed',NOW(),'2026-04-12',1000);
SELECT * FROM trains;
SELECT * FROM passengers;
SELECT * FROM bookings;
SELECT * FROM tickets;
SELECT 
p.name,
t.train_name,
s1.station_name AS source_station,
s2.station_name AS destination_station,
b.seat_number,
b.class_type,
b.status AS booking_status,
b.travel_date
FROM bookings b
JOIN passengers p ON b.passenger_id = p.passenger_id
JOIN trains t ON b.train_id = t.train_id
JOIN routes r ON r.train_id = t.train_id
JOIN stations s1 ON r.source_station = s1.station_id
JOIN stations s2 ON r.destination_station = s2.station_id;
ALTER TABLE bookings
ADD COLUMN class_type VARCHAR(20);
UPDATE bookings SET class_type = 'AC' WHERE seat_number <= 20;
UPDATE bookings SET class_type = 'Sleeper' WHERE seat_number > 20;
ALTER TABLE bookings
ADD COLUMN class_type VARCHAR(20);
ALTER TABLE bookings
ADD COLUMN booking_status VARCHAR(20);
UPDATE bookings
SET class_type = 'AC'
WHERE seat_number <= 20;
UPDATE bookings
SET class_type = 'Sleeper'
WHERE seat_number > 20;
UPDATE bookings
SET booking_status = 'Confirmed';
SELECT * FROM bookings;
SELECT column_name
FROM information_schema.columns
WHERE table_name='bookings';
SELECT *
FROM information_schema.columns
WHERE table_name='bookings';
SELECT * FROM bookings;
-- TRAINS TABLE
CREATE TABLE trains (
    train_id SERIAL PRIMARY KEY,
    train_name VARCHAR(100),
    source VARCHAR(50),
    destination VARCHAR(50),
    total_seats INT
);

-- PASSENGERS TABLE
CREATE TABLE passengers (
    passenger_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10)
);

-- BOOKINGS TABLE
CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    passenger_id INT,
    train_id INT,
    booking_date DATE,
    seat_number INT,
    class_type VARCHAR(20),
    FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id),
    FOREIGN KEY (train_id) REFERENCES trains(train_id)
);

-- PAYMENTS TABLE
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    booking_id INT,
    amount DECIMAL(10,2),
    payment_status VARCHAR(20),
    payment_date DATE,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
);
-- TRAINS
INSERT INTO trains (train_name, source, destination, total_seats) VALUES
('Rajdhani Express', 'Delhi', 'Mumbai', 500),
('Shatabdi Express', 'Delhi', 'Chandigarh', 300);

-- PASSENGERS
INSERT INTO passengers (name, age, gender) VALUES
('Amit Sharma', 28, 'Male'),
('Priya Singh', 24, 'Female');

-- BOOKINGS
INSERT INTO bookings (passenger_id, train_id, booking_date, seat_number, class_type) VALUES
(1, 1, '2026-03-28', 45, 'AC'),
(2, 2, '2026-03-28', 12, 'Sleeper');

-- PAYMENTS
INSERT INTO payments (booking_id, amount, payment_status, payment_date) VALUES
(1, 1500.00, 'Completed', '2026-03-28'),
(2, 800.00, 'Completed', '2026-03-28');
-- View all bookings with passenger + train details
SELECT p.name, t.train_name, b.seat_number, b.class_type
FROM bookings b
JOIN passengers p ON b.passenger_id = p.passenger_id
JOIN trains t ON b.train_id = t.train_id;

-- Total revenue
SELECT SUM(amount) AS total_revenue FROM payments;