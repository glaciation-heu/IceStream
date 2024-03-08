use poem_openapi::{
    param::Path, 
    param::Query,
    OpenApi, 
    Object
};
use poem::Result;

mod participation;
mod register_upload;

pub struct Api;

#[derive(Object)]
struct UploadPayload {
    name: String,
    desc: Option<String>,
}

#[derive(Object)]
struct UploadRes {
    name: String,
    id: Option<u32>
}

#[OpenApi]
impl Api {

    /// input_party registers participation. Return input-specification and output-party config on success.
    #[oai(path = "/participation/:collaboration_id", method = "post")]
    async fn post_participation(&self, 
        /// identifier of collaboration to register
        collaboration_id: Path<u32>, 
        /// identifier of the registering party
        party_id: Query<i32>
    ) -> Result<participation::PostParticipationResponse> {
        participation::post(collaboration_id.0, party_id.0)
    }

    /// input_party unregisteres from participation.
    #[oai(path = "/participation/:collaboration_id", method = "delete")]
    async fn del_participation(&self, 
        /// identifier of collaboration to register
        collaboration_id: Path<u32>,
        /// identifier of the party that wishes to unregister
        party_id: Query<i32>) -> Result<participation::DelParticipationResponse> {
        participation::delete(collaboration_id.0, party_id.0)
    }

    /// input_party confirms upload done.
    #[oai(path = "/register-upload/:collaboration_id", method = "post")]
    async fn register_upload(&self, 
        /// identifier of collaboration to register
        collaboration_id: Path<u32>, 
        /// identifier of the registering party
        party_id: Query<u32>, 
        /// the id of the secrets returned from the computation party
        secret_ids: Query<Vec<String>>) -> Result<register_upload::PostRegisterUploadResponse> {
        register_upload::post(collaboration_id.0, party_id.0, secret_ids.0)
    }
}
