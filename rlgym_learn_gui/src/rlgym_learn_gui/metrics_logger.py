from dataclasses import dataclass
from typing import Any, Dict, Generic, List, TypeVar

from pydantic import BaseModel
from rlgym_learn.api.typing import AgentControllerData
from rlgym_learn_algos.logging.dict_metrics_logger import DictMetricsLogger
from rlgym_learn_algos.logging.metrics_logger import (
    DerivedMetricsLoggerConfig,
    MetricsLogger,
)

from rlgym_learn_gui.communication import GUICommunicator

InnerMetricsLoggerConfig = TypeVar("InnerMetricsLoggerConfig")
InnerMetricsLoggerDerivedConfig = TypeVar("InnerMetricsLoggerDerivedConfig")


def convert_nested_dict(d):
    new = {}
    for k, v in d.items():
        if isinstance(v, dict):
            converted = convert_nested_dict(v)
            to_add = {f"{k}/{k1}": v1 for k1, v1 in converted.items()}
        else:
            to_add = {k: v}
        new = {**new, **to_add}
    return new


class GUIMetricsLoggerConfig(BaseModel, Generic[InnerMetricsLoggerConfig]):
    session_id: str | None = None
    port: int | None = None

    inner_metrics_logger_config: dict[str, Any] | InnerMetricsLoggerConfig | None = None


@dataclass
class GUIDerivedConfig(Generic[InnerMetricsLoggerDerivedConfig]):
    metrics_logger_config: GUIMetricsLoggerConfig
    session_id: str | None = None
    port: int | None = None
    inner_metrics_logger_derived_config: InnerMetricsLoggerDerivedConfig | None = None


class GUIMetricsLogger(
    MetricsLogger[
        GUIMetricsLoggerConfig[InnerMetricsLoggerConfig],
        GUIDerivedConfig[InnerMetricsLoggerDerivedConfig],
        AgentControllerData,
    ],
    Generic[
        InnerMetricsLoggerConfig,
        InnerMetricsLoggerDerivedConfig,
        AgentControllerData,
    ],
):
    def __init__(
        self,
        inner_metrics_logger: DictMetricsLogger[
            InnerMetricsLoggerConfig,
            InnerMetricsLoggerDerivedConfig,
            AgentControllerData,
        ],
        checkpoint_file_name: str = "gui_metrics_logger.json",
    ):
        self.inner_metrics_logger = inner_metrics_logger
        self.checkpoint_file_name = checkpoint_file_name

    def collect_env_metrics(self, data: List[Dict[str, Any]]):
        self.inner_metrics_logger.collect_env_metrics(data)

    def collect_agent_metrics(self, data: AgentControllerData):
        self.inner_metrics_logger.collect_agent_metrics(data)

    def report_metrics(self):
        _metrics = convert_nested_dict(self.inner_metrics_logger.get_metrics())
        self.gui_communicator.send_metrics(_metrics)
        self.inner_metrics_logger.report_metrics()

    def validate_config(self, config_obj: Any) -> GUIMetricsLoggerConfig:
        _base_config = GUIMetricsLoggerConfig.model_validate(config_obj)

        if _base_config.inner_metrics_logger_config is not None:
            _base_config.inner_metrics_logger_config = (
                self.inner_metrics_logger.validate_config(
                    config_obj["inner_metrics_logger_config"]
                )
            )

        return _base_config

    def load(self, config):
        self.config = config

        _session_id = config.metrics_logger_config.session_id
        if _session_id is None:
            _session_id = config.additional_derived_config.session_id

            if _session_id is None:
                raise ValueError(
                    "No session id provided by the user nor by the agent controller"
                )

        _port = config.metrics_logger_config.port
        if _port is None:
            _port = config.additional_derived_config.port

            if _port is None:
                raise ValueError(
                    "No port provided by the user nor by the agent controller"
                )

        self.gui_communicator = GUICommunicator(
            _session_id,
            _port,
            "metrics_logger",
        )

        self.inner_metrics_logger.load(
            DerivedMetricsLoggerConfig(
                checkpoint_load_folder=config.checkpoint_load_folder,
                agent_controller_name=config.agent_controller_name,
                metrics_logger_config=config.metrics_logger_config.inner_metrics_logger_config,
                additional_derived_config=config.additional_derived_config.inner_metrics_logger_derived_config
                if config.additional_derived_config is not None
                else None,
            )
        )
