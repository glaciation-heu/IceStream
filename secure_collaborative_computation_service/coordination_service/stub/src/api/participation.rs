use poem_openapi::{payload::{PlainText, Json}, ApiResponse, Object};
use serde::{Serialize, Deserialize};
use poem::Result;
use crate::cs_definitions;

#[derive(Object, Deserialize, Serialize)]
pub struct PostParticipationResponseBody {
    cs_config: cs_definitions::CsConfig,
    csv_specification: String
}

#[derive(ApiResponse)]
pub enum PostParticipationResponse {
    /// Successfully added to participating parties.
    #[oai(status = 200)]
    ComputationResult(Json<PostParticipationResponseBody>),

    /// Already added as participating party.
    #[oai(status = 208)]
    AlreadyAdded(Json<PostParticipationResponseBody>),

    /// Did not find a project with this ID.
    #[oai(status = 404)]
    NotFound,
}

pub fn post(computation_id: u32, party_id: i32) -> Result<PostParticipationResponse> {
    Ok(PostParticipationResponse::NotFound)
}

#[derive(ApiResponse)]
pub enum DelParticipationResponse {
    /// Successfully removed from participating parties.
    #[oai(status = 200)]
    Removed,

    /// Did not find a project with this ID.
    #[oai(status = 404)]
    NotFound,
}

pub fn delete(computation_id: u32, party_id: i32) -> Result<DelParticipationResponse> {

    Ok(DelParticipationResponse::NotFound)
}
