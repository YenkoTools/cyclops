from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

_initialized = False


def configure_tracing(service_name: str, environment: str) -> None:
    global _initialized
    if _initialized:
        return

    resource = Resource.create(
        {
            "service.name": service_name,
            "deployment.environment": environment,
        }
    )
    provider = TracerProvider(resource=resource)
    endpoint = __import__("os").getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    headers = __import__("os").getenv("OTEL_EXPORTER_OTLP_HEADERS")
    if endpoint:
        exporter = OTLPSpanExporter(endpoint=endpoint, headers=headers)
        provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    _initialized = True


@contextmanager
def traced_span(name: str, **attributes: str) -> Iterator[None]:
    tracer = trace.get_tracer("cyclops")
    with tracer.start_as_current_span(name) as span:
        for key, value in attributes.items():
            if value is not None:
                span.set_attribute(key, value)
        yield
