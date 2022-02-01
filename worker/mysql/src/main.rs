extern crate chrono;
use self::chrono::{DateTime, Utc};
use mysql::*;
use mysql::prelude::*;

#[derive(Debug, PartialEq, Eq)]
struct Server {
    id: i32,
    domain_name: Option<String>,
    domain_type: Option<String>,
    agency: Option<i32>,
    organization: Option<String>,
    status: Option<String>,
    clicks: i32,
    ipaddress: Option<String>,
    response_time: Option<i32>,
    last_checked: Option<chrono::NaiveDateTime>
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
)*/

#[derive(Debug, PartialEq, Eq)]
struct ServerLog {
    id: i32,
    datetime: Option<chrono::NaiveDateTime>,
    server_id: Option<i32>,
    response_code: Option<i32>,
    response_time: Option<i32>,
    ipaddress: Option<String>,
    url: String,
    error: Option<String>,
}

/*
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
