DROP DATABASE vkeiba;
CREATE DATABASE vkeiba;
CREATE TABLE vkeiba.race_result
(
  race_id varchar(10) NOT NULL,
  row_id tinyint NOT NULL,
  final_position varchar(3) NOT NULL,
  frame_number tinyint NOT NULL,
  horse_number tinyint NOT NULL,
  horse_id varchar(10) NOT NULL,
  sex varchar(2) NOT NULL,
  age varchar(2) NOT NULL,
  jockey_id varchar(10) NOT NULL,
  time time DEFAULT NULL,
  margin varchar(10) DEFAULT NULL,
  passing_position varchar(20) DEFAULT NULL,
  last_3f time DEFAULT NULL,
  jockey_weight float(4, 2) NOT NULL,
  horse_weight smallint,
  popularity tinyint DEFAULT NULL,
  odds float(5, 1) DEFAULT NULL,
  blinker varchar(1) DEFAULT NULL
);

CREATE TABLE vkeiba.race_info
(
  race_id varchar(10) NOT NULL,
  race_date date NOT NULL,
  times tinyint NOT NULL,
  place varchar(2) NOT NULL,
  days tinyint NOT NULL,
  start_time varchar(10) NOT NULL,
  race_name varchar(40) NOT NULL,
  weather varchar(2) NOT NULL,
  track_condition varchar(2) NOT NULL,
  track_type varchar(3) NOT NULL,
  rotation varchar(5) NOT NULL,
  distance smallint NOT NULL,
  race_condition varchar(10) NOT NULL,
  grade varchar(10) NOT NULL,
  race_type varchar(30) NOT NULL,
  money varchar(40) NOT NULL
);
