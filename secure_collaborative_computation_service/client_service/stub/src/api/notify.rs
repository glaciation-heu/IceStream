use poem_openapi::{ApiResponse, payload::PlainText};



#[derive(ApiResponse)]
pub enum NotifyResponse {
    /// Notification accepted
    #[oai(status = 202)]
    NotificationAccepted,

    /// Do not wait for results of the given collaboration_id
    #[oai(status = 406)]
    NotWaiting,
}