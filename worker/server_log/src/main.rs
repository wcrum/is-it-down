
#![allow(unused)]

extern crate chrono;
use self::chrono::{DateTime, Utc};
use sqlx::mysql::MySqlPoolOptions;
use sqlx::{FromRow, Row};

#[derive(Debug, FromRow)]
struct Server {
    id: i32,
    domain_name: String,
    domain_type: String,
    agency: i32,
    organization: String,
    status: String,
    clicks: i32,
    ipaddress: String,
    response_time: i32,
    last_checked: chrono::DateTime<chrono::Utc>
}

#[derive(Debug, FromRow)]
struct ServerLog {
    id: i32,
    datetime: chrono::DateTime<chrono::Utc>,
    server_id: i32,
    response_code: i32,
    response_time: i32,
    ipaddress: String,
    url: String,
    error: String,
}


#[tokio::main]
async fn main() -> Result<(), sqlx::Error> {
	let pool = MySqlPoolOptions::new()
		.max_connections(5)
		.connect("mysql://testing:testing@localhost/testing")
        .await?;

    Ok(())
}