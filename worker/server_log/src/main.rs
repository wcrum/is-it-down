
use sqlx::mysql::MySqlPoolOptions;

#[tokio::main]
async fn main() -> Result<(), sqlx::Error> {
	// 1) Create a connection pool
	let pool = MySqlPoolOptions::new()
		.max_connections(5)
		.connect("postgres://postgres:welcome@localhost/postgres");

        Ok(())
}