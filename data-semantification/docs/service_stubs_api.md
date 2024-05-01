# API Documentation for Data Reception Endpoints

This document outlines the current API endpoints, their methods, and anticipated responses for the data reception service in our Apache NiFi project. Our system is designed to handle a variety of data formats from robots and sensors, starting with NumPy `.npy` files.

## Current Endpoints

### NumPy `.npy` File Reception

- **Endpoint**: `/api/data/npy`
- **Method**: `POST`
- **Description**: Accepts NumPy `.npy` files for processing. This endpoint is designed to receive data files from robots and sensors, perform initial validation, and queue them for further processing.
- **Request Body**:
  - **Type**: `multipart/form-data`
  - **Content**: A file with the `.npy` extension.
- **Responses**:
  - **200 OK**:
    - **Description**: The file has been successfully received and validated.
    - **Body**: 
    ```json
    {
      "message": "File received successfully.",
      "fileId": "unique_file_identifier",
      "timestamp": "2023-03-02T14:00:00Z"
    }
    ```
  - **400 Bad Request**:
    - **Description**: The uploaded file is not a valid `.npy` file or did not meet validation criteria.
    - **Body**:
    ```json
    {
      "error": "Invalid file format or validation failed.",
      "details": "Specific details about the validation failure."
    }
    ```

## Future Endpoints

As our project evolves to support additional data formats, new endpoints will be documented in this section. Each format will have a dedicated endpoint similar to the `.npy` file reception, ensuring clear separation and specialized processing logic for each data type.

## Versioning and Updates

This API documentation will be regularly updated to reflect new endpoints, changes in the data processing logic, and modifications in response formats. We follow semantic versioning for our API to ensure backward compatibility and clear communication with all stakeholders about the changes and their impact.

## Conclusion

This API serves as the backbone for data reception and processing in our Apache NiFi project. By documenting our endpoints, methods, and responses, we aim to provide clarity and ease of use for developers and integrators working with our system. As we expand our capabilities to include more data formats, this document will be an essential resource for understanding and interacting with our services.

