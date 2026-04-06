from truefoundry.deploy import (
    Build, Service, PythonBuild, Port, Resources,
    ArtifactsDownload, TruefoundryArtifactSource
)

service = Service(
    name="iris-classifier",
    image=Build(
        build_spec=PythonBuild(
            # No requirements_path or local files needed —
            # just declare the packages MLServer needs
            pip_packages=["mlserver", "mlserver-sklearn"],
            python_version="3.11",
            command="mlserver start $MODEL_DIR",
        )
    ),
    ports=[
        Port(port=8080, host="iris-classifier.your-org.ai"),
        Port(port=8081),
    ],
    resources=Resources(
        cpu_request=0.5, cpu_limit=1.0,
        memory_request=512, memory_limit=1024,
    ),
    replicas=1,
    artifacts_download=ArtifactsDownload(
        artifacts=[
            TruefoundryArtifactSource(
                artifact_version_fqn="model:truefoundry/default/local-sklearn-seldon:1",
                download_path_env_variable="MODEL_DIR",
            )
        ]
    ),
)
service.deploy(workspace_fqn="your-tenant:your-cluster:your-workspace")
