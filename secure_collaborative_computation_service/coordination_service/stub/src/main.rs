use poem::{listener::TcpListener, Route, Server};
use poem_openapi::OpenApiService;
use std::env;

mod api;
mod cs_definitions;

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt()
        .init();

    let port = match env::var("SERVICE_PORT") {
        Ok(port) => port,
        Err(_) => "8080".to_string()
    };

    let addr = match env::var("SERVICE_ADDRESS") {
        Ok(addr) => addr,
        Err(_) => "0.0.0.0".to_string()
    };

    println!("Starting coordination service on {}:{}", addr, port);

    let api_service =
        OpenApiService::new(api::Api, "Coordination Service", "1.0")
            .description("Coordination Service to coordinate MPC computations")
            .server(format!("http://{}:{}", addr, port));

    let ui = api_service.swagger_ui();
    let app = Route::new().nest("/", api_service).nest("/docs", ui);


    let _ = Server::new(TcpListener::bind(format!("{}:{}", addr, port)))
        .run(app)
        .await;
}
