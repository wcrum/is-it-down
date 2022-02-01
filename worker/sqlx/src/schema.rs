table! {
    server (id) {
        id -> Int4,
        domain_name -> Text,
        domain_type -> Text,
        agency -> Integer,
        organization -> Text,
        status -> Text,
        clicks -> Integer,
        ipaddress -> Text,
        response_time -> Integer,
        last_checked -> Datetime,
    }
}