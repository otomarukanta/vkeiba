# DB設計

## race_info

```
create table vkeiba.race_info(
  race_id varchar(10) PRIMARY KEY,
  date date,
  times tinyint unsigned,
  place varchar(2),
  days varchar(2),
  start_time time,
  race_name varchar(20),
  weather varchar(2),
  track_condition varchar(2),
  track_type varchar(3),
  round varchar(1),
  distance smallint unsigned,
  race_condition varchar(10),
  grade varchar(6),
  race_type varchar(20),
  money varchar(20)
);
```

## race_result

CREATE TABLE vkeiba.race_result (
  race_id varchar(10) PRIMARY KEY,
  row_id varchar(2) PRIMARY KEY,
  final_position varchar(3) DEFAULT NULL,
  bracket tinyint(4) DEFAULT NULL,
  post_position tinyint(4) DEFAULT NULL,
  horse_id varchar(5) DEFAULT NULL,
  sex varchar(2) DEFAULT NULL,
  age varchar(2) DEFAULT NULL,
  jockey_id varchar(10) DEFAULT NULL,
  time time DEFAULT NULL,
  margin varchar(10) DEFAULT NULL,
  passing_position varchar(20) DEFAULT NULL,
  last_3f time DEFAULT NULL,
  impost float(4,2) DEFAULT NULL,
  weight smallint(6) DEFAULT NULL,
  weight_change smallint(6) DEFAULT NULL,
  popularity tinyint(4),
  ozz floa(4,1) DEFAULT NULL,
  blinker tinyint(1)
);

```
