use poem::Result;
use poem_openapi::{
    payload::{Json, PlainText},
    ApiResponse, Object,
};
use sysinfo::System;

#[derive(Object)]
pub struct SysStatus {
    mem_consumption: f32,
    kernel_version: Option<String>,
    os_version: Option<String>,
    host_name: Option<String>,
}

#[derive(ApiResponse)]
pub enum SysStatusResponse {
    #[oai(status = 200)]
    Ok(Json<SysStatus>),
    #[oai(status = 500)]
    InternalServerError(PlainText<String>),
}

pub fn sys_status() -> Result<SysStatusResponse> {
    let mut sys = System::new_all();
    sys.refresh_all();
    let status = SysStatus {
        mem_consumption: sys.used_memory() as f32 / sys.total_memory() as f32,
        kernel_version: System::kernel_version(),
        os_version: System::long_os_version(),
        host_name: System::host_name(),
    };
    Ok(SysStatusResponse::Ok(Json(status)))
}
