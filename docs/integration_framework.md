

 - An integration framework is a crucial component in modern software development that facilitates the seamless connection and communication between different software applications, systems, or services. Its primary purpose is to streamline the exchange of data and functionalities, allowing disparate technologies to work together efficiently. In our work environment, the integration framework serves as the backbone for ensuring interoperability and cohesion across various tools and systems.

- **Hiro** is leading task 2.4 and 7.2 and will be responsible for the ingeration framework.

## The integration framework:
- [Process](#process)
- [Tools](#tools)
- [Environments](#environments)
- [Repository](#repository)
- [Basic requirements](#basic-requirements-for-the-services)
- [Expectations](#expectations)
- [Monitor the progress](#monitor-the-progress)

### Process:

- We use [github issues](https://github.com/features/issues)/projects/milestones as a tracker
- We create a project in github
- We use github pull requests as much as possible for reviews, even for the docs
- We communicate asynchronously as much as possible and make meetings only if needed
- Task coordinator Rafy Benjamin <[rafy.benjamin@hiro-microdatacenters.nl](mailto:rafy.benjamin@hiro-microdatacenters.nl)>
    - coordinates any integration work
    - any question or unclear situation? He is a main contact point.
- We follow 2 week sprints
- We encourage partners to apply Discovery/Delivery framework and HIRO can provide guidance how to implement that
- we piggyback on a biweekly meeting of task 6.2 where we
    - report progress
    - have a demo (recorded and shared in a group)
        - 3 minutes per partner
        - demonstrate the APIs, documents, insights as a discovery outcome
        - demonstrate working software as part of delivery outcome
        - Service/components owners needs to update the tickets with the status of what is done
- Every service has an owner in the readme with their contact - mail. The owner will be assigned tasks in github project

### Tools:

- documentation markdown format in the github repository
- diagrams - [draw.io](http://draw.io) or [mermaid.live](http://mermaid.live) committed to github repository
- docker image repository - (it is being prepared by [Guangyuan.Piao@dell.com](mailto:Guangyuan.Piao@dell.com))
- helm chart repository - [https://artifacthub.io/](https://artifacthub.io/)
- HIRO provides a template for integrated github workflows CI/CD for python based service

### Environments:

- Partner development environment
    - Kubernetes clusters are provided by DELL. Everyone should have access to those.
- Integration environment
    - K8s is provided by DELL

### Repository:

- Partners can request access to repository by writing to  [glaciation-hiro@hiro-microdatacenters.nl](mailto:glaciation-hiro@hiro-microdatacenters.nl)

### Basic requirements for the services:

- Service implementation details is up to the team who is responsible on the service
- The service should have openapi.yaml service description in the `<service>/openeapi` folder of the repo
- The API must follow the REST API principles
    - [https://spec.openapis.org/oas/v3.1.0](https://spec.openapis.org/oas/v3.1.0)
    - [https://swagger.io/resources/articles/best-practices-in-api-design/](https://swagger.io/resources/articles/best-practices-in-api-design/)
- The service should be dockerized and helm chart available (HIRO will provide template python service where all boilerplate is already implemented)
- It is expected lightweight markdown documentation about a service in the `<service>/docs` section:
    - The main domain concepts described (see domain driven design)
    - How to build the service
    - How to setup local dev environment
    - How to deploy the service to remote environment
    - Service dependencies and their contacts - mailing list
    - Possible issues and how to troubleshoot them
    - In folder `<service>/docs/adr` we keep implementation specific documentation/decisions in the form of [Architecture Decision Records](https://adr.github.io/), This is especially valuable if joint decisions are made by peers
    

### Expectations:

#### The milestones for 2.4 are the following (mostly about definitions and interfaces):

- Requirements for the services are defined and interaction diagrams are available.
- Domain model/terminology is defined and REST/OpenAPI spec is available.
- Service stubs (only api and no implementation yet) are available and they should be able to run standalone in integration environment.

#### The milestones for 7.2 are the following (this is about integrations of components together):

- Integration environment is available. Ground work on setting up integration environment.
- Core Integration is done with stub services (make sure components can talk to each other)
- a number of service integration iterations


### Monitor the progress:
- Tasks that will be on Github project
- two week sprints
- Biweekly meeting of task 6.2