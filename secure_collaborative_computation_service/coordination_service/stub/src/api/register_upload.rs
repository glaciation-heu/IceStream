use poem_openapi::ApiResponse;

use poem::Result;

#[derive(ApiResponse)]
pub enum PostRegisterUploadResponse {
    /// upload registered successful
    #[oai(status = 200)]
    OK,

    /// Already registered.
    #[oai(status = 208)]
    AlreadyRegistered,

    /// Error, Project not found
    #[oai(status = 404)]
    NotFound
}

pub fn post(collaboration_id: u32, party_id: u32, secret_ids: Vec<String>) -> Result<PostRegisterUploadResponse> {
    Ok(PostRegisterUploadResponse::NotFound)
}
