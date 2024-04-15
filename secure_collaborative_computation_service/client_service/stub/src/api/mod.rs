use poem_openapi::{
    payload::PlainText,
    param::Path, 
    param::Query,
    OpenApi, 
    Object
};
use poem::Result;

mod secrets;
mod result;
mod notify;
mod sys_status;

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

    /// Create secrets. access-scope: input_party
    #[oai(path = "/secrets/:collaboration_id", method = "post")]
    async fn upload(&self, 
        /// identifier of collaboration
        collaboration_id: Path<u32>,
        /// csv of secrets
        payload: PlainText<secrets::UploadPayload>) -> Result<secrets::UploadResponse> {
        secrets::upload(collaboration_id.0, payload.0)
    }

    /// get secrets by tag. access-scope: input_party
    #[oai(path = "/secrets/:collaboration_id", method = "get")]
    async fn get_secrets(&self, 
        /// identifier of collaboration
        collaboration_id: Path<u32>, 
        /// identifiers of secrets to get
        secret_ids: Query<Vec<String>>) -> Result<secrets::GetSecretResponse> {
        secrets::get(collaboration_id.0, secret_ids.0)
    }

    /// delete secrets with id. access-scope: input_party
    #[oai(path = "/secrets/:collaboration_id", method = "delete")]
    async fn del_result(&self, 
        /// identifier of collaboration
        collaboration_id: Path<u32>, 
        /// identifiers of secrets to remove
        secret_ids: Query<Vec<String>>) -> Result<secrets::DelSecretResp> {
        secrets::delete(collaboration_id.0, secret_ids.0)
    }

    /// Get computation results (checks if computation is ready). access-scope: output_party
    #[oai(path = "/result/:collaboration_id", method = "get")]
    async fn get_result(&self, collaboration_id: Path<u32>) -> Result<result::ResultResponse> {
        result::result(collaboration_id.0)
    }

    /// Start the computation. access-scope: coordinator
    #[oai(path = "/notify/:collaboration_id", method = "put")]
    async fn notify(&self, 
        /// identifier of collaboration
        collaboration_id: Path<u32>) -> Result<notify::NotifyResponse> {
        Ok(notify::NotifyResponse::NotWaiting)
    }

    /// Returns status code 200. Used to check if service is available.
    #[oai(path = "/ping", method = "get")]
    async fn ping(&self) -> Result<()> {
        Ok(())
    }

    /// Get system informations.
    #[oai(path = "/sys_status", method = "get")]
    async fn sys_status(&self) -> Result<sys_status::SysStatusResponse> {
        sys_status::sys_status()
    }
}
