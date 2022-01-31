extern crate chrono;
use self::chrono::{DateTime, Duration, NaiveDate, NaiveDateTime, NaiveTime, TimeZone, Utc};

#[derive(Queryable)]
pub struct Server {
    pub id: i32,
    pub domain_name: String,
    pub domain_type: String,
    pub agency: i32,
    pub organization: String,
    pub status: String,
    pub clicks: i32,
    pub ipaddress: String,
    pub response_time: i32,
    pub last_checked: chrono::NaiveDateTime
}

/*
CREATE TABLE `server` (
  `id` int NOT NULL AUTO_INCREMENT,
  `domain_name` varchar(255) NOT NULL,
  `domain_type` varchar(255) DEFAULT NULL,
  `agency` int DEFAULT NULL,
  `organization` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `clicks` int DEFAULT NULL,
  `ipaddress` varchar(255) DEFAULT NULL,
  `response_time` int DEFAULT NULL,
  `last_checked` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
)
CREATE TABLE `serverlog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `datetime` datetime NOT NULL,
  `server_id` int DEFAULT NULL,
  `response_code` int DEFAULT NULL,
  `response_time` int DEFAULT NULL,
  `ipaddress` varchar(255) DEFAULT NULL,
  `url` varchar(255) NOT NULL,
  `error` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `server_id` (`server_id`),
  CONSTRAINT `serverlog_ibfk_1` FOREIGN KEY (`server_id`) REFERENCES `server` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=424 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
*/