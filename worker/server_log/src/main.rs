
#![allow(unused)]

extern crate chrono;
use self::chrono::{DateTime, Utc};
use sqlx::mysql::{MySqlPoolOptions, MySqlRow};
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
    last_checked: chrono::NaiveDateTime,
}

#[derive(Debug, FromRow)]
struct ServerLog {
    id: i32,
    datetime: chrono::NaiveDateTime,
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
    
        println!("\n=== select tickets with query.map...:\n{:?}", servers);
    Ok(())
}