-- Creates the tables needed to store environmental data

CREATE TABLE envdata(
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    time TIMESTAMP NOT NULL,
    sensor TINYTEXT NOT NULL,

    humidity DOUBLE NOT NULL,
    pressure DOUBLE NOT NULL,
    temperature_from_humidity DOUBLE NOT NULL,
    temperature_from_pressure DOUBLE NOT NULL,

    orientation_pitch DOUBLE NOT NULL,
    orientation_roll DOUBLE NOT NULL,
    orientation_yaw DOUBLE NOT NULL,

    compass_x DOUBLE NOT NULL, 
    compass_y DOUBLE NOT NULL, 
    compass_z DOUBLE NOT NULL,

    gyroscope_pitch DOUBLE NOT NULL,
    gyroscope_roll DOUBLE NOT NULL,
    gyroscope_yaw DOUBLE NOT NULL,

    accelerometer_pitch DOUBLE NOT NULL,
    accelerometer_roll DOUBLE NOT NULL, 
    accelerometer_yaw DOUBLE NOT NULL
);