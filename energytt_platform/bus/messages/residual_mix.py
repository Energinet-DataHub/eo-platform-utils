from dataclasses import dataclass

from energytt_platform.serialize import Serializable
from energytt_platform.models.residual_mix import \
    ResidualMixEmissions, ResidualMixTechnologyDistribution


@dataclass
class ResidualMixEmissionsUpdate(Serializable):
    """
    TODO
    """
    emissions: ResidualMixEmissions


@dataclass
class ResidualMixTechnologyDistributionUpdate(Serializable):
    """
    TODO
    """
    distributions: ResidualMixTechnologyDistribution
