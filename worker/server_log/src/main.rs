
#![allow(unused)]

extern crate chrono;
use self::chrono::{DateTime, Utc};
use sqlx::mysql::{MySqlPoolOptions, MySqlRow};
use sqlx::{FromRow, Row};

#[derive(Debug, FromRow)]
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

#[derive(Debug, FromRow)]
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

#[tokio::main]
async fn main() -> Result<(), sqlx::Error> {
	let pool = MySqlPoolOptions::new()
		.max_connections(5)
		.connect("mysql://testing:testing@localhost/testing")
        .await?;

    let select_query = sqlx::query("SELECT * FROM server");

    let servers: Vec<Server> = select_query
        .map(|row: MySqlRow| Server {
            id: row.get("id"),
            domain_name: row.get("domain_name"),
            domain_type: row.get("domain_type"),
            agency: row.get("agency"),
            organization: row.get("organization"),
            status: row.get("status"),
            clicks: row.get("clicks"),
            ipaddress: row.get("ipaddress"),
            response_time: row.get("response_time"),
            last_checked: row.get("last_checked")
        })
        .fetch_all(&pool)
        .await?;
    
    println!("Worker starting. Scrapping {} servers.", servers.len());
    for s in &servers {

    }
    
    Ok(())
}