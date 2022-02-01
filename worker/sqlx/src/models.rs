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
