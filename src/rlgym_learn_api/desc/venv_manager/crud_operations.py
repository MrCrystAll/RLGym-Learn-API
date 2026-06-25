import os
from enum import StrEnum

from pydantic import BaseModel, Field


class VenvRLGymPreset(StrEnum):
    API = "api"
    ROCKET_LEAGUE = "rocket_league"


class VenvLearnPreset(StrEnum):
    API = "api"
    PPO = "ppo"


class VenvPreset(BaseModel):
    rlgym_preset: VenvRLGymPreset
    learn_preset: VenvLearnPreset


class VenvCreationArgs(BaseModel):
    project_id: str
    python_executable: str | os.PathLike[str]
    preset: VenvPreset | None = None


class VenvInstallArgs(BaseModel):
    project_id: str
    package_name: str
    extra_args: list[str] = Field(default_factory=list)


class VenvUninstallArgs(BaseModel):
    project_id: str
    package_name: str


class VenvUpdateArgs(BaseModel):
    project_id: str
    package_name: str


class VenvInstallRequirementsArgs(BaseModel):
    project_id: str
    requirements_path: str | os.PathLike[str]
    extra_args: list[str] = Field(default_factory=list)


def _rlgym_dependencies(preset: VenvRLGymPreset) -> list[str]:
    match preset:
        case VenvRLGymPreset.API:
            return ["rlgym"]
        case VenvRLGymPreset.ROCKET_LEAGUE:
            return ["rlgym[rl]"]


def _learn_dependencies(preset: VenvLearnPreset) -> list[str]:
    match preset:
        case VenvLearnPreset.API:
            return ["git+https://github.com/MrCrystAll/rlgym-learn@GUI"]
        case VenvLearnPreset.PPO:
            return ["git+https://github.com/MrCrystAll/rlgym-learn-algos@GUI"]


def get_preset_dependencies(preset: VenvPreset | None) -> list[str]:
    if preset is None:
        return []

    return [
        *_rlgym_dependencies(preset.rlgym_preset),
        *_learn_dependencies(preset.learn_preset),
    ]
