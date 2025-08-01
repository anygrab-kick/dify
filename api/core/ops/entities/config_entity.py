from enum import StrEnum

from pydantic import BaseModel, ValidationInfo, field_validator


class TracingProviderEnum(StrEnum):
    ARIZE = "arize"
    PHOENIX = "phoenix"
    LANGFUSE = "langfuse"
    LANGSMITH = "langsmith"
    OPIK = "opik"
    WEAVE = "weave"
    ALIYUN = "aliyun"


class BaseTracingConfig(BaseModel):
    """
    Base model class for tracing
    """

    ...


class ArizeConfig(BaseTracingConfig):
    """
    Model class for Arize tracing config.
    """

    api_key: str | None = None
    space_id: str | None = None
    project: str | None = None
    endpoint: str = "https://otlp.arize.com"

    @field_validator("project")
    @classmethod
    def project_validator(cls, v, info: ValidationInfo):
        if v is None or v == "":
            v = "default"

        return v

    @field_validator("endpoint")
    @classmethod
    def endpoint_validator(cls, v, info: ValidationInfo):
        if v is None or v == "":
            v = "https://otlp.arize.com"
        if not v.startswith(("https://", "http://")):
            raise ValueError("endpoint must start with https:// or http://")
        if "/" in v[8:]:
            parts = v.split("/")
            v = parts[0] + "//" + parts[2]

        return v


class PhoenixConfig(BaseTracingConfig):
    """
    Model class for Phoenix tracing config.
    """

    api_key: str | None = None
    project: str | None = None
    endpoint: str = "https://app.phoenix.arize.com"

    @field_validator("project")
    @classmethod
    def project_validator(cls, v, info: ValidationInfo):
        if v is None or v == "":
            v = "default"

        return v

    @field_validator("endpoint")
    @classmethod
    def endpoint_validator(cls, v, info: ValidationInfo):
        if v is None or v == "":
            v = "https://app.phoenix.arize.com"
        if not v.startswith(("https://", "http://")):
            raise ValueError("endpoint must start with https:// or http://")
        if "/" in v[8:]:
            parts = v.split("/")
            v = parts[0] + "//" + parts[2]

        return v


class LangfuseConfig(BaseTracingConfig):
    """
    Model class for Langfuse tracing config.
    """

    public_key: str
    secret_key: str
    host: str = "https://api.langfuse.com"

    @field_validator("host")
    @classmethod
    def set_value(cls, v, info: ValidationInfo):
        if v is None or v == "":
            v = "https://api.langfuse.com"
        if not v.startswith("https://") and not v.startswith("http://"):
            raise ValueError("host must start with https:// or http://")

        return v


class LangSmithConfig(BaseTracingConfig):
    """
    Model class for Langsmith tracing config.
    """

    api_key: str
    project: str
    endpoint: str = "https://api.smith.langchain.com"

    @field_validator("endpoint")
    @classmethod
    def set_value(cls, v, info: ValidationInfo):
        if v is None or v == "":
            v = "https://api.smith.langchain.com"
        if not v.startswith("https://"):
            raise ValueError("endpoint must start with https://")

        return v


class OpikConfig(BaseTracingConfig):
    """
    Model class for Opik tracing config.
    """

    api_key: str | None = None
    project: str | None = None
    workspace: str | None = None
    url: str = "https://www.comet.com/opik/api/"

    @field_validator("project")
    @classmethod
    def project_validator(cls, v, info: ValidationInfo):
        if v is None or v == "":
            v = "Default Project"

        return v

    @field_validator("url")
    @classmethod
    def url_validator(cls, v, info: ValidationInfo):
        if v is None or v == "":
            v = "https://www.comet.com/opik/api/"
        if not v.startswith(("https://", "http://")):
            raise ValueError("url must start with https:// or http://")
        if not v.endswith("/api/"):
            raise ValueError("url should ends with /api/")

        return v


class WeaveConfig(BaseTracingConfig):
    """
    Model class for Weave tracing config.
    """

    api_key: str
    entity: str | None = None
    project: str
    endpoint: str = "https://trace.wandb.ai"
    host: str | None = None

    @field_validator("endpoint")
    @classmethod
    def set_value(cls, v, info: ValidationInfo):
        if v is None or v == "":
            v = "https://trace.wandb.ai"
        if not v.startswith("https://"):
            raise ValueError("endpoint must start with https://")

        return v

    @field_validator("host")
    @classmethod
    def validate_host(cls, v, info: ValidationInfo):
        if v is not None and v != "":
            if not v.startswith(("https://", "http://")):
                raise ValueError("host must start with https:// or http://")
        return v


class AliyunConfig(BaseTracingConfig):
    """
    Model class for Aliyun tracing config.
    """

    app_name: str = "dify_app"
    license_key: str
    endpoint: str


OPS_FILE_PATH = "ops_trace/"
OPS_TRACE_FAILED_KEY = "FAILED_OPS_TRACE"
