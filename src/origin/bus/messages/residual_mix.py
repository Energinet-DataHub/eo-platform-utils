from dataclasses import dataclass

from src.origin.bus import Message
from src.origin.models.residual_mix import \
    ResidualMixEmissions, ResidualMixTechnologyDistribution


@dataclass
class ResidualMixEmissionsUpdate(Message):
    """
    TODO
    """
    emissions: ResidualMixEmissions


@dataclass
class ResidualMixTechnologyDistributionUpdate(Message):
    """
    TODO
    """
    distributions: ResidualMixTechnologyDistribution
