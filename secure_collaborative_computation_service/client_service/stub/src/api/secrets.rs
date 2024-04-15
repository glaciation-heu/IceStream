use poem_openapi::{payload::{Json, PlainText}, ApiResponse};

use poem::Result;

pub type UploadPayload = String;
//#[derive(Object)]
//pub struct UploadPayload {
//    secrets: Vec<String>,
//    tags: Vec<String>
//}


#[derive(ApiResponse)]
pub enum UploadResponse {
    /// Secret created successfully.
    #[oai(status = 200)]
    OK(
        /// The ids of the created secret
        Json<Vec<String>>
    ),

    /// Did not find a project with this ID.
    #[oai(status = 404)]
    NotFound,

    #[oai(status = 406)]
    NotAcceptable
}


#[derive(ApiResponse)]
pub enum GetSecretResponse {
    /// Computation ID response
    #[oai(status = 200)]
    Secret(PlainText<String>),

    /// Did not find a project with this ID.
    #[oai(status = 404)]
    NotFound,

    /// Secret ID not specified
    #[oai(status = 406)]
    SecretNotFound
}

pub fn upload(_id: u32, _secrets: UploadPayload) -> Result<UploadResponse> {
    let res: Vec<String> = vec!["74b95c04-eb54-47e5-b8ca-bfe99383834f".to_string()];
    Ok(UploadResponse::OK(Json(res)))
}

pub fn get(_id: u32, _tags: Vec<String>) -> Result<GetSecretResponse> {
    Ok(GetSecretResponse::Secret(PlainText("my-secret".to_string())))
}

#[derive(ApiResponse)]
pub enum DelSecretResp {

    /// Removing secrets was successfull
    #[oai(status = 200)]
    OK(PlainText<String>),

    /// Did not find a project with this ID.
    #[oai(status = 404)]
    NotFound(PlainText<String>),

    /// Secret ID not specified
    #[oai(status = 406)]
    SecretNotFound
}

pub fn delete(_id: u32, _secret_ids: Vec<String>) -> Result<DelSecretResp> {
    Ok(DelSecretResp::OK(PlainText("secrets removed!".to_string())))
}
