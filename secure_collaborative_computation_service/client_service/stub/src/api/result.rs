use poem_openapi::{payload::PlainText, ApiResponse};
use poem::Result;

#[derive(ApiResponse)]
pub enum ResultResponse {
    /// Computation ID response
    #[oai(status = 200)]
    ComputationResult(PlainText<String>),

    /// Did not find a project with this ID.
    #[oai(status = 404)]
    NotFound(PlainText<String>),

    /// The project has not finished computing.
    #[oai(status = 409)]
    ProcessingNotFinished
}

pub fn result(id: u32) -> Result<ResultResponse> {
    Ok(ResultResponse::ComputationResult(PlainText("result".to_string())))
}
