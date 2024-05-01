use serde::{Deserialize, Serialize};

use poem_openapi::Object;

#[derive(Object, Deserialize, Serialize)]
pub struct CsProviderConfig {
    amphoraServiceUrl: String,
    castorServiceUrl: String,
    ephemeralServiceUrl: String,
    id: i32,
    baseUrl: String
}

#[derive(Object, Deserialize, Serialize)]
pub struct CsConfig {
    prim: String,
    r: String,
    rinv: String,
    noSslValidation: bool,
    trustedCertificates: Vec<String>,
    providers: Vec<CsProviderConfig>
}